/**
 * flashcards.js
 * Controla a lógica da página de flashcards do EDUCAFAST.
 *
 * Fluxo (BDD):
 *  Estado 0 → Só a seleção de matéria visível.
 *  Estado 1 → Matéria selecionada → seção de assuntos aparece (busca + grid).
 *  Estado 2 → Assunto selecionado → visualizador de flashcards aparece.
 *
 * Casos negativos tratados:
 *  - Nenhuma matéria selecionada → assuntos não aparecem (Estado 0).
 *  - Assunto sem flashcards     → mensagem de erro contextual.
 *  - Busca sem resultado        → aviso de "nenhum assunto encontrado".
 */

/* ──────────────────────────────────────────
   Estado global
   ────────────────────────────────────────── */
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
};

let debounceTimer = null;

/* ──────────────────────────────────────────
   Referencias DOM (lazy)
   ────────────────────────────────────────── */
const $ = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];

/* ──────────────────────────────────────────
   Inicialização
   ────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  // Botões de matéria
  $$('.btn-materia').forEach(btn => {
    btn.addEventListener('click', () => selecionarMateria(btn));
  });

  // Campo de busca — com debounce
  document.addEventListener('input', e => {
    if (e.target.id === 'input-busca') {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => buscarAssuntos(e.target.value.trim()), 300);
    }
  });

  // Virar card ao clicar na área
  document.addEventListener('click', e => {
    const flip = e.target.closest('#flip-area');
    if (flip) virarCard();
  });

  // Virar com teclado (Enter/Espaço)
  document.addEventListener('keydown', e => {
    if (e.target.id === 'flip-area' && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      virarCard();
    }
    // Atalhos de teclado no visualizador
    if (estado.flashcards.length) {
      if (e.key === 'ArrowRight') avancarCard();
      if (e.key === 'ArrowLeft') voltarCard();
      if (e.key === ' ') { e.preventDefault(); virarCard(); }
    }
  });
});

/* ──────────────────────────────────────────
   ETAPA 1 — Selecionar Matéria
   ────────────────────────────────────────── */
function selecionarMateria(btn) {
  // Atualiza visual dos botões
  $$('.btn-materia').forEach(b => b.classList.remove('selecionada'));
  btn.classList.add('selecionada');

  // Atualiza estado
  estado.materiaId   = btn.dataset.materiaId;
  estado.materiaNome  = btn.dataset.materiaNome;
  estado.materiaIcone = btn.dataset.materiaIcone;
  estado.materiaCor   = btn.dataset.materiaCor;
  estado.assuntoId   = null;
  estado.flashcards  = [];
  estado.cardIndex   = 0;
  estado.virado      = false;

  // Limpa busca anterior
  const inputBusca = $('#input-busca');
  if (inputBusca) inputBusca.value = '';

  // Esconde visualizador se estava aberto
  esconderSecao('secao-flashcards');

  // Carrega os assuntos
  carregarAssuntos('');
}

/* ──────────────────────────────────────────
   ETAPA 2 — Carregar / Buscar Assuntos
   ────────────────────────────────────────── */
async function carregarAssuntos(q = '') {
  if (!estado.materiaId) return;

  const secao = $('#secao-assuntos');

  // Cria ou reaproveita a seção de assuntos
  if (!secao) {
    criarSecaoAssuntos();
  }

  // Mostra loading
  const grid = $('#grid-assuntos');
  if (grid) {
    grid.innerHTML = `<div class="loading-wrap" aria-live="polite">
      <div class="spinner" role="status"></div>
      <span>Carregando assuntos…</span>
    </div>`;
  }

  mostrarSecao('secao-assuntos');

  try {
    const url = `${URL_API_ASSUNTOS.replace('0', estado.materiaId)}?q=${encodeURIComponent(q)}`;
    const resp = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
    const data = await resp.json();

    if (!resp.ok) throw new Error(data.erro || 'Erro ao carregar assuntos.');

    estado.assuntos = data.assuntos;
    renderizarAssuntos(data.assuntos, q);

  } catch (err) {
    const grid = $('#grid-assuntos');
    if (grid) {
      grid.innerHTML = renderAvisoEstado('⚠️', 'Erro ao carregar assuntos.', err.message);
    }
  }
}

