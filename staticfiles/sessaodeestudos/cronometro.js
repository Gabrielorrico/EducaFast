/**
 * EDUCAFAST — Cronômetro de Estudos
 * sessaodeestudos/static/sessaodeestudos/cronometro.js
 *
 * Funcionalidades:
 * - Selecionar matéria
 * - Iniciar, pausar, retomar e finalizar cronômetro
 * - Enviar sessão finalizada para o Django via AJAX
 * - Atualizar a lista de sessões recentes sem recarregar a página
 */

/* ============================================================
   Estado da aplicação
   ============================================================ */
const estado = {
  materiaId: null,
  materiaNome: '',
  materiaIcone: '',
  materiaCor: '',

  emAndamento: false,
  pausado: false,

  segundosAcumulados: 0,   // Total contado antes de uma pausa
  inicioAtual: null,       // Timestamp do último "Iniciar" ou "Retomar"
  intervalo: null,         // Referência do setInterval
};

/* ============================================================
   Elementos do DOM
   ============================================================ */
const elRelogio       = document.getElementById('relogio');
const elHoras         = document.getElementById('horas');
const elMinutos       = document.getElementById('minutos');
const elSegundos      = document.getElementById('segundos');
const elStatus        = document.getElementById('status-cronometro');
const elIconeMateria  = document.getElementById('icone-materia-ativa');
const elNomeMateria   = document.getElementById('nome-materia-ativa');
const elFeedback      = document.getElementById('feedback-sessao');
const elFeedbackTexto = document.getElementById('feedback-texto');
const elListaSessoes  = document.getElementById('lista-sessoes');
const elAvisoSemSessoes = document.getElementById('aviso-sem-sessoes');

const btnIniciar  = document.getElementById('btn-iniciar');
const btnPausar   = document.getElementById('btn-pausar');
const btnRetomar  = document.getElementById('btn-retomar');
const btnParar    = document.getElementById('btn-parar');

/* ============================================================
   Seleção de matéria
   ============================================================ */
document.querySelectorAll('.btn-materia').forEach(btn => {
  btn.addEventListener('click', () => {
    // Ignora clique se cronômetro estiver rodando
    if (estado.emAndamento && !estado.pausado) return;

    // Desmarca a anterior
    document.querySelectorAll('.btn-materia').forEach(b => {
      b.classList.remove('selecionada');
      b.setAttribute('aria-checked', 'false');
    });

    // Marca a selecionada
    btn.classList.add('selecionada');
    btn.setAttribute('aria-checked', 'true');

    // Atualiza o estado
    estado.materiaId    = btn.dataset.materiaId;
    estado.materiaNome  = btn.dataset.materiaNome;
    estado.materiaIcone = btn.dataset.materiaIcone;
    estado.materiaCor   = btn.dataset.materiaCor;

    // Atualiza o display
    elIconeMateria.textContent = estado.materiaIcone;
    elNomeMateria.textContent  = estado.materiaNome;

    // Habilita o botão de iniciar (somente se não estiver rodando)
    if (!estado.emAndamento) {
      btnIniciar.disabled = false;
    }
  });
});

/* ============================================================
   Formatação do tempo
   ============================================================ */
function formatarNumero(n) {
  return String(n).padStart(2, '0');
}

function atualizarDisplay(totalSegundos) {
  const h = Math.floor(totalSegundos / 3600);
  const m = Math.floor((totalSegundos % 3600) / 60);
  const s = totalSegundos % 60;

  elHoras.textContent    = formatarNumero(h);
  elMinutos.textContent  = formatarNumero(m);
  elSegundos.textContent = formatarNumero(s);

  // Atualiza o atributo datetime para acessibilidade
  elRelogio.setAttribute('datetime', `PT${h}H${m}M${s}S`);
}

function segundosDecorridos() {
  return Math.floor((Date.now() - estado.inicioAtual) / 1000);
}

function totalAtual() {
  return estado.segundosAcumulados + segundosDecorridos();
}

/* ============================================================
   Controles do cronômetro
   ============================================================ */
function iniciarCronometro() {
  if (!estado.materiaId) return;

  estado.emAndamento  = true;
  estado.pausado      = false;
  estado.inicioAtual  = Date.now();

  elStatus.textContent = '● Estudando...';
  elRelogio.classList.remove('pausado');

  // Esconde "Iniciar", mostra "Pausar" e "Finalizar"
  btnIniciar.hidden  = true;
  btnPausar.hidden   = false;
  btnPausar.disabled = false;
  btnRetomar.hidden  = true;
  btnParar.hidden    = false;
  btnParar.disabled  = false;

  // Bloqueia a seleção de matéria durante a sessão
  document.querySelectorAll('.btn-materia').forEach(b => b.style.pointerEvents = 'none');

  // Inicia o contador — atualiza a cada segundo
  estado.intervalo = setInterval(() => {
    atualizarDisplay(totalAtual());
  }, 1000);
}

function pausarCronometro() {
  if (!estado.emAndamento || estado.pausado) return;

  // Acumula o tempo decorrido até agora
  estado.segundosAcumulados += segundosDecorridos();
  estado.inicioAtual = null;

  clearInterval(estado.intervalo);
  estado.intervalo = null;
  estado.pausado = true;

  elStatus.textContent = '⏸ Pausado';
  elRelogio.classList.add('pausado');

  btnPausar.hidden  = true;
  btnRetomar.hidden = false;
  btnRetomar.disabled = false;
}

