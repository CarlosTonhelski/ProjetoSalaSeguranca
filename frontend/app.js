// ── DADOS ──────────────────────────────────────────────────────
const BACKEND = 'http://localhost:5000';

let colaboradores = [
  { id:1, nome:'Joao',   matricula:'1136868', cargo:'Game Designer',  rfid:'TAG001', acesso:1, ativo:1 },
  { id:2, nome:'Carlos', matricula:'1137093', cargo:'Concept Artist',  rfid:'TAG002', acesso:1, ativo:1 },
  { id:3, nome:'Julia',  matricula:'1136562', cargo:'Estagiaria',      rfid:'TAG003', acesso:0, ativo:1 },
  { id:4, nome:'Maria',  matricula:'2026004', cargo:'RH',              rfid:'TAG004', acesso:0, ativo:1 },
];
let nextId = 5, eventos = [], nextEvId = 1;
const dentroSala = new Set();
let editingId = null;

// ── UTILITÁRIOS ────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const initials = nome => nome.split(' ').slice(0,2).map(w=>w[0]).join('').toUpperCase();
const nowStr   = () => new Date().toISOString().slice(0,16).replace('T',' ');

function toast(msg, tipo) {
  const t = $('toast');
  t.textContent = msg;
  t.className = `toast show toast-${tipo}`;
  setTimeout(() => t.className = 'toast', 2500);
}

// ── AUTH ───────────────────────────────────────────────────────
function fazerLogin() {
  if ($('login-user').value === 'admin' && $('login-pass').value === 'admin123') {
    $('login-screen').style.display = 'none';
    $('app').style.display = 'block';
    renderTabela(); renderControle();
  } else toast('Usuário ou senha incorretos.', 'err');
}

function fazerLogout() {
  $('login-screen').style.display = 'flex';
  $('app').style.display = 'none';
}

document.addEventListener('keydown', e => {
  if (e.key === 'Enter' && $('login-screen').style.display !== 'none') fazerLogin();
});

// ── NAVEGAÇÃO ──────────────────────────────────────────────────
function showTab(tab) {
  const tabs = ['cadastro', 'colaboradores', 'controle'];
  document.querySelectorAll('nav a').forEach((el, i) => el.classList.toggle('active', tabs[i] === tab));
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  $('page-' + tab).classList.add('active');
  if (tab === 'colaboradores') renderTabela();
  if (tab === 'controle')      renderControle();
}

// ── CADASTRO ───────────────────────────────────────────────────
function salvarColaborador() {
  const nome = $('f-nome').value.trim(), matricula = $('f-matricula').value.trim();
  const cargo = $('f-cargo').value.trim(), rfid = $('f-rfid').value.trim();
  const acesso = parseInt($('f-acesso').value), ativo = parseInt($('f-status').value);

  if (!nome || !matricula)                               { toast('Nome e matrícula são obrigatórios.', 'err'); return; }
  if (colaboradores.find(c => c.matricula === matricula)){ toast('Matrícula já cadastrada.', 'err'); return; }
  if (rfid && colaboradores.find(c => c.rfid === rfid))  { toast('Tag RFID já cadastrada.', 'err'); return; }

  colaboradores.push({ id: nextId++, nome, matricula, cargo, rfid, acesso, ativo });
  limparForm();
  $('form-feedback').textContent = `✓ ${nome} cadastrado com sucesso.`;
  $('form-feedback').style.display = 'block';
  setTimeout(() => $('form-feedback').style.display = 'none', 3000);
  toast(`${nome} cadastrado!`, 'ok');
}

function limparForm() {
  ['f-nome','f-matricula','f-cargo','f-rfid'].forEach(id => $(id).value = '');
  $('f-acesso').value = '1'; $('f-status').value = '1';
}

// ── TABELA COLABORADORES ───────────────────────────────────────
function renderTabela() {
  const busca = ($('busca') || { value:'' }).value.toLowerCase();
  const lista = colaboradores.filter(c =>
    c.nome.toLowerCase().includes(busca) ||
    c.matricula.toLowerCase().includes(busca) ||
    c.cargo.toLowerCase().includes(busca)
  );
  const tb = $('tabela-body');
  if (!lista.length) { tb.innerHTML = '<tr class="empty-row"><td colspan="8">Nenhum colaborador cadastrado</td></tr>'; return; }
  tb.innerHTML = lista.map(c => `
    <tr>
      <td><div class="avatar">${initials(c.nome)}</div></td>
      <td>${c.nome}</td>
      <td style="font-family:monospace;font-size:12px">${c.matricula}</td>
      <td>${c.cargo}</td>
      <td style="font-family:monospace;font-size:11px">${c.rfid || '—'}</td>
      <td>${c.acesso ? '<span class="badge badge-green">Sim</span>' : '<span class="badge badge-yellow">Não</span>'}</td>
      <td>${c.ativo  ? '<span class="badge badge-green">Ativo</span>' : '<span class="badge badge-red">Inativo</span>'}</td>
      <td style="display:flex;gap:6px">
        <button class="btn btn-sm" onclick="abrirModal(${c.id})">✏️ Editar</button>
        <button class="btn btn-sm btn-ghost" onclick="excluir(${c.id})">🗑️</button>
      </td>
    </tr>`).join('');
}

function excluir(id) {
  if (!confirm('Excluir este colaborador?')) return;
  colaboradores = colaboradores.filter(c => c.id !== id);
  dentroSala.delete(id);
  renderTabela();
  toast('Colaborador excluído.', 'warn');
}

