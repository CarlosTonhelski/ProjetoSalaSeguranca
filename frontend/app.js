// ── BACKEND ───────────────────────────────────────────────────
const BACKEND = 'http://localhost:5000';

// ── DADOS ──────────────────────────────────────────────────────
let colaboradores = [];

let nextEvId = 1;

let eventos = [];

const dentroSala = new Set();

let editingId = null;

// ── UTILITÁRIOS ────────────────────────────────────────────────
const $ = id => document.getElementById(id);

const initials = nome =>
  nome
    .split(' ')
    .slice(0, 2)
    .map(w => w[0])
    .join('')
    .toUpperCase();

const nowStr = () =>
  new Date()
    .toISOString()
    .slice(0, 16)
    .replace('T', ' ');

// ── TOAST ──────────────────────────────────────────────────────
function toast(msg, tipo) {

  const t = $('toast');

  t.textContent = msg;

  t.className = `toast show toast-${tipo}`;

  setTimeout(() => {

    t.className = 'toast';

  }, 2500);
}

// ── CARREGAR COLABORADORES ────────────────────────────────────
async function carregarColaboradores() {

  try {

    const response = await fetch(
      `${BACKEND}/colaboradores`
    );

    colaboradores = await response.json();

    renderTabela();

  } catch {

    toast(
      'Erro ao carregar colaboradores',
      'err'
    );
  }
}

// ── CARREGAR SALA ──────────────────────────────────────────────
async function carregarSala() {

  try {

    const response = await fetch(
      `${BACKEND}/sala`
    );

    const pessoas = await response.json();

    dentroSala.clear();

    pessoas.forEach(nome => {

      dentroSala.add(nome);
    });

    const container = $('inside-list');

    if (!container) return;

    if (!pessoas.length) {

      container.innerHTML = `
        <div class="empty-state">
          Nenhum colaborador na sala
        </div>
      `;

      return;
    }

    container.innerHTML = pessoas.map(nome => `

      <div class="inside-person">

        <div class="avatar">
          ${initials(nome)}
        </div>

        <div>
          ${nome}
        </div>

      </div>

    `).join('');

  } catch {

    toast(
      'Erro ao carregar sala',
      'err'
    );
  }
}

// ── EVENTOS RECENTES ───────────────────────────────────────────
async function carregarEventosRecentes() {

  try {

    const response = await fetch(
      `${BACKEND}/logs`
    );

    const logs = await response.json();

    const container = $('recent-events');

    if (!container) return;

    if (!logs.length) {

      container.innerHTML = `
        <div class="empty-state">
          Nenhum evento registrado
        </div>
      `;

      return;
    }

    container.innerHTML = logs
      .slice(0, 10)
      .map(log => {

        let badge = 'badge-blue';

        if (log.tipo_evento === 'NEGADO') {
          badge = 'badge-yellow';
        }

        if (log.tipo_evento === 'INVASAO') {
          badge = 'badge-red';
        }

        if (log.tipo_evento === 'ENTRADA') {
          badge = 'badge-green';
        }

        return `

          <div class="event-item">

            <div>

              <div class="event-title">
                ${log.tag || 'RFID'}
              </div>

              <div class="event-date">
                ${new Date(
                  log.data_hora
                ).toLocaleString()}
              </div>

            </div>

            <span class="badge ${badge}">
              ${log.tipo_evento}
            </span>

          </div>

        `;
      })
      .join('');

  } catch {

    toast(
      'Erro ao carregar eventos',
      'err'
    );
  }
}

// ── ATUALIZAR CONTROLE ─────────────────────────────────────────
async function atualizarControle() {

  await carregarSala();

  renderControle();

  carregarEventosRecentes();
}

// ── AUTH ───────────────────────────────────────────────────────
async function fazerLogin() {

  const username = $('login-user')
    .value
    .trim();

  const senha = $('login-pass')
    .value
    .trim();

  if (!username || !senha) {

    toast(
      'Informe usuário e senha',
      'err'
    );

    return;
  }

  try {

    const response = await fetch(
      `${BACKEND}/login`,
      {

        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          username,
          senha
        })
      }
    );

    const data = await response.json();

    if (response.ok) {

      $('login-screen').style.display = 'none';

      $('app').style.display = 'block';

      await carregarColaboradores();

      await atualizarControle();

      toast(data.mensagem, 'ok');

    } else {

      toast(data.mensagem, 'err');
    }

  } catch {

    toast(
      'Erro ao conectar no backend',
      'err'
    );
  }
}

// ── LOGOUT ─────────────────────────────────────────────────────
function fazerLogout() {

  $('login-screen').style.display = 'flex';

  $('app').style.display = 'none';
}

// ── ENTER LOGIN ────────────────────────────────────────────────
document.addEventListener('keydown', e => {

  if (
    e.key === 'Enter' &&
    $('login-screen').style.display !== 'none'
  ) {
    fazerLogin();
  }
});

// ── NAVEGAÇÃO ──────────────────────────────────────────────────
function showTab(tab) {

  const tabs = [
    'cadastro',
    'colaboradores',
    'controle'
  ];

  document
    .querySelectorAll('nav a')
    .forEach((el, i) => {

      el.classList.toggle(
        'active',
        tabs[i] === tab
      );
    });

  document
    .querySelectorAll('.page')
    .forEach(p => {

      p.classList.remove('active');
    });

  $('page-' + tab)
    .classList
    .add('active');

  if (tab === 'colaboradores') {

    renderTabela();
  }

  if (tab === 'controle') {

    atualizarControle();
  }
}