function buscarAssuntos(q) {
  carregarAssuntos(q);
}

/* ──────────────────────────────────────────
   Renderizar grade de assuntos
   ────────────────────────────────────────── */
function criarSecaoAssuntos() {
  const main = $('#conteudo-principal');
  const html = `
    <section class="secao-assuntos" id="secao-assuntos" aria-label="Assuntos da matéria" style="display:none">
      <div class="assuntos-header">
        <div class="assuntos-titulo">
          <span id="assuntos-icone-materia"></span>
          <span class="materia-badge" id="assuntos-nome-materia"></span>
          <span style="font-size:0.85rem;color:var(--text-muted);font-weight:400">— Escolha um assunto</span>
        </div>
        <label class="busca-wrap" aria-label="Buscar assunto">
          <span class="busca-icone">🔍</span>
          <input
            type="search"
            id="input-busca"
            class="input-busca"
            placeholder="Buscar assunto…"
            autocomplete="off"
            aria-label="Buscar assunto"
          />
        </label>
      </div>
      <div class="grid-assuntos" id="grid-assuntos" role="list" aria-label="Lista de assuntos"></div>
    </section>`;
  main.insertAdjacentHTML('beforeend', html);
}

function renderizarAssuntos(assuntos, busca) {
  const grid = $('#grid-assuntos');
  const iconeEl = $('#assuntos-icone-materia');
  const nomeEl  = $('#assuntos-nome-materia');

  if (iconeEl) iconeEl.textContent = estado.materiaIcone;
  if (nomeEl)  nomeEl.textContent  = estado.materiaNome;

  if (!assuntos.length) {
    // CASO NEGATIVO: não há flashcards para aquele assunto / busca sem resultado
    const msg = busca
      ? `Nenhum assunto encontrado para <strong>"${escHtml(busca)}"</strong> em ${escHtml(estado.materiaNome)}.`
      : `Ainda não há assuntos cadastrados para <strong>${escHtml(estado.materiaNome)}</strong>.`;

    grid.innerHTML = `
      <div class="aviso-estado" role="status" aria-live="polite" style="grid-column:1/-1">
        <span class="aviso-icone">${busca ? '🔍' : '📭'}</span>
        <p>${msg}</p>
      </div>`;
    return;
  }

  grid.innerHTML = assuntos.map(a => `
    <button
      class="card-assunto"
      role="listitem"
      data-assunto-id="${a.id}"
      aria-label="${escHtml(a.nome)}, ${a.total} flashcard${a.total !== 1 ? 's' : ''}"
      type="button"
    >
      <div class="assunto-info">
        <span class="assunto-nome">${escHtml(a.nome)}</span>
        <span class="assunto-qtd">${a.total} flashcard${a.total !== 1 ? 's' : ''}</span>
      </div>
      <span class="assunto-seta">›</span>
    </button>`).join('');

  // Delegação de eventos nos cards recém-criados
  grid.querySelectorAll('.card-assunto').forEach(card => {
    card.addEventListener('click', () => selecionarAssunto(card.dataset.assuntoId));
  });
}

/* ──────────────────────────────────────────
   ETAPA 3 — Selecionar Assunto / Flashcards
   ────────────────────────────────────────── */
