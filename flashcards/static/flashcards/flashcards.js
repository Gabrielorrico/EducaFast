let estado = {
  materiaId: null,
  materiaNome: '',
  materiaIcone: '',
  materiaCor: '',
  assuntos: [],
  assuntoId: null,
  assuntoNome: '',
  resumo: '',
  flashcards: [],
  cardIndex: 0,
  virado: false,
  cardsEstudados: new Set(),
  assuntoConcluido: false,
};

let debounceTimer = null;

const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

/* ──────────────────────────────────────────
   Inicialização
────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  $$('.btn-materia').forEach(btn => {
    btn.addEventListener('click', () => selecionarMateria(btn));
  });

  document.addEventListener('input', e => {
    if (e.target.id === 'input-busca') {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => buscarAssuntos(e.target.value.trim()), 300);
    }
  });

  document.addEventListener('click', e => {
    if (e.target.closest('button')) return;
    const flip = e.target.closest('#flip-area');
    if (flip) virarCard();
  });

  document.addEventListener('keydown', e => {
    if (e.target.id === 'flip-area' && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      virarCard();
    }

    if (estado.flashcards.length) {
      if (e.key === 'ArrowRight') avancarCard();
      if (e.key === 'ArrowLeft') voltarCard();
      if (e.key === ' ') {
        e.preventDefault();
        virarCard();
      }
    }
  });
});

/* ──────────────────────────────────────────
   ESTUDADO
────────────────────────────────────────── */
async function marcarComoEstudado(cardId) {
  const url = URL_MARCAR_ESTUDADO.replace('0', cardId);
  const tokenEl = document.querySelector('meta[name="csrf-token"]');
  const token = tokenEl ? tokenEl.getAttribute('content') : '';

  try {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': token,
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
      },
    });

    if (resp.ok) {
      estado.cardsEstudados.add(cardId);
      return true;
    }

    console.error('[Flashcards] Erro ao marcar como estudado:', resp.status);
    return false;
  } catch (err) {
    console.error('[Flashcards] Erro ao marcar como estudado:', err);
    return false;
  }
}

async function concluirAssunto() {
  if (!estado.flashcards || !estado.flashcards.length) return;

  const resultados = await Promise.all(
    estado.flashcards.map(card => marcarComoEstudado(card.id))
  );

  if (resultados.every(Boolean)) {
    estado.assuntoConcluido = true;
    atualizarBotaoDireito(true);
  }
}

/* ──────────────────────────────────────────
   ETAPA 1 — MATÉRIA
────────────────────────────────────────── */
function selecionarMateria(btn) {
  $$('.btn-materia').forEach(b => b.classList.remove('selecionada'));
  btn.classList.add('selecionada');

  estado.materiaId = btn.dataset.materiaId;
  estado.materiaNome = btn.dataset.materiaNome;
  estado.materiaIcone = btn.dataset.materiaIcone;
  estado.materiaCor = btn.dataset.materiaCor;
  estado.assuntoId = null;
  estado.assuntoNome = '';
  estado.resumo = '';
  estado.flashcards = [];
  estado.cardIndex = 0;
  estado.virado = false;
  estado.cardsEstudados = new Set();
  estado.assuntoConcluido = false;

  const inputBusca = $('#input-busca');
  if (inputBusca) inputBusca.value = '';

  esconderSecao('secao-flashcards');
  carregarAssuntos('');
}

/* ──────────────────────────────────────────
   ETAPA 2 — ASSUNTOS
────────────────────────────────────────── */
async function carregarAssuntos(q = '') {
  if (!estado.materiaId) return;

  if (!$('#secao-assuntos')) criarSecaoAssuntos();

  const grid = $('#grid-assuntos');
  if (grid) {
    grid.innerHTML = `
      <div class="loading-wrap">
        <div class="spinner"></div>
        <span>Carregando assuntos…</span>
      </div>
    `;
  }

  mostrarSecao('secao-assuntos');

  try {
    const url = `${URL_API_ASSUNTOS.replace('0', estado.materiaId)}?q=${encodeURIComponent(q)}`;
    const resp = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
    const data = await resp.json();

    estado.assuntos = data.assuntos || [];
    renderizarAssuntos(estado.assuntos, q);
  } catch (err) {
    console.error('[Flashcards] Erro ao carregar assuntos:', err);
    if (grid) grid.innerHTML = renderAvisoEstado('⚠️', 'Erro ao carregar assuntos.');
  }
}

