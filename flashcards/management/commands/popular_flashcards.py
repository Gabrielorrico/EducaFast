"""
Comando para popular o banco com dados de exemplo de flashcards.
Execute: python manage.py popular_flashcards
"""
from django.core.management.base import BaseCommand
from django.db import transaction


DADOS = [
    # ──────────────────────────────────────────────────────────────
    # MATEMÁTICA
    # ──────────────────────────────────────────────────────────────
    {
        'materia': {'nome': 'Matemática', 'icone': '📐', 'cor': '#3b82f6'},
        'assuntos': [
            {
                'nome': 'Funções do 1º Grau',
                'resumo': (
                    'Uma função do 1º grau (ou função afim) é definida por f(x) = ax + b, '
                    'onde a ≠ 0. O gráfico é sempre uma reta. '
                    'O coeficiente "a" determina a inclinação (crescente se a > 0, decrescente se a < 0) '
                    'e "b" indica onde a reta cruza o eixo y. '
                    'A raiz (zero da função) é encontrada fazendo f(x) = 0, resultando em x = -b/a.'
                ),
                'flashcards': [
                    ('O que é uma função do 1º grau?',
                     'É uma função definida por f(x) = ax + b, com a ≠ 0. Seu gráfico é uma reta oblíqua ao eixo x.'),
                    ('O que representa o coeficiente "a" em f(x) = ax + b?',
                     '"a" é o coeficiente angular (inclinação da reta). Se a > 0 a função é crescente; se a < 0, decrescente.'),
                    ('O que representa o coeficiente "b" em f(x) = ax + b?',
                     '"b" é o coeficiente linear. Indica o ponto onde a reta intercepta o eixo y (ordenada na origem).'),
                    ('Como encontrar a raiz (zero) de f(x) = ax + b?',
                     'Fazendo f(x) = 0: ax + b = 0 → x = -b/a. Esse é o ponto onde a reta corta o eixo x.'),
                    ('Dada f(x) = 2x - 6, quais são a raiz e o valor de f(0)?',
                     'Raiz: 2x - 6 = 0 → x = 3. Valor de f(0): f(0) = 2(0) - 6 = -6 (ponto -6 no eixo y).'),
                    ('Quando duas funções afins são paralelas?',
                     'Quando possuem o mesmo coeficiente angular "a" e coeficientes lineares "b" diferentes.'),
                ],
            },
            {
                'nome': 'Funções do 2º Grau',
                'resumo': (
                    'A função quadrática é definida por f(x) = ax² + bx + c, com a ≠ 0. '
                    'Seu gráfico é uma parábola: concava para cima se a > 0, para baixo se a < 0. '
                    'O vértice é o ponto de máximo ou mínimo. '
                    'As raízes são calculadas pela fórmula de Bhaskara: x = (-b ± √Δ) / 2a, onde Δ = b² - 4ac.'
                ),
                'flashcards': [
                    ('O que é uma função do 2º grau?',
                     'É f(x) = ax² + bx + c com a ≠ 0. Seu gráfico é uma parábola.'),
                    ('O que é o discriminante (Δ) de uma função quadrática?',
                     'Δ = b² - 4ac. Se Δ > 0: duas raízes reais; Δ = 0: uma raiz; Δ < 0: sem raízes reais.'),
                    ('Qual é a fórmula de Bhaskara?',
                     'x = (-b ± √Δ) / 2a, onde Δ = b² - 4ac. Usada para encontrar as raízes da equação quadrática.'),
                    ('Como encontrar o vértice da parábola f(x) = ax² + bx + c?',
                     'Xv = -b / 2a e Yv = -Δ / 4a. Se a > 0, Yv é o mínimo; se a < 0, Yv é o máximo.'),
                    ('Resolva x² - 5x + 6 = 0.',
                     'a=1, b=-5, c=6. Δ = 25-24 = 1. x = (5 ± 1)/2 → x₁ = 3 e x₂ = 2.'),
                    ('Quando a parábola abre para baixo?',
                     'Quando o coeficiente "a" é negativo (a < 0). Nesse caso, o vértice é um ponto de máximo.'),
                ],
            },
            {
                'nome': 'Probabilidade',
                'resumo': (
                    'Probabilidade mede a chance de um evento ocorrer. '
                    'P(A) = n(A) / n(Ω), onde n(A) é o número de casos favoráveis '
                    'e n(Ω) é o número total de casos possíveis do espaço amostral. '
                    'O valor de P(A) é sempre entre 0 (impossível) e 1 (certo). '
                    'Eventos complementares: P(A) + P(Ā) = 1.'
                ),
                'flashcards': [
                    ('Qual é a fórmula da probabilidade clássica?',
                     'P(A) = n(A) / n(Ω), onde n(A) = casos favoráveis e n(Ω) = total de casos possíveis.'),
                    ('O que é espaço amostral?',
                     'É o conjunto de todos os resultados possíveis de um experimento aleatório. Representado por Ω.'),
                    ('Ao lançar um dado, qual a probabilidade de sair número par?',
                     'Pares: {2,4,6} → 3 casos favoráveis. Ω = 6. P = 3/6 = 1/2 = 50%.'),
                    ('O que são eventos complementares?',
                     'São eventos em que P(A) + P(Ā) = 1. Se P(chover) = 0,3, então P(não chover) = 0,7.'),
                    ('Qual a probabilidade de tirar uma carta de copas em um baralho de 52 cartas?',
                     'Copas: 13 cartas. P = 13/52 = 1/4 = 25%.'),
                    ('O que é probabilidade condicional?',
                     'P(A|B) = P(A∩B) / P(B). É a probabilidade de A ocorrer dado que B já ocorreu.'),
                ],
            },
            {
                'nome': 'Progressão Aritmética (PA)',
                'resumo': (
                    'Uma PA é uma sequência em que a diferença entre termos consecutivos (razão r) é constante. '
                    'Termo geral: aₙ = a₁ + (n-1)·r. '
                    'Soma dos n primeiros termos: Sₙ = n·(a₁ + aₙ)/2. '
                    'Se r > 0 a PA é crescente; se r < 0 é decrescente; se r = 0 é constante.'
                ),
                'flashcards': [
                    ('O que é uma Progressão Aritmética?',
                     'É uma sequência numérica em que a diferença entre termos consecutivos (razão r) é constante.'),
                    ('Qual é a fórmula do termo geral de uma PA?',
                     'aₙ = a₁ + (n-1)·r, onde a₁ é o primeiro termo, n é a posição e r é a razão.'),
                    ('Como calcular a soma dos n primeiros termos de uma PA?',
                     'Sₙ = n·(a₁ + aₙ)/2. Ou seja, n vezes a média do primeiro e do último termo.'),
                    ('Na PA (2, 5, 8, 11, ...), qual é o 10º termo?',
                     'a₁=2, r=3. a₁₀ = 2 + (10-1)·3 = 2 + 27 = 29.'),
                    ('Qual a soma dos 10 primeiros termos da PA (2, 5, 8, ...)?',
                     'S₁₀ = 10·(2 + 29)/2 = 10·31/2 = 155.'),
                    ('O que diferencia uma PA crescente de uma decrescente?',
                     'PA crescente: r > 0. PA decrescente: r < 0. PA constante: r = 0.'),
                ],
            },
            {
                'nome': 'Geometria Plana',
                'resumo': (
                    'Geometria plana estuda figuras bidimensionais. '
                    'Principais fórmulas: '
                    'Quadrado: A = l². Retângulo: A = b·h. Triângulo: A = b·h/2. '
                    'Círculo: A = πr², C = 2πr. '
                    'Trapézio: A = (B+b)·h/2. '
                    'O Teorema de Pitágoras (a² = b² + c²) é fundamental para triângulos retângulos.'
                ),
                'flashcards': [
                    ('Qual é a área de um triângulo?',
                     'A = (base × altura) / 2. A altura deve ser perpendicular à base escolhida.'),
                    ('Qual é a fórmula da área do círculo e do comprimento da circunferência?',
                     'Área: A = πr². Comprimento (perímetro): C = 2πr, onde r é o raio.'),
                    ('Enuncie o Teorema de Pitágoras.',
                     'Em um triângulo retângulo, o quadrado da hipotenusa é igual à soma dos quadrados dos catetos: a² = b² + c².'),
                    ('Qual é a área de um trapézio?',
                     'A = (B + b) · h / 2, onde B é a base maior, b é a base menor e h é a altura.'),
                    ('Como calcular a diagonal de um quadrado de lado l?',
                     'd = l·√2. Aplicando Pitágoras: d² = l² + l² = 2l².'),
                    ('Qual a diferença entre perímetro e área?',
                     'Perímetro é a soma de todos os lados (medida de comprimento). Área é a superfície interna (medida em unidades quadradas).'),
                ],
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # PORTUGUÊS
    # ──────────────────────────────────────────────────────────────
    {
        'materia': {'nome': 'Português', 'icone': '📝', 'cor': '#ef4444'},
        'assuntos': [
            {
                'nome': 'Figuras de Linguagem',
                'resumo': (
                    'Figuras de linguagem são recursos expressivos usados para enriquecer o texto. '
                    'As mais cobradas no ENEM são: Metáfora (comparação implícita), Metonímia (substituição por relação de sentido), '
                    'Hipérbole (exagero), Ironia (dizer o contrário do que se pensa), '
                    'Personificação/Prosopopeia (atribuir características humanas a seres inanimados) e '
                    'Eufemismo (suavização de ideia desagradável).'
                ),
                'flashcards': [
                    ('O que é metáfora?',
                     'É uma comparação implícita (sem "como" ou "tal qual"). Ex: "Ele é uma raposa" (= ele é esperto).'),
                    ('Qual a diferença entre metáfora e comparação (símile)?',
                     'Comparação usa conectivo ("como", "tal qual"): "Ele é esperto como uma raposa." Metáfora é direta: "Ele é uma raposa."'),
                    ('O que é hipérbole?',
                     'É um exagero intencional para enfatizar uma ideia. Ex: "Já te pedi isso um milhão de vezes!"'),
                    ('O que é ironia?',
                     'Consiste em afirmar o contrário do que se pensa, com intenção crítica ou humorística. Ex: "Que jogada brilhante!" (após um erro).'),
                    ('O que é personificação (prosopopeia)?',
                     'Atribui características ou ações humanas a seres inanimados ou irracionais. Ex: "O vento sussurrava segredos."'),
                    ('O que é eufemismo?',
                     'Substituição de uma expressão dura por outra mais suave. Ex: "Ele passou desta para melhor" (em vez de "ele morreu").'),
                ],
            },
            {
                'nome': 'Coesão e Coerência',
                'resumo': (
                    'Coesão é a ligação gramatical entre as partes do texto, feita por conectivos, pronomes e elipses. '
                    'Coerência é a lógica e harmonia de sentido global do texto. '
                    'Um texto pode ser coeso sem ser coerente. '
                    'Conectivos importantes: adição (e, além disso), oposição (mas, porém, contudo), '
                    'causa (porque, pois), consequência (portanto, logo), concessão (embora, apesar de).'
                ),
                'flashcards': [
                    ('O que é coesão textual?',
                     'É a articulação gramatical entre os elementos do texto, por meio de conectivos, pronomes, sinônimos e elipses.'),
                    ('O que é coerência textual?',
                     'É a lógica e harmonia de sentido do texto. Um texto coerente não apresenta contradições ou ideias sem nexo.'),
                    ('Quais conectivos expressam adição?',
                     '"E", "além disso", "também", "ademais", "outrossim". Ligam ideias que se somam.'),
                    ('Quais conectivos expressam oposição/adversidade?',
                     '"Mas", "porém", "contudo", "todavia", "no entanto", "entretanto". Indicam contraste.'),
                    ('Quais conectivos expressam causa e consequência?',
                     'Causa: "porque", "pois", "visto que". Consequência: "portanto", "logo", "assim", "por isso".'),
                    ('O que são conectivos de concessão? Dê exemplos.',
                     'Introduzem uma ideia que cede terreno, mas não invalida a principal. Ex: "embora", "apesar de", "ainda que", "mesmo que".'),
                ],
            },
            {
                'nome': 'Morfologia — Classes Gramaticais',
                'resumo': (
                    'Morfologia estuda a estrutura e a classificação das palavras. '
                    'As 10 classes gramaticais são: substantivo, adjetivo, artigo, numeral, pronome, verbo, advérbio, preposição, conjunção e interjeição. '
                    'Palavras variáveis: substantivo, adjetivo, artigo, numeral, pronome, verbo. '
                    'Palavras invariáveis: advérbio, preposição, conjunção, interjeição.'
                ),
                'flashcards': [
                    ('Qual é a função do substantivo?',
                     'Nomear seres, objetos, sentimentos, lugares, ações, etc. Ex: "casa", "felicidade", "coragem".'),
                    ('Qual é a função do adjetivo?',
                     'Caracterizar ou qualificar o substantivo. Concorda em gênero e número com ele. Ex: "casa bonita", "dias frios".'),
                    ('Qual é a função do advérbio?',
                     'Modificar o verbo, o adjetivo ou outro advérbio. É invariável. Ex: "Ela fala muito bem." (muito modifica bem).'),
                    ('Qual é a diferença entre conjunção e preposição?',
                     'Conjunção liga orações ou termos de mesma função. Preposição liga termos de funções diferentes, indicando relações como posse, lugar, etc.'),
                    ('O que são pronomes relativos? Dê exemplos.',
                     'Retomam um substantivo antecedente e introduzem oração subordinada. Ex: "que", "o qual", "cujo", "onde".'),
                    ('O que são verbos de ligação? Dê exemplos.',
                     'Ligam o sujeito ao predicativo, sem indicar ação. Ex: ser, estar, parecer, ficar, permanecer, tornar-se.'),
                ],
            },
            {
                'nome': 'Interpretação de Texto',
                'resumo': (
                    'Interpretação de texto exige leitura atenta para identificar: '
                    'tema (assunto central), tese (posição defendida), argumentos (provas da tese), '
                    'intenção do autor e recursos linguísticos usados. '
                    'Diferença crucial: inferência é concluir algo a partir de pistas no texto; '
                    'extrapolação é ir além do que o texto permite — deve ser evitada.'
                ),
                'flashcards': [
                    ('Qual a diferença entre tema e tese em um texto?',
                     'Tema é o assunto abordado (ex: violência urbana). Tese é a posição/opinião defendida sobre esse tema.'),
                    ('O que é inferência em interpretação de texto?',
                     'É uma conclusão lógica obtida a partir de pistas e informações presentes no próprio texto, sem extrapolar o que está dito.'),
                    ('O que é intertextualidade?',
                     'É quando um texto faz referência a outro (cita, parafraseia ou alude). Pode ser explícita ou implícita.'),
                    ('Como identificar a ironia em um texto?',
                     'Observando contradição entre o que é dito e o contexto. O tom, a exageração e o contexto contradizem o sentido literal.'),
                    ('O que são argumentos de autoridade?',
                     'São argumentos que citam especialistas, dados estatísticos ou fontes reconhecidas para dar credibilidade à tese.'),
                    ('O que é o ponto de vista do narrador?',
                     '1ª pessoa: narrador participante. 3ª pessoa onisciente: sabe tudo. 3ª pessoa observador: conta só o que vê.'),
                ],
            },
            {
                'nome': 'Sintaxe — Sujeito e Predicado',
                'resumo': (
                    'Sintaxe analisa as relações entre as palavras na oração. '
                    'Sujeito é o termo sobre o qual se declara algo. '
                    'Predicado é o que se declara sobre o sujeito. '
                    'Sujeito pode ser: simples (um núcleo), composto (dois ou mais núcleos), '
                    'indeterminado (existe mas não é identificado) ou oração sem sujeito (verbos impessoais).'
                ),
                'flashcards': [
                    ('O que é sujeito simples?',
                     'Tem apenas um núcleo. Ex: "O aluno estudou muito." (núcleo: aluno)'),
                    ('O que é sujeito indeterminado?',
                     'O sujeito existe mas não é identificado ou o emissor não quer identificá-lo. Verbo na 3ª do plural sem agente explícito ou com "se".'),
                    ('O que são orações sem sujeito?',
                     'Orações com verbos impessoais: verbos meteorológicos (chove, troveja), "haver" no sentido de existir, "fazer" indicando tempo.'),
                    ('Qual a diferença entre predicado verbal e nominal?',
                     'Verbal: núcleo é verbo de ação. Nominal: núcleo é predicativo do sujeito (verbo de ligação + adjetivo).'),
                    ('O que é objeto direto e objeto indireto?',
                     'OD completa o verbo transitivo direto sem preposição. OI completa o verbo transitivo indireto com preposição.'),
                    ('O que é aposto?',
                     'Termo que explica, resume ou especifica outro termo. Geralmente separado por vírgulas. Ex: "João, o presidente, chegou."'),
                ],
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # BIOLOGIA
    # ──────────────────────────────────────────────────────────────
    {
        'materia': {'nome': 'Biologia', 'icone': '🧬', 'cor': '#10b981'},
        'assuntos': [
            {
                'nome': 'A Célula',
                'resumo': (
                    'A célula é a unidade básica da vida. '
                    'Células procariontes (bactérias) não possuem núcleo definido. '
                    'Células eucariontes (animais, vegetais, fungos) possuem núcleo com membrana. '
                    'Organelas importantes: mitocôndrias (respiração celular), cloroplastos (fotossíntese, só em vegetais), '
                    'ribossomos (síntese de proteínas), retículo endoplasmático (transporte) e complexo de Golgi (embalagem de proteínas).'
                ),
                'flashcards': [
                    ('Qual a diferença entre célula procarionte e eucarionte?',
                     'Procarionte: sem núcleo definido (ex: bactérias). Eucarionte: com núcleo delimitado por membrana (animais, vegetais, fungos, protistas).'),
                    ('Qual é a função das mitocôndrias?',
                     'Realizam a respiração celular aeróbica, produzindo ATP (energia) a partir da glicose e do oxigênio.'),
                    ('O que são cloroplastos e onde são encontrados?',
                     'Organelas das células vegetais responsáveis pela fotossíntese. Contêm clorofila, que absorve luz solar para produzir glicose.'),
                    ('Qual a função dos ribossomos?',
                     'Síntese de proteínas (tradução do RNA mensageiro). Presentes em células procariontes e eucariontes.'),
                    ('Qual é a função do Complexo de Golgi?',
                     'Processar, empacotar e distribuir proteínas e lipídios produzidos no retículo endoplasmático, formando vesículas de secreção.'),
                    ('O que é a membrana plasmática e qual sua função?',
                     'É uma bicamada de fosfolipídios que envolve a célula. Controla a entrada e saída de substâncias (permeabilidade seletiva).'),
                ],
            },
            {
                'nome': 'Genética Mendeliana',
                'resumo': (
                    'Genética estuda a hereditariedade. Mendel estabeleceu duas leis: '
                    '1ª Lei: Lei da segregação — cada indivíduo possui dois alelos para cada característica, que se separam na formação dos gametas. '
                    '2ª Lei: Lei da segregação independente — alelos de genes diferentes segregam-se de forma independente. '
                    'Conceitos: alelo dominante (A) sobrepõe o recessivo (a). Genótipo AA = homozigoto dominante; Aa = heterozigoto; aa = homozigoto recessivo.'
                ),
                'flashcards': [
                    ('O que são alelos dominantes e recessivos?',
                     'Dominante (A): se expressa quando presente (AA ou Aa). Recessivo (a): só se expressa em homozigose (aa).'),
                    ('O que é a 1ª Lei de Mendel?',
                     'Lei da Segregação: cada característica é controlada por dois fatores (alelos) que se separam na formação dos gametas.'),
                    ('O que é a 2ª Lei de Mendel?',
                     'Lei da Segregação Independente: alelos de genes em cromossomos diferentes segregam-se independentemente na meiose.'),
                    ('O que é fenótipo e genótipo?',
                     'Genótipo é a constituição genética (ex: Aa). Fenótipo é a expressão observável (ex: olhos castanhos).'),
                    ('No cruzamento Aa × Aa, quais são os genótipos e fenótipos esperados?',
                     'Genótipos: 25% AA, 50% Aa, 25% aa. Fenótipos: 75% dominante, 25% recessivo (proporção 3:1).'),
                    ('O que é co-dominância?',
                     'Quando ambos os alelos se expressam simultaneamente no fenótipo. Ex: grupo sanguíneo AB (alelos Iᴬ e Iᴮ são co-dominantes).'),
                ],
            },
            {
                'nome': 'Ecologia',
                'resumo': (
                    'Ecologia estuda as relações entre os seres vivos e o meio ambiente. '
                    'Cadeia alimentar: produtores → consumidores primários → secundários → decompositores. '
                    'Relações ecológicas: harmônicas (mutualismo, comensalismo, protocooperação) e '
                    'desarmônicas (predatismo, parasitismo, competição, amensalismo). '
                    'Níveis de organização: indivíduo → população → comunidade → ecossistema → biosfera.'
                ),
                'flashcards': [
                    ('O que é uma cadeia alimentar?',
                     'Sequência linear de transferência de energia: Produtores (plantas) → Consumidores primários → Secundários → Decompositores.'),
                    ('O que é mutualismo? Dê um exemplo.',
                     'Relação harmônica em que ambos os organismos se beneficiam. Ex: abelhas e flores (polinização + néctar).'),
                    ('O que é parasitismo?',
                     'Relação desarmônica em que um organismo (parasita) se beneficia às custas do outro (hospedeiro), que é prejudicado.'),
                    ('O que é nicho ecológico?',
                     'É o papel funcional de um organismo no ecossistema: o que come, como se reproduz, onde vive, como interage com outros.'),
                    ('O que são produtores em uma teia alimentar?',
                     'Organismos autotróficos (plantas, algas, cianobactérias) que produzem matéria orgânica por fotossíntese ou quimiossíntese.'),
                    ('O que é o fluxo de energia em um ecossistema?',
                     'A energia flui unidirecionalmente (não há reciclagem). A cada nível trófico, cerca de 90% da energia é perdida como calor.'),
                ],
            },
            {
                'nome': 'Evolução',
                'resumo': (
                    'A Teoria da Evolução de Darwin baseia-se na seleção natural: '
                    'indivíduos com características favoráveis ao ambiente sobrevivem e reproduzem mais. '
                    'Evidências da evolução: registros fósseis, anatomia comparada (órgãos homólogos e análogos), '
                    'embriologia comparada e biologia molecular. '
                    'Lamarck propôs uso e desuso + herança de caracteres adquiridos (teoria refutada).'
                ),
                'flashcards': [
                    ('Qual é o mecanismo central da Teoria de Darwin?',
                     'Seleção natural: indivíduos com variações hereditárias favoráveis ao ambiente sobrevivem e deixam mais descendentes.'),
                    ('O que são órgãos homólogos?',
                     'Órgãos com mesma origem embrionária mas funções diferentes. Evidenciam ancestral comum. Ex: braço humano e asa de morcego.'),
                    ('O que são órgãos análogos?',
                     'Órgãos com funções semelhantes, mas origens embrionárias diferentes. Ex: asa de inseto e asa de ave.'),
                    ('Qual foi o erro na teoria de Lamarck?',
                     'Lamarck propôs que características adquiridas durante a vida eram herdadas pelos filhos (herança de caracteres adquiridos), o que não ocorre.'),
                    ('O que é especiação?',
                     'Processo pelo qual uma população origina novas espécies, geralmente por isolamento reprodutivo (geográfico, comportamental ou genético).'),
                    ('O que são fósseis e por que são evidências da evolução?',
                     'Restos ou marcas de organismos do passado preservados em rochas. Mostram formas de vida extintas e a progressão evolutiva ao longo do tempo.'),
                ],
            },
            {
                'nome': 'Fotossíntese e Respiração',
                'resumo': (
                    'Fotossíntese: 6CO₂ + 6H₂O + luz → C₆H₁₂O₆ + 6O₂. '
                    'Ocorre nos cloroplastos de células vegetais. Fase clara (reações de luz) produz ATP e NADPH. Fase escura (Ciclo de Calvin) fixa CO₂ em glicose. '
                    'Respiração aeróbica: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 36-38 ATP. '
                    'Etapas: glicólise (citoplasma) → ciclo de Krebs (mitocôndria) → cadeia respiratória (mitocôndria).'
                ),
                'flashcards': [
                    ('Qual é a equação geral da fotossíntese?',
                     '6CO₂ + 6H₂O + energia luminosa → C₆H₁₂O₆ + 6O₂. Produz glicose e libera oxigênio.'),
                    ('Quais são as duas fases da fotossíntese?',
                     'Fase clara (fotoquímica): ocorre nas tilacoides, usa luz para produzir ATP e NADPH. Fase escura (Ciclo de Calvin): fixa CO₂ em glicose no estroma.'),
                    ('Qual é a equação geral da respiração aeróbica?',
                     'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 36-38 ATP. Ocorre nas mitocôndrias (etapas finais).'),
                    ('O que é fermentação e quando ocorre?',
                     'Respiração anaeróbica parcial, sem uso de O₂. Produz menos ATP (2 ATP). Tipos: lática (músculo) e alcoólica (leveduras).'),
                    ('Por que as folhas são verdes?',
                     'A clorofila absorve luz vermelha e azul, refletindo a luz verde. Por isso percebemos as folhas como verdes.'),
                    ('Qual a relação entre fotossíntese e respiração no planeta?',
                     'São processos complementares: fotossíntese consome CO₂ e produz O₂; respiração consome O₂ e produz CO₂, mantendo o equilíbrio atmosférico.'),
                ],
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # HISTÓRIA
    # ──────────────────────────────────────────────────────────────
    {
        'materia': {'nome': 'História', 'icone': '📜', 'cor': '#f59e0b'},
        'assuntos': [
            {
                'nome': 'Brasil Colonial',
                'resumo': (
                    'O Brasil colonial (1500-1822) foi marcado pela exploração econômica metropolitana. '
                    'Ciclos econômicos: pau-brasil, cana-de-açúcar, mineração (ouro e diamantes). '
                    'A mão de obra foi inicialmente indígena e depois africana escravizada. '
                    'A Inconfidência Mineira (1789) e a Conjuração Baiana (1798) foram movimentos de resistência. '
                    'A vinda da Família Real (1808) transformou o Brasil em sede do Império Português.'
                ),
                'flashcards': [
                    ('Quais foram os principais ciclos econômicos do Brasil Colonial?',
                     'Pau-brasil (extração de madeira), cana-de-açúcar (nordeste, séculos XVI-XVII) e mineração de ouro e diamantes em Minas Gerais (século XVIII).'),
                    ('O que foi a Inconfidência Mineira (1789)?',
                     'Movimento separatista em Minas Gerais, liderado por Tiradentes e intelectuais, contra o domínio português e a cobrança de impostos. Foi delatado e fracassou.'),
                    ('Por que a Família Real portuguesa veio para o Brasil em 1808?',
                     'Para fugir das tropas de Napoleão Bonaparte, que havia invadido Portugal. A corte de D. João VI instalou-se no Rio de Janeiro.'),
                    ('O que foi o Pacto Colonial?',
                     'Sistema econômico que obrigava a colônia a comercializar exclusivamente com a metrópole, enriquecendo Portugal e restringindo o desenvolvimento colonial.'),
                    ('Qual foi a importância do tráfico negreiro para o Brasil Colonial?',
                     'Forneceu mão de obra escravizada africana para as lavouras e minas, tornando-se pilar da economia colonial. Cerca de 4 milhões de africanos foram trazidos ao Brasil.'),
                    ('O que foi a Conjuração Baiana (1798)?',
                     'Também chamada "Revolta dos Alfaiates", foi um movimento de escravos, artesãos e militares na Bahia, com ideais iluministas e abolicionistas. Foi reprimida com execuções.'),
                ],
            },
            {
                'nome': 'Revolução Industrial',
                'resumo': (
                    'A Revolução Industrial começou na Inglaterra no século XVIII, transformando a produção artesanal em fabril. '
                    '1ª Rev. Industrial (carvão, ferro, máquina a vapor). '
                    '2ª Rev. Industrial (eletricidade, petróleo, aço, taylorismo/fordismo). '
                    '3ª Rev. Industrial / Revolução Tecnológica (automação, tecnologia da informação). '
                    'Consequências: urbanização acelerada, surgimento do proletariado, exploração do trabalho, socialismo e sindicalismo.'
                ),
                'flashcards': [
                    ('Por que a Revolução Industrial começou na Inglaterra?',
                     'A Inglaterra reunia condições únicas: reservas de carvão e ferro, capital acumulado pelo comércio, mão de obra livre (cercamentos), governo estável e domínio marítimo.'),
                    ('Quais são as características da 1ª Revolução Industrial?',
                     'Uso do carvão e ferro, invenção da máquina a vapor (Watt, 1769), mecanização têxtil, transporte ferroviário. Século XVIII na Inglaterra.'),
                    ('O que foi o taylorismo?',
                     'Sistema de organização do trabalho criado por Frederick Taylor, baseado na divisão de tarefas, cronometragem e especialização do operário para aumentar a produtividade.'),
                    ('O que foi o fordismo?',
                     'Método criado por Henry Ford: linha de montagem em série, produção padronizada em massa e salários maiores para que trabalhadores consumissem os produtos.'),
                    ('Quais foram as principais consequências sociais da Revolução Industrial?',
                     'Surgimento do proletariado urbano, exploração de mulheres e crianças, péssimas condições de trabalho, crescimento de cidades insalubres e surgimento do movimento operário.'),
                    ('O que foi o Ludismo?',
                     'Movimento de trabalhadores ingleses (luditas) que destruíam máquinas por acreditarem que a mecanização causava desemprego. Século XIX.'),
                ],
            },
            {
                'nome': 'Segunda Guerra Mundial',
                'resumo': (
                    'A 2ª Guerra Mundial (1939-1945) foi o maior conflito da história. '
                    'Causas: ascensão do fascismo e nazismo, crise de 1929, Tratado de Versalhes (1919), expansionismo alemão. '
                    'Aliados (EUA, URSS, UK, França) × Eixo (Alemanha, Itália, Japão). '
                    'Marcos: invasão da Polônia (1939), Batalha de Stalingrado (virada), Dia D (1944), bombas atômicas em Hiroshima e Nagasaki (1945). '
                    'Resultado: criação da ONU e início da Guerra Fria.'
                ),
                'flashcards': [
                    ('Quais foram as causas da Segunda Guerra Mundial?',
                     'Humilhação alemã pelo Tratado de Versalhes, Crise de 1929, ascensão do nazismo, expansionismo de Hitler e fracasso da política de apaziguamento.'),
                    ('O que foi o Tratado de Versalhes e qual seu papel na 2ª Guerra?',
                     'Tratado de 1919 que culpou a Alemanha pela 1ª Guerra, impondo reparações humilhantes. Gerou instabilidade econômica e ressentimento, favorecendo o nazismo.'),
                    ('O que foi a Batalha de Stalingrado (1942-43)?',
                     'Decisiva derrota alemã na URSS. Considerada a virada da guerra: a Alemanha perdeu 300 mil soldados e nunca mais avançou no leste.'),
                    ('O que foi o Dia D (6 de junho de 1944)?',
                     'Desembarque dos Aliados na Normandia (França), abrindo a frente ocidental. Foi a maior operação anfíbia da história, acelerando a derrota da Alemanha.'),
                    ('Por que os EUA lançaram bombas atômicas no Japão?',
                     'Para forçar a rendição japonesa sem uma invasão terrestre (que custaria milhões de vidas). Hiroshima (6/8/1945) e Nagasaki (9/8/1945). Japão capitulou em 15/8/1945.'),
                    ('O que foi o Holocausto?',
                     'Genocídio sistemático promovido pela Alemanha nazista, que exterminou cerca de 6 milhões de judeus e outros 5 milhões de pessoas (ciganos, deficientes, opositores).'),
                ],
            },
            {
                'nome': 'República Velha no Brasil',
                'resumo': (
                    'A República Velha (1889-1930) foi marcada pelo poder das oligarquias rurais. '
                    'Política do café-com-leite: alternância de poder entre São Paulo (café) e Minas Gerais (leite). '
                    'Coronelismo: domínio político local dos grandes proprietários. '
                    'Movimentos de contestação: Tenentismo, Revolta da Chibata (1910), Canudos (1896-97), Contestado (1912-16). '
                    'Terminou com a Revolução de 1930, que levou Getúlio Vargas ao poder.'
                ),
                'flashcards': [
                    ('O que foi a "política do café com leite"?',
                     'Acordo entre as oligarquias de SP e MG para alternarem a presidência da República, dominando a política durante a República Velha.'),
                    ('O que foi o coronelismo?',
                     'Prática política em que grandes proprietários rurais (coronéis) controlavam votos e cargos públicos localmente por meio de troca de favores e intimidação.'),
                    ('O que foi a Revolta de Canudos (1896-1897)?',
                     'Movimento messiânico liderado por Antônio Conselheiro no sertão baiano. Reuniu milhares de sertanejos e foi massacrado pelo exército republicano em 4 expedições.'),
                    ('O que foi o Tenentismo?',
                     'Movimento político-militar dos anos 1920 que questionava a oligarquia. Episódios: Revolta dos 18 do Forte (1922) e Coluna Prestes (1924-1927).'),
                    ('O que foi a Revolução de 1930?',
                     'Movimento que depôs o presidente Washington Luís e impediu a posse de Júlio Prestes. Levou Getúlio Vargas ao poder, encerrando a República Velha.'),
                    ('O que foi a Revolta da Chibata (1910)?',
                     'Rebelião de marinheiros negros liderada por João Cândido contra castigos físicos (chibatadas) na Marinha brasileira. Obteve vitória inicial mas foi reprimida depois.'),
                ],
            },
            {
                'nome': 'Ditadura Militar no Brasil',
                'resumo': (
                    'O regime militar brasileiro durou de 1964 a 1985. '
                    'Iniciou com o golpe que depôs João Goulart. '
                    'Marcos: AI-5 (1968) — o ato mais repressivo, fechando o Congresso e suspendendo direitos. '
                    'Resistência: guerrilha urbana, movimentos estudantis, Guerrilha do Araguaia. '
                    'Abertura gradual: Lei da Anistia (1979), eleições diretas para governadores (1982), '
                    'Diretas Já (1983-84), eleição indireta de Tancredo Neves (1985).'
                ),
                'flashcards': [
                    ('O que foi o AI-5 (1968)?',
                     'Ato Institucional nº 5: o mais duro instrumento repressivo do regime. Fechou o Congresso, suspendeu habeas corpus, permitiu cassações e tortura.'),
                    ('Quem foi deposto pelo golpe militar de 1964?',
                     'O presidente João Goulart (Jango), que propunha as "Reformas de Base" (agrária, urbana, educacional). Era visto como ameaça comunista pelos militares e setores conservadores.'),
                    ('O que foi a Guerrilha do Araguaia?',
                     'Movimento armado do PCdoB (1972-74) no sul do Pará, tentando iniciar revolução rural. Foi completamente dizimado pelo exército. Mortos e desaparecidos ainda buscados.'),
                    ('O que foi o movimento "Diretas Já" (1983-84)?',
                     'Ampla campanha popular pela eleição direta do presidente. Emenda Dante de Oliveira foi rejeitada no Congresso, mas o movimento acelerou a redemocratização.'),
                    ('O que foi a Lei da Anistia (1979)?',
                     'Lei que permitiu o retorno de exilados políticos e libertou presos políticos. Porém, também anistiou militares que cometeram crimes e torturas.'),
                    ('Como terminou o regime militar no Brasil?',
                     'Com a eleição indireta de Tancredo Neves (1985), primeiro civil após 21 anos. Tancredo morreu antes de tomar posse e José Sarney assumiu, iniciando a Nova República.'),
                ],
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # QUÍMICA
    # ──────────────────────────────────────────────────────────────
    {
        'materia': {'nome': 'Química', 'icone': '⚗️', 'cor': '#8b5cf6'},
        'assuntos': [
            {
                'nome': 'Ligações Químicas',
                'resumo': (
                    'Ligações químicas unem átomos para formar moléculas ou retículos cristalinos. '
                    'Iônica: transferência de elétrons entre metal e não-metal (ex: NaCl). '
                    'Covalente: compartilhamento de elétrons entre não-metais (ex: H₂O). '
                    'Metálica: elétrons livres entre átomos metálicos (explica condutividade e brilho). '
                    'A regra do octeto diz que átomos tendem a ter 8 elétrons na camada de valência.'
                ),
                'flashcards': [
                    ('O que é ligação iônica?',
                     'Ligação entre metal e não-metal por transferência de elétrons. O metal perde e-⁻ (cátion) e o não-metal ganha (ânion). Ex: NaCl (sal de cozinha).'),
                    ('O que é ligação covalente?',
                     'Ligação entre não-metais por compartilhamento de pares de elétrons. Forma moléculas. Ex: H₂O, CO₂, NH₃.'),
                    ('O que é ligação metálica?',
                     'Ligação entre átomos metálicos por "mar de elétrons" livres. Explica a condutividade elétrica, maleabilidade e brilho dos metais.'),
                    ('O que é a regra do octeto?',
                     'Átomos tendem a completar 8 elétrons na camada de valência (hidrogênio tende a 2), ganhando estabilidade de gás nobre.'),
                    ('O que são ligações covalentes polares e apolares?',
                     'Polar: compartilhamento desigual (diferença de eletronegatividade), gerando dipolo. Apolar: compartilhamento igual. Ex: HCl (polar), Cl₂ (apolar).'),
                    ('O que é ligação de hidrogênio?',
                     'Interação intermolecular entre H ligado a F, O ou N e outro átomo eletronegativo. É a mais forte das forças intermoleculares. Ex: água, DNA.'),
                ],
            },
            {
                'nome': 'Soluções e Concentração',
                'resumo': (
                    'Solução é a mistura homogênea de soluto (dissolvido) e solvente (dissolve). '
                    'Concentração comum: C = m/V (g/L). '
                    'Molaridade: M = n/V (mol/L), onde n = m/MM. '
                    'Solubilidade: quantidade máxima de soluto que dissolve em 100g de solvente. '
                    'Diluição: C₁V₁ = C₂V₂ (a quantidade de soluto não muda ao diluir).'
                ),
                'flashcards': [
                    ('O que é concentração comum de uma solução?',
                     'C = m/V, onde m é a massa do soluto em gramas e V é o volume da solução em litros. Unidade: g/L.'),
                    ('O que é molaridade?',
                     'M = n/V, onde n é o número de moles de soluto e V é o volume em litros. Unidade: mol/L.'),
                    ('Como calcular o número de moles?',
                     'n = m / MM, onde m é a massa em gramas e MM é a massa molar (g/mol).'),
                    ('O que é a lei da diluição?',
                     'C₁V₁ = C₂V₂. Ao diluir uma solução, a quantidade de soluto permanece constante enquanto o volume aumenta.'),
                    ('O que é solução saturada?',
                     'Solução em que o solvente dissolveu a quantidade máxima de soluto possível a uma dada temperatura. Mais soluto formaria precipitado.'),
                    ('Como a temperatura afeta a solubilidade?',
                     'Para sólidos: geralmente aumenta com a temperatura. Para gases: diminui com o aumento da temperatura (por isso refrigerante quente perde gás mais rápido).'),
                ],
            },
            {
                'nome': 'Termoquímica',
                'resumo': (
                    'Termoquímica estuda o calor trocado nas reações químicas. '
                    'Reação exotérmica: libera calor, ΔH < 0. '
                    'Reação endotérmica: absorve calor, ΔH > 0. '
                    'Lei de Hess: a variação de entalpia é a mesma independente do caminho, '
                    'dependendo apenas do estado inicial e final. '
                    'Entalpia de formação padrão: ΔH de formação de 1 mol a partir dos elementos mais estáveis.'
                ),
                'flashcards': [
                    ('O que é uma reação exotérmica?',
                     'Reação que libera energia para o ambiente (calor). ΔH < 0. Ex: combustão, respiração celular.'),
                    ('O que é uma reação endotérmica?',
                     'Reação que absorve energia do ambiente. ΔH > 0. Ex: fotossíntese, cozimento de alimentos.'),
                    ('O que é a Lei de Hess?',
                     'A variação de entalpia de uma reação é independente do caminho percorrido, dependendo apenas do estado inicial e final. Permite somar equações termoquímicas.'),
                    ('O que é entalpia de formação padrão?',
                     'Variação de entalpia na formação de 1 mol de substância a partir dos seus elementos na forma mais estável a 25°C e 1 atm.'),
                    ('Como calcular ΔH pela Lei de Hess?',
                     'Soma-se as entalpias das etapas. Se inverter uma equação, inverter o sinal de ΔH. Se multiplicar por n, multiplicar ΔH por n.'),
                    ('O que é energia de ligação?',
                     'Energia necessária para romper 1 mol de uma ligação no estado gasoso. ΔH reação = Σ(energia das ligações rompidas) - Σ(energia das ligações formadas).'),
                ],
            },
            {
                'nome': 'Eletroquímica',
                'resumo': (
                    'Eletroquímica estuda a relação entre reações químicas e energia elétrica. '
                    'Pilha (célula galvânica): reação espontânea gera corrente. Ânodo: oxidação. Cátodo: redução. '
                    'Eletrólise: corrente elétrica força reação não-espontânea. '
                    'Potencial padrão: E°célula = E°cátodo - E°ânodo. Se E° > 0, reação é espontânea. '
                    'Lei de Faraday: relaciona carga elétrica com massa depositada/liberada na eletrólise.'
                ),
                'flashcards': [
                    ('O que é oxidação e redução?',
                     'Oxidação: perda de elétrons (aumento do NOx). Redução: ganho de elétrons (diminuição do NOx). Ocorrem sempre juntas (reação redox).'),
                    ('O que é uma pilha eletroquímica?',
                     'Dispositivo que converte energia química em elétrica por reação redox espontânea. Ânodo (−): oxidação. Cátodo (+): redução.'),
                    ('O que é eletrólise?',
                     'Processo que usa corrente elétrica para forçar reações não-espontâneas. Ex: produção de alumínio, cloro e eletrodeposição (galvanoplastia).'),
                    ('Como calcular o potencial de uma pilha?',
                     'E°célula = E°cátodo − E°ânodo. Se E°célula > 0, a reação é espontânea (a pilha funciona).'),
                    ('O que enuncia a 1ª Lei de Faraday?',
                     'A massa de substância depositada ou liberada na eletrólise é proporcional à quantidade de carga elétrica (Q = i × t) que passa pelo eletrólito.'),
                    ('O que é corrosão eletroquímica?',
                     'Deterioração de metais por reação redox com o ambiente (umidade, oxigênio). O ferro enferruja quando age como ânodo em contato com água e oxigênio.'),
                ],
            },
            {
                'nome': 'Química Orgânica — Funções e Nomenclatura',
                'resumo': (
                    'Química orgânica estuda compostos de carbono. '
                    'Funções orgânicas: hidrocarbonetos (só C e H), álcoois (-OH), ácidos carboxílicos (-COOH), '
                    'aldeídos (-CHO), cetonas (-CO-), éteres (-O-), ésteres (-COO-), aminas (-NH₂). '
                    'Nomenclatura IUPAC: prefixo (nº de carbonos) + infixo (tipo de ligação) + sufixo (função). '
                    'Ex: met(1C) + an(ligação simples) + ol = metanol.'
                ),
                'flashcards': [
                    ('Quais são os prefixos IUPAC para 1 a 5 carbonos na cadeia principal?',
                     'met- (1C), et- (2C), prop- (3C), but- (4C), pent- (5C). Continuam: hex, hept, oct, non, dec.'),
                    ('Como reconhecer um álcool?',
                     'Possui grupo hidroxila (-OH) ligado a carbono saturado. Sufixo: -ol. Ex: etanol (CH₃CH₂OH).'),
                    ('Como reconhecer um ácido carboxílico?',
                     'Possui grupo -COOH (carboxila). Sufixo: -oico + ácido. Ex: ácido acético (CH₃COOH).'),
                    ('Qual a diferença entre aldeído e cetona?',
                     'Aldeído: grupo carbonila (-CHO) no carbono terminal. Cetona: grupo carbonila (-CO-) entre carbonos. Sufixos: -al e -ona.'),
                    ('O que são isômeros?',
                     'Compostos com mesma fórmula molecular mas estrutura diferente. Tipos: cadeia, posição, função, geométrica (cis-trans) e óptica (enantiômeros).'),
                    ('O que é saponificação?',
                     'Reação de um éster com base forte (NaOH ou KOH) produzindo sabão (sal de ácido graxo) e glicerol. Reação base da fabricação de sabão.'),
                ],
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # FÍSICA
    # ──────────────────────────────────────────────────────────────
    {
        'materia': {'nome': 'Física', 'icone': '⚡', 'cor': '#06b6d4'},
        'assuntos': [
            {
                'nome': 'Cinemática',
                'resumo': (
                    'Cinemática estuda o movimento sem analisar suas causas. '
                    'MRU (Movimento Retilíneo Uniforme): velocidade constante, s = s₀ + v·t. '
                    'MRUV (Movimento Retilíneo Uniformemente Variado): aceleração constante, '
                    'v = v₀ + a·t, s = s₀ + v₀·t + ½at², v² = v₀² + 2aΔs (Torricelli). '
                    'Velocidade média: Vm = Δs/Δt.'
                ),
                'flashcards': [
                    ('Qual é a equação do MRU?',
                     's = s₀ + v·t. A posição varia linearmente com o tempo. Velocidade é constante e aceleração é zero.'),
                    ('Quais são as equações do MRUV?',
                     'v = v₀ + at; s = s₀ + v₀t + ½at²; v² = v₀² + 2aΔs (Torricelli). Aceleração "a" é constante.'),
                    ('O que é velocidade escalar média?',
                     'Vm = Δs/Δt = (sf - si)/(tf - ti). É a razão entre o deslocamento e o intervalo de tempo.'),
                    ('Um carro sai do repouso com aceleração de 2 m/s². Qual sua velocidade após 5s?',
                     'v = v₀ + at = 0 + 2×5 = 10 m/s.'),
                    ('O que é aceleração? Qual a unidade SI?',
                     'Variação da velocidade por unidade de tempo: a = Δv/Δt. Unidade SI: m/s².'),
                    ('O que é queda livre?',
                     'MRUV vertical com aceleração g ≈ 10 m/s² (gravidade), sem resistência do ar. Fórmulas do MRUV com a = g.'),
                ],
            },
            {
                'nome': 'Dinâmica — Leis de Newton',
                'resumo': (
                    '1ª Lei (Inércia): um corpo em repouso permanece em repouso e em movimento permanece em movimento, a menos que uma força resultante aja sobre ele. '
                    '2ª Lei: F = m·a. A resultante de forças é proporcional à massa e à aceleração. '
                    '3ª Lei (Ação e reação): para toda ação há uma reação igual em módulo, contrária em direção e mesma reta de ação.'
                ),
                'flashcards': [
                    ('Enuncie a 1ª Lei de Newton.',
                     'Lei da Inércia: todo corpo tende a manter seu estado de repouso ou movimento retilíneo uniforme, a menos que uma força resultante não nula atue sobre ele.'),
                    ('O que diz a 2ª Lei de Newton?',
                     'F = m·a. A aceleração de um corpo é diretamente proporcional à força resultante e inversamente proporcional à sua massa.'),
                    ('Enuncie a 3ª Lei de Newton.',
                     'Para toda ação há uma reação de igual intensidade, mesma direção e sentido oposto. As forças de ação e reação atuam em corpos diferentes.'),
                    ('O que é força de atrito?',
                     'Força que se opõe ao movimento entre superfícies em contato. Fat = μ·N, onde μ é o coeficiente de atrito e N é a força normal.'),
                    ('O que é força peso e força normal?',
                     'Peso (P = mg): força gravitacional sobre o corpo. Normal (N): força perpendicular da superfície sobre o corpo, que equilibra o peso em superfícies horizontais.'),
                    ('Um bloco de 5kg sofre força de 20N. Qual sua aceleração? (desconsidere atrito)',
                     'F = ma → 20 = 5·a → a = 4 m/s².'),
                ],
            },
            {
                'nome': 'Eletrostática',
                'resumo': (
                    'Eletrostática estuda cargas elétricas em repouso. '
                    'Lei de Coulomb: F = k·|q₁·q₂|/d², onde k ≈ 9×10⁹ N·m²/C². '
                    'Campo elétrico: E = F/q (força por unidade de carga). '
                    'Potencial elétrico: V = U/q (energia por unidade de carga). '
                    'Cargas de mesmo sinal se repelem; cargas de sinais opostos se atraem.'
                ),
                'flashcards': [
                    ('O que é a Lei de Coulomb?',
                     'F = k·|q₁·q₂|/d². A força entre duas cargas é proporcional ao produto das cargas e inversamente proporcional ao quadrado da distância.'),
                    ('Qual o valor da constante eletrostática k?',
                     'k ≈ 9×10⁹ N·m²/C² no vácuo. Também escrita como k = 1/(4πε₀).'),
                    ('O que é campo elétrico?',
                     'E = F/q. É a força por unidade de carga positiva de prova. Sai de cargas positivas e entra em negativas. Unidade: N/C.'),
                    ('O que é potencial elétrico?',
                     'V = U/q = trabalho por carga. Escalar, não vetorial. A diferença de potencial (tensão) é o que move cargas em circuitos.'),
                    ('Como se dá a eletrização por atrito, contato e indução?',
                     'Atrito: troca de elétrons entre materiais. Contato: corpo carregado toca neutro, ambos ficam com mesma carga. Indução: aproximação redistribui cargas sem contato.'),
                    ('O que é o efeito das pontas em condutores?',
                     'Cargas se concentram em regiões de maior curvatura (pontas). Isso fundamenta o funcionamento do para-raios.'),
                ],
            },
            {
                'nome': 'Ondas e Óptica',
                'resumo': (
                    'Ondas: perturbações que propagam energia. Transversais (vibração ⊥ propagação, ex: luz) e longitudinais (vibração ∥ propagação, ex: som). '
                    'v = λ·f. c = 3×10⁸ m/s (luz no vácuo). '
                    'Óptica: reflexão (ângulo de incidência = ângulo de reflexão) e refração (mudança de velocidade ao mudar de meio, Lei de Snell: n₁·senθ₁ = n₂·senθ₂). '
                    'Lentes convergentes formam imagens reais (objeto além do foco).'
                ),
                'flashcards': [
                    ('Qual a equação fundamental das ondas?',
                     'v = λ · f, onde v é a velocidade da onda, λ (lambda) é o comprimento de onda e f é a frequência.'),
                    ('Qual a diferença entre onda transversal e longitudinal?',
                     'Transversal: vibração perpendicular à direção de propagação (ex: luz, ondas na corda). Longitudinal: vibração paralela (ex: som).'),
                    ('O que é o índice de refração?',
                     'n = c/v. Razão entre a velocidade da luz no vácuo e a velocidade no meio. Quanto maior n, mais o meio "freia" a luz.'),
                    ('O que é a Lei de Snell-Descartes?',
                     'n₁ · sen θ₁ = n₂ · sen θ₂. Descreve o desvio da luz ao mudar de meio (refração).'),
                    ('O que é reflexão total interna?',
                     'Ocorre quando a luz vai de meio mais denso para menos denso com ângulo maior que o crítico. Toda luz é refletida. Base das fibras ópticas.'),
                    ('Como funcionam lentes convergentes?',
                     'Convergem raios paralelos no foco. Objetos além do foco formam imagens reais e invertidas. Dentro do foco formam imagens virtuais e ampliadas (lupa).'),
                ],
            },
            {
                'nome': 'Termodinâmica',
                'resumo': (
                    'Termodinâmica estuda calor e trabalho. '
                    '0ª Lei: equilíbrio térmico (A=B e A=C → B=C). '
                    '1ª Lei: ΔU = Q - W (energia interna = calor recebido - trabalho realizado). '
                    '2ª Lei: o calor flui espontaneamente do quente para o frio; nenhuma máquina tem 100% de eficiência (Kelvin-Planck). '
                    'Ciclo de Carnot: máquina ideal com máxima eficiência η = 1 - Tf/Tq.'
                ),
                'flashcards': [
                    ('O que enuncia a 1ª Lei da Termodinâmica?',
                     'ΔU = Q - W. A variação da energia interna é igual ao calor recebido menos o trabalho realizado pelo sistema.'),
                    ('O que enuncia a 2ª Lei da Termodinâmica?',
                     'O calor flui espontaneamente do corpo mais quente para o mais frio. Nenhuma máquina térmica converte todo calor em trabalho (há perda inevitável).'),
                    ('O que é entropia?',
                     'Medida da desordem de um sistema. A 2ª Lei afirma que a entropia do universo aumenta em processos irreversíveis (tendência ao caos).'),
                    ('Qual a fórmula da eficiência de uma máquina térmica?',
                     'η = W/Qq = 1 - Qf/Qq = 1 - Tf/Tq (ciclo de Carnot). W = trabalho útil, Qq = calor fonte quente, Qf = calor cedido à fonte fria.'),
                    ('O que é um processo isotérmico?',
                     'Ocorre a temperatura constante (ΔT = 0 → ΔU = 0). Todo calor recebido é convertido em trabalho: Q = W.'),
                    ('O que é um processo adiabático?',
                     'Não há troca de calor com o meio (Q = 0). Então ΔU = -W: o sistema só troca energia via trabalho.'),
                ],
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # INGLÊS
    # ──────────────────────────────────────────────────────────────
    {
        'materia': {'nome': 'Inglês', 'icone': '🌐', 'cor': '#0ea5e9'},
        'assuntos': [
            {
                'nome': 'Simple Present',
                'resumo': (
                    'O Simple Present é usado para hábitos, fatos gerais e verdades universais. '
                    'Estrutura afirmativa: sujeito + verbo base (he/she/it acrescenta -s ou -es). '
                    'Negativa: sujeito + do/does + not + verbo base. '
                    'Interrogativa: Do/Does + sujeito + verbo base? '
                    'Advérbios de frequência: always, usually, often, sometimes, rarely, never.'
                ),
                'flashcards': [
                    ('When do we use the Simple Present?',
                     'For habits (I wake up at 7), general facts (The sun rises in the east), and scheduled events (The train leaves at 8).'),
                    ('How do we form the affirmative with he/she/it?',
                     'Add -s or -es to the verb base. Ex: He works, She watches, It goes. Irregular: have → has, be → is.'),
                    ('How do we form the negative in Simple Present?',
                     'Subject + do/does + not + verb base. Ex: I do not (don\'t) like coffee. She does not (doesn\'t) work here.'),
                    ('How do we form a question in Simple Present?',
                     'Do/Does + subject + verb base? Ex: Do you speak English? Does he live here? (Never use "does he lives")'),
                    ('What are frequency adverbs? Give examples.',
                     'Words showing how often: always (100%), usually, often, sometimes, rarely, never (0%). They go before the main verb: I always study.'),
                    ('What is the difference between "do" and "does"?',
                     '"Do" is used with I, you, we, they. "Does" is used with he, she, it. In questions and negatives only — not in affirmatives.'),
                ],
            },
            {
                'nome': 'Simple Past',
                'resumo': (
                    'O Simple Past é usado para ações concluídas no passado, em um tempo específico. '
                    'Verbos regulares: acrescentar -ed (worked, played, studied). '
                    'Verbos irregulares: forma própria (go→went, buy→bought, see→saw). '
                    'Negativa: subject + did + not + verb base. '
                    'Interrogativa: Did + subject + verb base? '
                    'Marcadores: yesterday, last week, ago, in 1990.'
                ),
                'flashcards': [
                    ('When do we use the Simple Past?',
                     'For completed actions in the past, often with a time marker. Ex: I visited Paris last year. She called me yesterday.'),
                    ('How do we form regular verbs in the Simple Past?',
                     'Add -ed: work→worked, play→played. Spelling rules: study→studied (y→ied), stop→stopped (double consonant).'),
                    ('Give 6 common irregular verbs in the Simple Past.',
                     'go→went, see→saw, buy→bought, come→came, have→had, say→said. These must be memorized individually.'),
                    ('How do we form the negative in Simple Past?',
                     'Subject + did not (didn\'t) + verb base (infinitive). Ex: I didn\'t go. She didn\'t see him. Never "didn\'t went".'),
                    ('How do we form a question in Simple Past?',
                     'Did + subject + verb base? Ex: Did you go to school? Did she call you? The main verb stays in base form.'),
                    ('What time expressions signal the Simple Past?',
                     'Yesterday, last night/week/year, ago (two days ago), in + year (in 2010), when I was a child.'),
                ],
            },
            {
                'nome': 'Modal Verbs',
                'resumo': (
                    'Modal verbs expressam possibilidade, permissão, obrigação ou habilidade. '
                    'Principais: can (habilidade/permissão), could (habilidade no passado/pedido educado), '
                    'must (obrigação forte), should (conselho), may/might (possibilidade), '
                    'will (futuro/previsão), would (condicional/pedido formal). '
                    'Regra: modal + verbo base (sem "to" e sem -s).'
                ),
                'flashcards': [
                    ('What is the structure with modal verbs?',
                     'Subject + modal + verb base (no "to", no -s). Ex: She can swim. He must leave. They should study.'),
                    ('What is the difference between "must" and "should"?',
                     '"Must" = strong obligation (You must wear a seatbelt). "Should" = advice/recommendation (You should eat healthier).'),
                    ('What is the difference between "can" and "could"?',
                     '"Can" = present ability or permission. "Could" = past ability or polite request. Ex: Could you help me, please?'),
                    ('How do we express possibility with modals?',
                     '"May" = 50% chance (It may rain). "Might" = less likely (It might snow). "Could" = also possibility (That could be true).'),
                    ('How do we form the negative with modals?',
                     'Modal + not + verb base. Ex: You must not (mustn\'t) smoke here. You should not (shouldn\'t) be late.'),
                    ('What does "would" express?',
                     'Polite requests (Would you help me?), conditional (I would travel if I had money), and past habits (We would visit grandma every Sunday).'),
                ],
            },
            {
                'nome': 'Connectives and Linking Words',
                'resumo': (
                    'Connectives (conectivos) ligam ideias e organizam o texto em inglês. '
                    'Adição: and, also, in addition, furthermore, moreover. '
                    'Contraste: but, however, although, even though, on the other hand, nevertheless. '
                    'Causa: because, since, as, due to. '
                    'Consequência: so, therefore, thus, as a result. '
                    'Conclusão: in conclusion, to sum up, finally.'
                ),
                'flashcards': [
                    ('What connectives express addition?',
                     '"And", "also", "in addition", "furthermore", "moreover". Ex: She speaks English and French. Furthermore, she knows Spanish.'),
                    ('What connectives express contrast?',
                     '"But", "however", "although", "even though", "nevertheless", "on the other hand". Ex: It was cold; however, we went out.'),
                    ('What is the difference between "although" and "however"?',
                     '"Although" connects two clauses in one sentence (Although it rained, we went). "However" starts a new sentence/clause (It rained. However, we went).'),
                    ('What connectives express cause?',
                     '"Because", "since", "as", "due to", "owing to". Ex: She stayed home because she was sick. Due to the rain, we cancelled.'),
                    ('What connectives express consequence/result?',
                     '"So", "therefore", "thus", "as a result", "consequently". Ex: He studied hard; therefore, he passed the exam.'),
                    ('What phrases are used to conclude a text?',
                     '"In conclusion", "to sum up", "to conclude", "finally", "in summary". Used in the last paragraph to summarize the main idea.'),
                ],
            },
            {
                'nome': 'Reading Comprehension Strategies',
                'resumo': (
                    'Estratégias para leitura em inglês no ENEM: '
                    'Skimming: leitura rápida para captar a ideia geral (título, primeiro e último parágrafo). '
                    'Scanning: varredura para encontrar informação específica (datas, nomes, números). '
                    'Inferência: concluir algo não dito explicitamente pelo contexto. '
                    'Palavras cognatas (parecidas com o português) ajudam; cuidado com falsos cognatos (actually = na verdade, não "atualmente").'
                ),
                'flashcards': [
                    ('What is "skimming" in reading?',
                     'Reading quickly to get the general idea of a text, without reading every word. Focus on titles, headings, first and last sentences of paragraphs.'),
                    ('What is "scanning" in reading?',
                     'Searching through a text quickly to find specific information: a name, date, number or keyword, without reading everything.'),
                    ('What are "cognates"? Give examples.',
                     'Words similar in English and Portuguese: hospital, natural, possible, important. They help understand texts without translation.'),
                    ('What are "false cognates"? Give examples.',
                     'Words that look similar but mean differently. Ex: "actually" = na verdade (not "atualmente"); "library" = biblioteca (not "livraria").'),
                    ('How do you infer meaning from context?',
                     'Use surrounding words, the topic, grammar clues and logic to deduce the meaning of unknown words without a dictionary.'),
                    ('What is the topic sentence?',
                     'The main idea of a paragraph, usually the first sentence. Identifying topic sentences in each paragraph reveals the text\'s structure.'),
                ],
            },
        ],
    },

    # ──────────────────────────────────────────────────────────────
    # GEOGRAFIA
    # ──────────────────────────────────────────────────────────────
    {
        'materia': {'nome': 'Geografia', 'icone': '🌍', 'cor': '#22c55e'},
        'assuntos': [
            {
                'nome': 'Biomas Brasileiros',
                'resumo': (
                    'O Brasil possui 6 biomas terrestres: '
                    'Amazônia (maior floresta tropical do mundo, altíssima biodiversidade), '
                    'Cerrado (savana brasileira, segundo maior bioma, berço das águas), '
                    'Mata Atlântica (muito degradada, ~12% original restante, hotspot mundial), '
                    'Caatinga (único bioma exclusivamente brasileiro, semiárido), '
                    'Pampa (extremo sul, campos gaúchos) e '
                    'Pantanal (maior planície alagável do mundo, sazonal).'
                ),
                'flashcards': [
                    ('Quais são os 6 biomas terrestres do Brasil?',
                     'Amazônia, Cerrado, Mata Atlântica, Caatinga, Pampa e Pantanal. O Brasil também possui ecossistemas costeiros como manguezais e restingas.'),
                    ('Por que o Cerrado é chamado de "berço das águas"?',
                     'Porque nele nascem importantes bacias hidrográficas brasileiras: Araguaia-Tocantins, São Francisco, Paraná e Paraguai, abastecendo grande parte do país.'),
                    ('Qual bioma é exclusivamente brasileiro?',
                     'A Caatinga. É o único bioma 100% nacional, ocorrendo apenas no Nordeste brasileiro e norte de Minas Gerais. Possui vegetação adaptada à seca.'),
                    ('Qual o estado de conservação da Mata Atlântica?',
                     'É um dos biomas mais degradados: restam apenas ~12% da cobertura original. É considerado um hotspot mundial de biodiversidade — área prioritária para conservação.'),
                    ('O que é o Pantanal e onde está localizado?',
                     'Maior planície alagável do mundo, localizado no MT e MS (Brasil), além de partes da Bolívia e Paraguai. A inundação sazonal (cheia/seca) determina sua biodiversidade única.'),
                    ('Quais são as principais ameaças aos biomas brasileiros?',
                     'Desmatamento para agropecuária, queimadas, urbanização, mineração e monocultura. A Amazônia e o Cerrado são os que mais perdem área atualmente.'),
                ],
            },
            {
                'nome': 'Climatologia',
                'resumo': (
                    'Clima é o padrão atmosférico de longo prazo de uma região; tempo é o estado momentâneo. '
                    'Fatores que influenciam o clima: latitude, altitude, maritimidade, continentalidade, correntes oceânicas e massas de ar. '
                    'Climas do Brasil: equatorial (Amazônia), tropical (Centro-Oeste/Sudeste), semiárido (Nordeste), subtropical (Sul) e tropical de altitude. '
                    'El Niño (aquece o Pacífico → seca no NE e chuvas no Sul) e La Niña (efeito inverso).'
                ),
                'flashcards': [
                    ('Qual a diferença entre clima e tempo?',
                     'Tempo: estado momentâneo da atmosfera (hoje está frio e chuvoso). Clima: padrão médio de longo prazo de uma região (>30 anos de dados).'),
                    ('O que é El Niño e quais seus efeitos no Brasil?',
                     'Aquecimento anormal das águas do Pacífico equatorial. No Brasil: seca no Nordeste e chuvas excessivas no Sul e Sudeste.'),
                    ('O que é La Niña e quais seus efeitos no Brasil?',
                     'Resfriamento das águas do Pacífico — oposto ao El Niño. No Brasil: chuvas no Nordeste e seca no Sul. Intensifica contrastes regionais.'),
                    ('O que é a ZCIT (Zona de Convergência Intertropical)?',
                     'Faixa de baixa pressão próxima ao Equador onde os ventos alísios convergem, provocando chuvas intensas. Influencia diretamente o regime de chuvas do Nordeste.'),
                    ('Quais são os fatores geográficos que influenciam o clima?',
                     'Latitude (temperatura diminui nos polos), altitude (diminui 0,6°C a cada 100m), maritimidade (oceano suaviza temperaturas), correntes oceânicas e massas de ar.'),
                    ('O que é inversão térmica e quais seus problemas?',
                     'Camada de ar quente prende o ar frio e poluído junto ao solo. Agrava a poluição urbana, causando doenças respiratórias. Comum em São Paulo no inverno.'),
                ],
            },
            {
                'nome': 'Urbanização Brasileira',
                'resumo': (
                    'O Brasil passou de país rural para urbano entre 1950-1980 (êxodo rural intenso). '
                    'Hoje mais de 85% da população vive em cidades. '
                    'Problemas urbanos: favelização, desemprego, violência, trânsito, saneamento precário. '
                    'Metropolização: crescimento das metrópoles e formação de regiões metropolitanas. '
                    'Megalópole brasileira: eixo São Paulo-Rio de Janeiro. '
                    'Cidades médias crescem como alternativa às metrópoles saturadas.'
                ),
                'flashcards': [
                    ('O que é êxodo rural e quando ocorreu no Brasil?',
                     'Migração em massa do campo para a cidade. No Brasil foi intenso entre 1950-1980, impulsionado pela mecanização agrícola e industrialização das cidades.'),
                    ('Qual o grau de urbanização do Brasil hoje?',
                     'Mais de 85% da população brasileira vive em áreas urbanas (IBGE). O Brasil é um dos países mais urbanizados do mundo, mas com urbanização desigual e periférica.'),
                    ('O que é metropolização?',
                     'Processo de crescimento e expansão das metrópoles, que absorvem municípios vizinhos formando regiões metropolitanas (ex: Grande São Paulo com 39 municípios).'),
                    ('Quais são os principais problemas das grandes cidades brasileiras?',
                     'Favelização (deficit habitacional), violência urbana, trânsito caótico, poluição, saneamento básico precário (esgoto a céu aberto) e desemprego estrutural.'),
                    ('O que é a megalópole brasileira?',
                     'Contínuo urbano entre São Paulo e Rio de Janeiro, passando por Campinas, São José dos Campos e Volta Redonda — a maior concentração urbana e econômica do Brasil.'),
                    ('O que são cidades médias e por que crescem?',
                     'Cidades de 100 mil a 500 mil habitantes que crescem como alternativa às metrópoles saturadas. Oferecem qualidade de vida, custo menor e oportunidades de emprego.'),
                ],
            },
            {
                'nome': 'Geopolítica Mundial',
                'resumo': (
                    'Geopolítica estuda as relações entre espaço geográfico e poder político. '
                    'Guerra Fria (1947-1991): bipolaridade EUA × URSS. '
                    'Nova Ordem Mundial (pós-1991): multipolaridade, protagonismo dos EUA, surgimento de novas potências (China, Índia, Brasil). '
                    'Organismos internacionais: ONU, OMC, FMI, OTAN. '
                    'BRICS: Brasil, Rússia, Índia, China e África do Sul — bloco de economias emergentes.'
                ),
                'flashcards': [
                    ('O que foi a Guerra Fria?',
                     'Disputa geopolítica, ideológica e econômica entre EUA (capitalismo) e URSS (socialismo) de 1947 a 1991. Nunca houve confronto direto, mas guerras por procuração.'),
                    ('O que é a Nova Ordem Mundial?',
                     'Configuração geopolítica pós-Guerra Fria: fim da bipolaridade, domínio momentâneo dos EUA como hiperpotência, e ascensão de novos polos como China, UE e Índia.'),
                    ('O que é o BRICS?',
                     'Bloco informal de economias emergentes: Brasil, Rússia, Índia, China e África do Sul. Representam ~40% da população mundial e buscam maior peso na geopolítica global.'),
                    ('Qual o papel da ONU no cenário geopolítico?',
                     'Organização das Nações Unidas: promover paz, segurança e cooperação internacional. O Conselho de Segurança (5 membros permanentes com veto) concentra o poder real.'),
                    ('O que é imperialismo e neocolonialismo?',
                     'Imperialismo: dominação política e militar de nações mais fortes sobre mais fracas (século XIX). Neocolonialismo: dominação econômica, comercial e cultural nos séculos XX-XXI.'),
                    ('O que são blocos econômicos regionais? Dê exemplos.',
                     'Acordos de integração econômica entre países. Ex: União Europeia (UE), Mercosul (América do Sul), NAFTA/USMCA (América do Norte), ASEAN (Sudeste Asiático).'),
                ],
            },
            {
                'nome': 'Questões Ambientais Globais',
                'resumo': (
                    'Os principais problemas ambientais globais são: '
                    'Aquecimento global (efeito estufa intensificado pelo CO₂, metano e outros gases). '
                    'Destruição da camada de ozônio (CFCs — já em recuperação após Protocolo de Montreal, 1987). '
                    'Desertificação (degradação de terras áridas e semiáridas). '
                    'Perda de biodiversidade. '
                    'Marcos: Rio-92 (Agenda 21), Protocolo de Kyoto (1997), Acordo de Paris (2015 — limitar aquecimento a 1,5°C).'
                ),
                'flashcards': [
                    ('O que é o efeito estufa e qual o problema atual?',
                     'Processo natural em que gases (CO₂, metano, vapor d\'água) retêm calor na atmosfera. O problema é sua intensificação pelo homem, causando aquecimento global.'),
                    ('Quais são os principais gases do efeito estufa?',
                     'CO₂ (queima de combustíveis fósseis), metano (pecuária e aterros), óxido nitroso (agropecuária) e CFCs (refrigeração — também destroem o ozônio).'),
                    ('O que foi o Acordo de Paris (2015)?',
                     'Tratado internacional que comprometeu quase todos os países a limitar o aquecimento global a 1,5°C acima dos níveis pré-industriais, com metas de redução de emissões.'),
                    ('O que é desertificação e onde ocorre no Brasil?',
                     'Degradação de terras áridas e semiáridas por ação humana e clima. No Brasil, afeta principalmente o semiárido nordestino (Polo de Desenvolvimento do Nordeste).'),
                    ('O que foi o Protocolo de Montreal (1987)?',
                     'Tratado que baniu os CFCs (clorofluorcarbonos), responsáveis pela destruição da camada de ozônio. Considerado um dos acordos ambientais de maior sucesso.'),
                    ('O que é a pegada ecológica?',
                     'Medida da área de terra e água necessária para sustentar o consumo de uma pessoa ou país. Países ricos têm pegada muito maior que países pobres.'),
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Popula o banco com assuntos e flashcards de exemplo para o ENEM.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpar',
            action='store_true',
            help='Remove todos os assuntos e flashcards antes de popular.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        # Imports aqui dentro evitam falhas silenciosas no carregamento do comando
        try:
            from sessaodeestudos.models import Materia  # ⚠️ ajuste se Materia estiver em outro app
        except ImportError as e:
            self.stderr.write(self.style.ERROR(
                f'Não foi possível importar Materia: {e}\n'
                'Edite a linha de import em popular_flashcards.py para apontar para o app correto.'
            ))
            return

        from flashcards.models import Assunto, Flashcard

        if options['limpar']:
            Flashcard.objects.all().delete()
            Assunto.objects.all().delete()
            self.stdout.write(self.style.WARNING('Dados anteriores removidos.'))

        total_assuntos = 0
        total_cards = 0

        for entrada in DADOS:
            dados_mat = entrada['materia']
            materia, criada = Materia.objects.get_or_create(
                nome=dados_mat['nome'],
                defaults={'icone': dados_mat['icone'], 'cor': dados_mat['cor']},
            )
            if criada:
                self.stdout.write(f'  ✔ Matéria criada: {materia.nome}')

            for i, dados_ass in enumerate(entrada['assuntos']):
                assunto, _ = Assunto.objects.get_or_create(
                    materia=materia,
                    nome=dados_ass['nome'],
                    defaults={'resumo': dados_ass['resumo'], 'ordem': i},
                )
                total_assuntos += 1

                for j, (frente, verso) in enumerate(dados_ass['flashcards']):
                    Flashcard.objects.get_or_create(
                        assunto=assunto,
                        ordem=j,
                        defaults={'frente': frente, 'verso': verso},
                    )
                    total_cards += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Concluído! {total_assuntos} assuntos e {total_cards} flashcards inseridos.'
            )
        )