async function selecionarAssunto(assuntoId) {
  // Esconde visualizador anterior
  esconderSecao('secao-flashcards');

  // Mostra loading no lugar da seção de flashcards
  const main = $('#conteudo-principal');
  let secaoFlash = $('#secao-flashcards');

  if (!secaoFlash) {
    main.insertAdjacentHTML('beforeend', `
      <div id="secao-flashcards" class="secao-flashcards" aria-label="Visualizador de flashcards" style="display:none"></div>`);
    secaoFlash = $('#secao-flashcards');
  }

  secaoFlash.innerHTML = `
    <div class="painel-flash" style="border-radius:var(--radius);background:#fff;box-shadow:var(--sombra-card);padding:28px;">
      <div class="loading-wrap"><div class="spinner"></div><span>Carregando flashcards…</span></div>
    </div>`;
  mostrarSecao('secao-flashcards');
  secaoFlash.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  try {
    const url = URL_API_FLASHCARDS.replace('0', assuntoId);
    const resp = await fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } });
    const data = await resp.json();

    if (!resp.ok) {
      // CASO NEGATIVO: sem flashcards para este assunto
      secaoFlash.innerHTML = `
        <div class="painel-erro" role="alert">
          <span class="erro-icone">📭</span>
          <p>${escHtml(data.erro || 'Nenhum flashcard disponível para este assunto.')}</p>
        </div>`;
      return;
    }

    // Sucesso — atualiza estado e renderiza
    estado.assuntoId   = assuntoId;
    estado.assuntoNome = data.assunto.nome;
    estado.resumo      = data.assunto.resumo;
    estado.flashcards  = data.flashcards;
    estado.cardIndex   = 0;
    estado.virado      = false;

    renderizarVisualizador(secaoFlash, data);

  } catch (err) {
    secaoFlash.innerHTML = `
      <div class="painel-erro" role="alert">
        <span class="erro-icone">⚠️</span>
        <p>Erro ao carregar os flashcards. Tente novamente.</p>
      </div>`;
  }
}

/* ──────────────────────────────────────────
   Renderizar o visualizador de flashcards
   ────────────────────────────────────────── */
function renderizarVisualizador(container, data) {
  const total = data.flashcards.length;

  container.innerHTML = `
    <div class="flash-grid">

      <!-- Painel principal -->
      <div class="painel-flash">

        <!-- Breadcrumb + voltar -->
        <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;">
          <div class="flash-breadcrumb">
            <span>${escHtml(estado.materiaIcone)} ${escHtml(estado.materiaNome)}</span>
            <span class="sep">›</span>
            <strong>${escHtml(data.assunto.nome)}</strong>
          </div>
          <button class="btn-voltar-assuntos" id="btn-voltar-assuntos" type="button" aria-label="Voltar para a lista de assuntos">
            ‹ Voltar
          </button>
        </div>

        <!-- Barra de progresso -->
        <div class="flash-progresso" aria-label="Progresso">
          <span class="flash-progresso-texto" id="prog-texto">1 / ${total}</span>
          <div class="barra-prog-wrap" role="progressbar" aria-valuemin="0" aria-valuemax="${total}" aria-valuenow="1">
            <div class="barra-prog" id="barra-prog" style="width:${(1/total*100).toFixed(1)}%"></div>
          </div>
        </div>

        <!-- Flip card -->
        <div class="flip-area" id="flip-area" tabindex="0" role="button" aria-label="Clique para virar o card">
          <div class="flip-inner" id="flip-inner">
            <div class="flip-frente" id="flip-frente">
              <span class="flip-label">Pergunta</span>
              <p class="flip-texto" id="texto-frente">${escHtml(data.flashcards[0].frente)}</p>
              <span class="flip-dica">Clique para ver a resposta</span>
            </div>
            <div class="flip-verso" id="flip-verso">
              <span class="flip-label" style="color:rgba(255,255,255,0.5)">Resposta</span>
              <p class="flip-texto" id="texto-verso">${escHtml(data.flashcards[0].verso)}</p>
              <span class="flip-dica" style="color:rgba(255,255,255,0.4)">Clique para ver a pergunta</span>
            </div>
          </div>
        </div>

        <!-- Controles de navegação -->
        <div class="flash-controles" role="group" aria-label="Navegação entre cards">
          <button class="btn-nav" id="btn-anterior" type="button" aria-label="Card anterior" ${total <= 1 ? 'disabled' : ''}>◀</button>
          <button class="btn-virar" id="btn-virar" type="button">↕ Virar card</button>
          <button class="btn-nav" id="btn-proximo" type="button" aria-label="Próximo card" ${total <= 1 ? 'disabled' : ''}>▶</button>
        </div>

      </div><!-- fim painel-flash -->

      <!-- Painel lateral: resumo do assunto -->
      <aside class="painel-resumo" aria-label="Resumo do assunto">

        <h2 class="resumo-titulo">📋 Resumo do assunto</h2>
        <p class="resumo-assunto-nome">${escHtml(estado.materiaIcone)} ${escHtml(data.assunto.nome)}</p>
        <p class="resumo-texto">${escHtml(data.assunto.resumo)}</p>

      </aside>

    </div>`;

  // Eventos dos botões de controle
  $('#btn-anterior').addEventListener('click', voltarCard);
  $('#btn-proximo').addEventListener('click', avancarCard);
  $('#btn-virar').addEventListener('click', virarCard);
  $('#btn-voltar-assuntos').addEventListener('click', voltarParaAssuntos);
}