function buscarAssuntos(q) {
  carregarAssuntos(q);
}

function criarSecaoAssuntos() {
  $('#conteudo-principal').insertAdjacentHTML('beforeend', `
    <section class="secao-assuntos" id="secao-assuntos" style="display:none">
      <div class="assuntos-header">
        <div class="assuntos-titulo">
          <span id="assuntos-icone-materia"></span>
          <span class="materia-badge" id="assuntos-nome-materia"></span>
        </div>
        <label class="busca-wrap">
          <span class="busca-icone">🔍</span>
          <input type="search" id="input-busca" class="input-busca" placeholder="Buscar assunto…" autocomplete="off" />
        </label>
      </div>
      <div class="grid-assuntos" id="grid-assuntos" role="list"></div>
    </section>
  `);
}

function renderizarAssuntos(assuntos, busca) {
  const grid = $('#grid-assuntos');
  if (!grid) return;

  const icone = $('#assuntos-icone-materia');
  const nome = $('#assuntos-nome-materia');
  if (icone) icone.textContent = estado.materiaIcone;
  if (nome) nome.textContent = estado.materiaNome;

  if (!assuntos || !assuntos.length) {
    grid.innerHTML = renderAvisoEstado(busca ? '🔍' : '📭', 'Nenhum assunto encontrado.');
    return;
  }

  grid.innerHTML = assuntos.map(a => `
    <button class="card-assunto" data-assunto-id="${a.id}" type="button">
      <div class="assunto-info">
        <span class="assunto-nome">${escHtml(a.nome)}</span>
        <span class="assunto-qtd">${a.total} flashcards</span>
      </div>
      <span class="assunto-seta">›</span>
    </button>
  `).join('');

  grid.querySelectorAll('.card-assunto').forEach(card => {
    card.addEventListener('click', () => selecionarAssunto(card.dataset.assuntoId));
  });
}

/* ──────────────────────────────────────────
   ETAPA 3 — FLASHCARDS
────────────────────────────────────────── */
async function selecionarAssunto(id) {
  const main = $('#conteudo-principal');

  let secao = $('#secao-flashcards');
  if (!secao) {
    main.insertAdjacentHTML('beforeend', `<div id="secao-flashcards" class="secao-flashcards" style="display:none"></div>`);
    secao = $('#secao-flashcards');
  }

  secao.innerHTML = `
    <div class="painel-flash">
      <div class="loading-wrap">
        <div class="spinner"></div>
        <span>Carregando cards…</span>
      </div>
    </div>
  `;
  mostrarSecao('secao-flashcards');

  try {
    const url = URL_API_FLASHCARDS.replace('0', id);
    const resp = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
    const data = await resp.json();

    if (data.erro) {
      secao.innerHTML = renderAvisoEstado('📭', data.erro);
      return;
    }

    estado.assuntoId = id;
    estado.assuntoNome = data.assunto?.nome || '';
    estado.resumo = data.assunto?.resumo || '';
    estado.flashcards = data.flashcards || [];
    estado.cardIndex = 0;
    estado.virado = false;
    estado.assuntoConcluido = false;
    estado.cardsEstudados = new Set(
      estado.flashcards.filter(c => c.estudado).map(c => c.id)
    );

    renderizarVisualizador(secao, data);
  } catch (err) {
    console.error('[Flashcards] Erro ao carregar flashcards:', err);
    secao.innerHTML = renderAvisoEstado('⚠️', 'Erro ao carregar flashcards.');
  }
}