function abrirModal(id) {
  const c = colaboradores.find(x => x.id === id); if (!c) return;
  editingId = id;
  $('e-nome').value = c.nome; $('e-matricula').value = c.matricula;
  $('e-cargo').value = c.cargo; $('e-rfid').value = c.rfid || '';
  $('e-acesso').value = c.acesso; $('e-status').value = c.ativo;
  $('modal-edit').classList.add('open');
}

function fecharModal() { $('modal-edit').classList.remove('open'); editingId = null; }

function salvarEdicao() {
  if (!editingId) return;
  const idx = colaboradores.findIndex(c => c.id === editingId); if (idx === -1) return;
  colaboradores[idx] = { ...colaboradores[idx],
    nome: $('e-nome').value.trim(), matricula: $('e-matricula').value.trim(),
    cargo: $('e-cargo').value.trim(), rfid: $('e-rfid').value.trim(),
    acesso: parseInt($('e-acesso').value), ativo: parseInt($('e-status').value),
  };
  fecharModal(); renderTabela(); toast('Colaborador atualizado.', 'ok');
}

// ── CONTROLE ───────────────────────────────────────────────────
function renderControle() {
  const entradas = eventos.filter(e => e.tipo === 'entrada').length;
  const negados  = eventos.filter(e => e.tipo === 'negado').length;
  const invasoes = eventos.filter(e => e.tipo === 'invasao').length;

  $('stats-row').innerHTML = `
    <div class="stat-card green"><div class="stat-value">${dentroSala.size}</div><div class="stat-label">Dentro da sala</div></div>
    <div class="stat-card blue"><div class="stat-value">${entradas}</div><div class="stat-label">Entradas hoje</div></div>
    <div class="stat-card yellow"><div class="stat-value">${negados}</div><div class="stat-label">Acessos negados</div></div>
    <div class="stat-card red"><div class="stat-value">${invasoes}</div><div class="stat-label">Tentativas invasão</div></div>`;

  const dotColors = { entrada:'green', saida:'blue', negado:'yellow', invasao:'red' };
  const labels    = { entrada:'Entrada autorizada', saida:'Saída registrada', negado:'Acesso negado', invasao:'Tentativa de invasão' };

  $('event-list').innerHTML = eventos.length
    ? [...eventos].reverse().slice(0,8).map(e => {
        const c = colaboradores.find(x => x.id === e.colaboradorId);
        return `<div class="event-item">
          <div class="event-dot ${dotColors[e.tipo]}"></div>
          <div><strong>${labels[e.tipo]}</strong><span style="color:var(--muted);margin-left:4px">— ${c ? c.nome : e.tag}</span></div>
          <span class="event-meta">${e.ts.slice(11)}</span>
        </div>`;
      }).join('')
    : '<p style="color:var(--muted);font-size:13px">Nenhum evento registrado.</p>';

  const dentro = [...dentroSala].map(id => colaboradores.find(c => c.id === id)).filter(Boolean);
  $('inside-list').innerHTML = dentro.length
    ? dentro.map(c => `
        <div class="inside-item">
          <div class="inside-avatar">${initials(c.nome)}</div>
          <div><div class="inside-name">${c.nome}</div><div class="inside-cargo">${c.cargo}</div></div>
          <span class="badge badge-green" style="margin-left:auto">Presente</span>
          <button class="btn btn-sm btn-ghost" onclick="retirarDaSala(${c.id})" style="margin-left:8px">🚪 Retirar</button>
        </div>`).join('')
    : '<p style="color:var(--muted);font-size:13px">Nenhum colaborador na sala.</p>';
}

function retirarDaSala(id) {
  const c = colaboradores.find(x => x.id === id); if (!c) return;
  dentroSala.delete(id);
  adicionarEvento('saida', id, c.rfid || '—');
  toast(`${c.nome} retirado da sala.`, 'warn');
  renderControle();
}

function simularLeitura() {
  const tag = $('sim-tag').value.trim();
  if (!tag) { toast('Informe uma tag RFID.', 'err'); return; }

  const c = colaboradores.find(x => x.rfid === tag);
  const res = $('sim-result');
  res.style.display = 'block';
  res.className = 'sim-result';

  if (!c) {
    res.classList.add('sim-err');
    res.textContent = '🚨 ALERTA — Tag não cadastrada. Possível tentativa de invasão!';
    adicionarEvento('invasao', null, tag);
  } else if (!c.ativo) {
    res.classList.add('sim-warn');
    res.textContent = `⛔ Colaborador ${c.nome} está inativo.`;
    adicionarEvento('negado', c.id, tag);
  } else if (!c.acesso) {
    res.classList.add('sim-warn');
    res.textContent = `🔒 ${c.nome} não possui permissão de acesso à sala.`;
    adicionarEvento('negado', c.id, tag);
  } else if (dentroSala.has(c.id)) {
    res.classList.add('sim-info');
    res.textContent = `👋 Até logo, ${c.nome}! Saída registrada.`;
    dentroSala.delete(c.id);
    adicionarEvento('saida', c.id, tag);
  } else {
    const jaEntrou = eventos.some(e => e.colaboradorId === c.id && e.tipo === 'entrada');
    res.classList.add('sim-ok');
    res.textContent = jaEntrou ? `✅ Bem-vindo de volta, ${c.nome}!` : `✅ Bem-vindo, ${c.nome}!`;
    dentroSala.add(c.id);
    adicionarEvento('entrada', c.id, tag);
  }
  $('sim-tag').value = '';
  renderControle();
}

function adicionarEvento(tipo, colId, tag) {
  eventos.push({ id: nextEvId++, tipo, colaboradorId: colId, tag, ts: nowStr() });
}