function retomarCronometro() {
  if (!estado.emAndamento || !estado.pausado) return;

  estado.pausado     = false;
  estado.inicioAtual = Date.now();

  elStatus.textContent = '● Estudando...';
  elRelogio.classList.remove('pausado');

  btnRetomar.hidden = true;
  btnPausar.hidden  = false;

  estado.intervalo = setInterval(() => {
    atualizarDisplay(totalAtual());
  }, 1000);
}

function pararCronometro() {
  if (!estado.emAndamento) return;

  // Acumula o tempo se não estiver pausado
  if (!estado.pausado && estado.inicioAtual) {
    estado.segundosAcumulados += segundosDecorridos();
  }

  clearInterval(estado.intervalo);
  estado.intervalo   = null;
  estado.emAndamento = false;
  estado.pausado     = false;

  const totalFinal = estado.segundosAcumulados;

  // Restaura display
  elStatus.textContent = 'Sessão finalizada';
  elRelogio.classList.remove('pausado');
  btnParar.disabled    = true;
  btnPausar.hidden     = true;
  btnRetomar.hidden    = true;
  btnParar.hidden      = false;

  // Reabilita seleção de matéria
  document.querySelectorAll('.btn-materia').forEach(b => b.style.pointerEvents = '');

  // Envia para o Django
  salvarSessao(estado.materiaId, totalFinal);

  // Reseta o estado interno para nova sessão
  estado.segundosAcumulados = 0;
  estado.inicioAtual = null;

  // Após 3s: restaura o botão de iniciar para nova sessão
  setTimeout(() => {
    btnIniciar.hidden   = false;
    btnIniciar.disabled = estado.materiaId ? false : true;
    btnParar.hidden     = true;
    atualizarDisplay(0);
    elStatus.textContent = 'Aguardando início';
  }, 3000);
}

/* ============================================================
   Eventos dos botões
   ============================================================ */
btnIniciar.addEventListener('click', iniciarCronometro);
btnPausar.addEventListener('click', pausarCronometro);
btnRetomar.addEventListener('click', retomarCronometro);
btnParar.addEventListener('click', pararCronometro);

/* ============================================================
   AJAX — salvar sessão no Django
   ============================================================ */
async function salvarSessao(materiaId, duracaoSegundos) {
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  try {
    const resposta = await fetch(URL_SALVAR_SESSAO, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        materia_id: materiaId,
        duracao_segundos: duracaoSegundos,
      }),
    });

    const dados = await resposta.json();

    if (dados.sucesso) {
      mostrarFeedback(`Sessão de ${dados.sessao.materia} salva! ⏱ ${dados.sessao.duracao}`);
      adicionarSessaoNaLista(dados.sessao);
    } else {
      mostrarFeedback(`Erro: ${dados.erro}`, true);
    }

  } catch (erro) {
    console.error('Erro ao salvar sessão:', erro);
    mostrarFeedback('Não foi possível salvar. Verifique sua conexão.', true);
  }
}

/* ============================================================
   UI — Feedback e atualização da lista
   ============================================================ */
function mostrarFeedback(mensagem, erro = false) {
  elFeedbackTexto.textContent = mensagem;
  elFeedback.hidden = false;
  elFeedback.style.background = erro ? '#f8d7da' : '#d4edda';
  elFeedback.style.borderColor = erro ? '#f5c6cb' : '#a3d5b0';
  elFeedback.style.color = erro ? '#721c24' : '#155724';
  elFeedback.querySelector('.feedback-icone').textContent = erro ? '❌' : '✅';

  // Esconde automaticamente após 5 segundos
  setTimeout(() => { elFeedback.hidden = true; }, 5000);
}

function adicionarSessaoNaLista(sessao) {
  // Remove aviso de lista vazia se existir
  if (elAvisoSemSessoes) elAvisoSemSessoes.remove();

  // Cria o elemento da lista
  const li = document.createElement('li');
  li.className = 'item-sessao';
  li.innerHTML = `
    <span class="sessao-icone">${sessao.icone}</span>
    <div class="sessao-info">
      <strong class="sessao-materia">${sessao.materia}</strong>
      <time class="sessao-data">${sessao.data}</time>
    </div>
    <span class="sessao-duracao">${sessao.duracao}</span>
  `;

  // Garante que a lista existe; se não, cria
  let lista = document.getElementById('lista-sessoes');
  if (!lista) {
    lista = document.createElement('ul');
    lista.id = 'lista-sessoes';
    lista.className = 'lista-sessoes';
    // Insere no card de histórico
    const cardHistorico = document.querySelector('.card-historico');
    if (cardHistorico) cardHistorico.appendChild(lista);
  }

  // Insere no topo da lista
  lista.prepend(li);

  // Mantém no máximo 5 itens visíveis
  const itens = lista.querySelectorAll('.item-sessao');
  if (itens.length > 5) itens[itens.length - 1].remove();
}

/* ============================================================
   Inicialização
   ============================================================ */
// Garante que os botões começam no estado correto
btnPausar.hidden  = true;
btnRetomar.hidden = true;
btnParar.hidden   = true;
atualizarDisplay(0);