// ── CADASTRO ───────────────────────────────────────────────────
async function salvarColaborador() {

  const nome = $('f-nome')
    .value
    .trim();

  const matricula = $('f-matricula')
    .value
    .trim();

  const cargo = $('f-cargo')
    .value
    .trim();

  const rfid = $('f-rfid')
    .value
    .trim();

  if (
    !nome ||
    !matricula ||
    !cargo ||
    !rfid
  ) {

    toast(
      'Preencha todos os campos.',
      'err'
    );

    return;
  }

  const colaborador = {

    nome,

    matricula,

    cargo,

    rfid_tag: rfid,

    acesso_permitido:
      $('f-acesso').value === '1',

    ativo:
      $('f-status').value === '1'
  };

  try {

    const response = await fetch(
      `${BACKEND}/colaboradores`,
      {

        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify(colaborador)
      }
    );

    const data = await response.json();

    if (response.ok) {

      toast(data.mensagem, 'ok');

      limparForm();

      carregarColaboradores();

    } else {

      toast(data.erro, 'err');
    }

  } catch {

    toast(
      'Erro ao conectar no backend',
      'err'
    );
  }
}

// ── LIMPAR FORM ────────────────────────────────────────────────
function limparForm() {

  [
    'f-nome',
    'f-matricula',
    'f-cargo',
    'f-rfid'
  ].forEach(id => {

    $(id).value = '';
  });

  $('f-acesso').value = '1';

  $('f-status').value = '1';
}

// ── TABELA ─────────────────────────────────────────────────────
function renderTabela() {

  const busca = (
    $('busca') || { value: '' }
  )
    .value
    .toLowerCase();

  const lista = colaboradores.filter(c =>

    c.nome.toLowerCase().includes(busca) ||

    c.matricula.toLowerCase().includes(busca) ||

    c.cargo.toLowerCase().includes(busca)
  );

  const tb = $('tabela-body');

  if (!lista.length) {

    tb.innerHTML = `
      <tr class="empty-row">
        <td colspan="8">
          Nenhum colaborador cadastrado
        </td>
      </tr>
    `;

    return;
  }

  tb.innerHTML = lista.map(c => `

    <tr>

      <td>
        <div class="avatar">
          ${initials(c.nome)}
        </div>
      </td>

      <td>${c.nome}</td>

      <td>${c.matricula}</td>

      <td>${c.cargo}</td>

      <td>${c.rfid_tag}</td>

      <td>
        ${
          c.acesso_permitido
          ? '<span class="badge badge-green">Sim</span>'
          : '<span class="badge badge-yellow">Não</span>'
        }
      </td>

      <td>
        ${
          c.ativo
          ? '<span class="badge badge-green">Ativo</span>'
          : '<span class="badge badge-red">Inativo</span>'
        }
      </td>

      <td style="display:flex;gap:6px">

        <button
          class="btn btn-sm"
          onclick="abrirModal(${c.id})"
        >
          ✏️
        </button>

        <button
          class="btn btn-sm btn-ghost"
          onclick="excluir(${c.id})"
        >
          🗑️
        </button>

      </td>

    </tr>

  `).join('');
}

// ── CONTROLE ───────────────────────────────────────────────────
function renderControle() {

  const entradas = eventos.filter(
    e => e.tipo === 'entrada'
  ).length;

  const negados = eventos.filter(
    e => e.tipo === 'negado'
  ).length;

  const invasoes = eventos.filter(
    e => e.tipo === 'invasao'
  ).length;

  $('stats-row').innerHTML = `

    <div class="stat-card green">

      <div class="stat-value">
        ${dentroSala.size}
      </div>

      <div class="stat-label">
        DENTRO DA SALA
      </div>

    </div>

    <div class="stat-card blue">

      <div class="stat-value">
        ${entradas}
      </div>

      <div class="stat-label">
        ENTRADAS HOJE
      </div>

    </div>

    <div class="stat-card yellow">

      <div class="stat-value">
        ${negados}
      </div>

      <div class="stat-label">
        ACESSOS NEGADOS
      </div>

    </div>

    <div class="stat-card red">

      <div class="stat-value">
        ${invasoes}
      </div>

      <div class="stat-label">
        TENTATIVAS INVASÃO
      </div>

    </div>
  `;
}

// ── RFID ───────────────────────────────────────────────────────
async function simularLeitura() {

  const tag = $('sim-tag')
    .value
    .trim();

  if (!tag) {

    toast(
      'Informe uma RFID',
      'err'
    );

    return;
  }

  try {

    const response = await fetch(
      `${BACKEND}/rfid`,
      {

        method: 'POST',

        headers: {
          'Content-Type': 'application/json'
        },

        body: JSON.stringify({
          rfid_tag: tag
        })
      }
    );

    const data = await response.json();

    const res = $('sim-result');

    res.style.display = 'block';

    res.textContent = data.mensagem;

    if (data.status === 'permitido') {

      res.className =
        'sim-result sim-ok';

    } else if (data.status === 'saida') {

      res.className =
        'sim-result sim-info';

    } else if (data.status === 'negado') {

      res.className =
        'sim-result sim-warn';

    } else {

      res.className =
        'sim-result sim-err';
    }

    $('sim-tag').value = '';

    adicionarEvento(
      data.tipo_evento?.toLowerCase() ||
      'invasao',
      null,
      tag
    );

    await atualizarControle();

  } catch {

    toast(
      'Erro ao comunicar com backend',
      'err'
    );
  }
}

// ── EVENTOS ────────────────────────────────────────────────────
function adicionarEvento(
  tipo,
  colId,
  tag
) {

  eventos.push({

    id: nextEvId++,

    tipo,

    colaboradorId: colId,

    tag,

    ts: nowStr()
  });
}