/* ──────────────────────────────────────────
   RENDER
────────────────────────────────────────── */
function renderizarVisualizador(container, data) {
  console.log('RENDERIZOU VISUALIZADOR 🔥');

  if (!estado.flashcards || estado.flashcards.length === 0) {
    container.innerHTML = `
      <div class="painel-erro">
        <div class="erro-icone">📭</div>
        <p>Nenhum flashcard encontrado para esse assunto.</p>
      </div>
    `;
    return;
  }

  const total = estado.flashcards.length;
  const card = estado.flashcards[0];

  container.innerHTML = `
    <div class="flash-wrapper">
      <div class="flash-grid">
        <div class="painel-flash">

          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="flash-breadcrumb">
              <span>${escHtml(estado.materiaIcone)} ${escHtml(estado.materiaNome)}</span>
              <span class="sep">›</span>
              <strong>${escHtml(data.assunto?.nome || '')}</strong>
            </div>
            <button class="btn-voltar-assuntos" id="btn-voltar-assuntos" type="button">‹ Voltar</button>
          </div>

          <div class="flash-progresso">
            <span id="prog-texto">1 / ${total}</span>
            <div class="barra-prog-wrap">
              <div class="barra-prog" id="barra-prog" style="width:${((1 / total) * 100).toFixed(1)}%"></div>
            </div>
          </div>

          <div class="flip-area" id="flip-area" tabindex="0">
            <div class="flip-inner" id="flip-inner">
              <div class="flip-frente">
                <span class="flip-label">Pergunta</span>
                <p class="flip-texto" id="texto-frente">${escHtml(card.frente)}</p>
                <span class="flip-dica">Clique para ver a resposta</span>
              </div>
              <div class="flip-verso">
                <span class="flip-label">Resposta</span>
                <p class="flip-texto" id="texto-verso">${escHtml(card.verso)}</p>
              </div>
            </div>
          </div>

          <div class="flash-controles">
            <button class="btn-nav" id="btn-anterior" type="button" ${total <= 1 ? 'disabled' : ''}>◀</button>
            <button class="btn-virar" id="btn-virar" type="button">↕ Virar card</button>
            <button class="btn-nav btn-proximo-acao" id="btn-proximo" type="button">▶</button>
          </div>
        </div>

        <aside class="painel-resumo">
          <h2 class="resumo-titulo">📋 Resumo</h2>
          <p class="resumo-texto">${escHtml(data.assunto?.resumo || '')}</p>
        </aside>
      </div>
    </div>
  `;

  document.getElementById('btn-anterior')?.addEventListener('click', voltarCard);
  document.getElementById('btn-virar')?.addEventListener('click', virarCard);
  document.getElementById('btn-voltar-assuntos')?.addEventListener('click', voltarParaAssuntos);
  

  atualizarBotaoDireito();
}

/* ──────────────────────────────────────────
   NAVEGAÇÃO
────────────────────────────────────────── */
function virarCard() {
  const area = $('#flip-area');
  if (!area) return;

  estado.virado = !estado.virado;
  area.classList.toggle('virado', estado.virado);
}

function atualizarBotaoDireito(finalizado = false) {
  const btn = document.getElementById('btn-proximo');
  if (!btn) return;

  const ultimo = estado.cardIndex === estado.flashcards.length - 1;

  // RESET TOTAL DO BOTÃO
  btn.disabled = false;
  btn.classList.remove('btn-finalizado');
  btn.onclick = null;

  if (finalizado) {
    btn.textContent = '✓';
    btn.disabled = true;
    btn.classList.add('btn-finalizado');
    return;
  }

  if (ultimo) {
    console.log('🔥 CHEGOU NO ÚLTIMO CARD');

    btn.textContent = '✓';
    btn.disabled = false;
    btn.onclick = concluirAssunto;

  } else {
    btn.textContent = '▶';
    btn.onclick = avancarCard;
  }
}

function irParaCard(i) {
  if (i < 0 || i >= estado.flashcards.length) return;

  const card = estado.flashcards[i];
  estado.cardIndex = i;
  estado.virado = false;

  const frente = $('#texto-frente');
  const verso = $('#texto-verso');
  const area = $('#flip-area');
  const progTexto = $('#prog-texto');
  const barraProg = $('#barra-prog');
  const btnAnterior = $('#btn-anterior');

  if (frente) frente.textContent = card.frente;
  if (verso) verso.textContent = card.verso;
  if (area) area.classList.remove('virado');

  if (progTexto) progTexto.textContent = `${i + 1} / ${estado.flashcards.length}`;
  if (barraProg) barraProg.style.width = `${(((i + 1) / estado.flashcards.length) * 100).toFixed(1)}%`;

  if (btnAnterior) btnAnterior.disabled = i === 0;

  atualizarBotaoDireito();
}

function avancarCard() {
  if (estado.cardIndex < estado.flashcards.length - 1) {
    irParaCard(estado.cardIndex + 1);
  }
}

function voltarCard() {
  if (estado.cardIndex > 0) {
    irParaCard(estado.cardIndex - 1);
  }
}

function voltarParaAssuntos() {
  esconderSecao('secao-flashcards');
}

/* ────────────────────────────────────────── */
function mostrarSecao(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = '';
}

function esconderSecao(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

function escHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>"']/g, m => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;'
  }[m]));
}

function renderAvisoEstado(icone, titulo) {
  return `<div class="aviso-estado"><span class="aviso-icone">${icone}</span><p>${titulo}</p></div>`;
}