/* ──────────────────────────────────────────
   Controles do visualizador
   ────────────────────────────────────────── */
function virarCard() {
  const area = $('#flip-area');
  if (!area) return;

  estado.virado = !estado.virado;

  if (estado.virado) {
    area.classList.add('virado');
    area.setAttribute('aria-label', 'Clique para ver a pergunta');
  } else {
    area.classList.remove('virado');
    area.setAttribute('aria-label', 'Clique para ver a resposta');
  }
}

function avancarCard() {
  const total = estado.flashcards.length;
  if (estado.cardIndex < total - 1) {
    irParaCard(estado.cardIndex + 1);
  }
}

function voltarCard() {
  if (estado.cardIndex > 0) {
    irParaCard(estado.cardIndex - 1);
  }
}

function irParaCard(indice) {
  const total = estado.flashcards.length;
  if (indice < 0 || indice >= total) return;

  estado.cardIndex = indice;
  estado.virado = false;

  const card = estado.flashcards[indice];
  const total1based = indice + 1;

  // Atualiza textos
  const textoFrente = $('#texto-frente');
  const textoVerso  = $('#texto-verso');
  if (textoFrente) textoFrente.textContent = card.frente;
  if (textoVerso)  textoVerso.textContent  = card.verso;

  // Remove virado
  const flipArea = $('#flip-area');
  if (flipArea) {
    flipArea.classList.remove('virado');
    flipArea.setAttribute('aria-label', 'Clique para ver a resposta');
  }

  // Progresso
  const progTexto = $('#prog-texto');
  const barraProg = $('#barra-prog');
  const barraWrap = $('.barra-prog-wrap');
  if (progTexto) progTexto.textContent = `${total1based} / ${total}`;
  if (barraProg) barraProg.style.width = `${(total1based / total * 100).toFixed(1)}%`;
  if (barraWrap) barraWrap.setAttribute('aria-valuenow', total1based);

  // Botões de navegação
  const btnAnt = $('#btn-anterior');
  const btnPro = $('#btn-proximo');
  if (btnAnt) btnAnt.disabled = indice === 0;
  if (btnPro) btnPro.disabled = indice === total - 1;
}

/* ──────────────────────────────────────────
   Navegação entre seções (BDD)
   ────────────────────────────────────────── */
function voltarParaAssuntos() {
  estado.assuntoId  = null;
  estado.flashcards = [];
  estado.cardIndex  = 0;
  estado.virado     = false;
  esconderSecao('secao-flashcards');

  const secAssuntos = $('#secao-assuntos');
  if (secAssuntos) secAssuntos.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ──────────────────────────────────────────
   Helpers DOM
   ────────────────────────────────────────── */
function mostrarSecao(id) {
  const el = $(`#${id}`);
  if (el) { el.style.display = ''; el.removeAttribute('hidden'); }
}

function esconderSecao(id) {
  const el = $(`#${id}`);
  if (el) el.style.display = 'none';
}

function renderAvisoEstado(icone, titulo, detalhe = '') {
  return `
    <div class="aviso-estado" style="grid-column:1/-1" role="status">
      <span class="aviso-icone">${icone}</span>
      <p><strong>${escHtml(titulo)}</strong>${detalhe ? '<br>' + escHtml(detalhe) : ''}</p>
    </div>`;
}

function escHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}