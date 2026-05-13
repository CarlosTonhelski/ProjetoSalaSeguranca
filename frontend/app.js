app.js

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
  new Date().toISOString().slice(0, 16).replace('T', ' ');

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

  const response = await fetch(`${BACKEND}/colaboradores`);

  colaboradores = await response.json();

  renderTabela();
}

// ── AUTH ───────────────────────────────────────────────────────
async function fazerLogin() {

  const username = $('login-user').value;
  const senha = $('login-pass').value;

  const response = await fetch(`${BACKEND}/login`, {

    method: 'POST',

    headers: {
      'Content-Type': 'application/json'
    },

    body: JSON.stringify({
      username,
      senha
    })
  });

  const data = await response.json();

  if (response.ok) {

    $('login-screen').style.display = 'none';

    $('app').style.display = 'block';

    await carregarColaboradores();

    renderControle();

    toast(data.mensagem, 'ok');

  } else {

    toast(data.mensagem, 'err');
  }
}

function fazerLogout() {

  $('login-screen').style.display = 'flex';

  $('app').style.display = 'none';
}

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

  const tabs = ['cadastro', 'colaboradores', 'controle'];

  document.querySelectorAll('nav a').forEach((el, i) => {

    el.classList.toggle('active', tabs[i] === tab);
  });

  document.querySelectorAll('.page').forEach(p => {
    p.classList.remove('active');
  });

  $('page-' + tab).classList.add('active');

  if (tab === 'colaboradores') {
    renderTabela();
  }

  if (tab === 'controle') {
    renderControle();
  }
}

// ── CADASTRO ───────────────────────────────────────────────────
async function salvarColaborador() {

  const colaborador = {

    nome: $('f-nome').value.trim(),

    matricula: $('f-matricula').value.trim(),

    cargo: $('f-cargo').value.trim(),

    rfid_tag: $('f-rfid').value.trim(),

    acesso_permitido: $('f-acesso').value === '1',

    ativo: $('f-status').value === '1'
  };

  const response = await fetch(`${BACKEND}/colaboradores`, {

    method: 'POST',

    headers: {
      'Content-Type': 'application/json'
    },

    body: JSON.stringify(colaborador)
  });

  const data = await response.json();

  if (response.ok) {

    toast(data.mensagem, 'ok');

    limparForm();

    carregarColaboradores();

  } else {

    toast(data.erro, 'err');
  }
}

function limparForm() {

  ['f-nome', 'f-matricula', 'f-cargo', 'f-rfid']
    .forEach(id => {
      $(id).value = '';
    });

  $('f-acesso').value = '1';

  $('f-status').value = '1';
}

// ── TABELA ─────────────────────────────────────────────────────
function renderTabela() {

  const busca = ($('busca') || { value: '' })
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

      <td style="font-family:monospace;font-size:12px">
        ${c.matricula}
      </td>

      <td>${c.cargo}</td>

      <td style="font-family:monospace;font-size:11px">
        ${c.rfid_tag || '—'}
      </td>

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
          ✏️ Editar
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

// ── DELETE ─────────────────────────────────────────────────────
async function excluir(id) {

  if (!confirm('Excluir este colaborador?')) {
    return;
  }

  const response = await fetch(
    `${BACKEND}/colaboradores/${id}`,
    {
      method: 'DELETE'
    }
  );

  const data = await response.json();

  if (response.ok) {

    toast(data.mensagem, 'ok');

    carregarColaboradores();

  } else {

    toast(data.erro, 'err');
  }
}

// ── MODAL ──────────────────────────────────────────────────────
function abrirModal(id) {

  const c = colaboradores.find(x => x.id === id);

  if (!c) return;

  editingId = id;

  $('e-nome').value = c.nome;
  $('e-matricula').value = c.matricula;
  $('e-cargo').value = c.cargo;
  $('e-rfid').value = c.rfid_tag || '';
  $('e-acesso').value = c.acesso_permitido ? '1' : '0';
  $('e-status').value = c.ativo ? '1' : '0';

  $('modal-edit').classList.add('open');
}

function fecharModal() {

  $('modal-edit').classList.remove('open');

  editingId = null;
}

// ── EDITAR ─────────────────────────────────────────────────────
async function salvarEdicao() {

  if (!editingId) return;

  const colaborador = {

    nome: $('e-nome').value.trim(),

    matricula: $('e-matricula').value.trim(),

    cargo: $('e-cargo').value.trim(),

    rfid_tag: $('e-rfid').value.trim(),

    acesso_permitido: $('e-acesso').value === '1',

    ativo: $('e-status').value === '1'
  };

  const response = await fetch(
    `${BACKEND}/colaboradores/${editingId}`,
    {
      method: 'PUT',

      headers: {
        'Content-Type': 'application/json'
      },

      body: JSON.stringify(colaborador)
    }
  );

  const data = await response.json();

  if (response.ok) {

    toast(data.mensagem, 'ok');

    fecharModal();

    carregarColaboradores();

  } else {

    toast(data.erro, 'err');
  }
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
      <div class="stat-value">${dentroSala.size}</div>
      <div class="stat-label">Dentro da sala</div>
    </div>

    <div class="stat-card blue">
      <div class="stat-value">${entradas}</div>
      <div class="stat-label">Entradas hoje</div>
    </div>

    <div class="stat-card yellow">
      <div class="stat-value">${negados}</div>
      <div class="stat-label">Acessos negados</div>
    </div>

    <div class="stat-card red">
      <div class="stat-value">${invasoes}</div>
      <div class="stat-label">Tentativas invasão</div>
    </div>
  `;
}

// ── RFID ───────────────────────────────────────────────────────
async function simularLeitura() {

  const tag = $('sim-tag').value.trim();

  const response = await fetch(`${BACKEND}/rfid`, {

    method: 'POST',

    headers: {
      'Content-Type': 'application/json'
    },

    body: JSON.stringify({
      rfid_tag: tag
    })
  });

  const data = await response.json();

  const res = $('sim-result');

  res.style.display = 'block';

  res.textContent = data.mensagem;

  if (data.status === 'permitido') {

    res.className = 'sim-result sim-ok';

  } else if (data.status === 'saida') {

    res.className = 'sim-result sim-info';

  } else if (data.status === 'negado') {

    res.className = 'sim-result sim-warn';

  } else {

    res.className = 'sim-result sim-err';
  }

  $('sim-tag').value = '';

  adicionarEvento(
    data.tipo_evento?.toLowerCase() || 'invasao',
    null,
    tag
  );

  renderControle();
}

// ── EVENTOS ────────────────────────────────────────────────────
function adicionarEvento(tipo, colId, tag) {

  eventos.push({
    id: nextEvId++,
    tipo,
    colaboradorId: colId,
    tag,
    ts: nowStr()
  });
}

