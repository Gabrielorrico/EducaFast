# Bem-vindo ao EducaFast 
Esse é o manual de contribuição, do nosso projeto. Nesse documento vamos falar sobre:

- as regras de conduta do projeto.
- Como contribuir para o código do EducaFast.
- Como clonar o repositório principal.
- como executar o conjunto de testes.

EducaFast é uma aplicação web desenvolvida para facilitar, organizar e acelerar os estudos de vestibulandos, reunindo em um único ambiente diversas ferramentas essenciais para a preparação acadêmica. A plataforma foi criada com o objetivo de centralizar recursos de estudo, evitando que estudantes precisem utilizar vários aplicativos ou sites diferentes para revisar conteúdos, resolver provas antigas e acompanhar seu desempenho. 

## Regras de conduta
Antes de tudo vamos falar sobre as regras de como contribuir para o código, impondo algumas limitações para controle e um bom estruturamento do nosso projeto.
1. Não apague nenhuma funcionalidade implementada ou qualquer tipo de código complexo do projeto.

(Apagar o código de outras pessoas é primeiramente desreipeitoso e prejudicará no desenvolvimento da nossa plataforma. Tudo foi pensado com muito carinho e foi feito com muito cuidado, se está implementado é porque é uma parte importante do projeto. Aceitamos mudanças no código para melhorias de funcionalidade e uma boa experiêncida do usuário. Faça sua modificações a partir do que já faz parte do projeto.)


3. Crie uma Branch só sua para acomapanahr seu progresso e não interferir no código base antes de estar tudo pronto.

(separar as modificações que ainda estão em construção do que já está tudo certo é muito importante para organização do código e evitar problemas)


5. Não suba suas modificações sem abrir um pull request e sem a analise dos contribuidores principais.

(Isso pode levar a algum conflito no código princial ou até mesmo levar a implemnetar algo que está fora dos princípios do nosso projeto. Então, tenha cuidado antes de enviar seu código e sempre peça revisão de cada modificação, explicando o que foi feito e o seu proposito)


6. Teste modificações antes de abrir o Pull Request.

(Código não testado pode introduzir problemas. Antes de enviar qualquer mudança, rode os testes para garantir que todos passam e execute manualmente a funcionalidade no navegador. Se você adicionar uma nova feature, crie testes para ela!)


7. Documente modificações.

(Se você adicionar uma nova funcionalidade, atualize a documentação como por exemplo: README, comentários no código e etc. Se corrigir um bug complexo, explique o motivo da correção em comentários. Código sem documentação é difícil de manter e entender. Lembre-se: você está escrevendo código para que outras pessoas possam entender e dar continuidade.)


8. Divirta-se e sempre pense em formas de melhorar nossa plataforma. Isso vai ajudar muito os desenvolvedores e os usuários!

E por último e não menos importante, siga os padrões de código do projeto e sempre comunique-se com a equeipe antes de alguma grande alteração. Assim, todos ficam felizes e o projeto vai dar muito certo.

## Como contribuir para o código do EducaFast

Aqui está o passo a passo para rodar o projeto na sua máquina e começar a contribuir.

### 1. Pré-requisitos

Certifique-se de ter instalado:
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads/)
- **pip**: Gerenciador de pacotes Python (instalado com Python)

### 2. Clone o repositório
No seu ambiente de versionamento dê o seguinte comando: 
git clone https://github.com/Gabrielorrico/EducaFast.git (Essa é a URL do nosso projeto)

### 3. Crie um ambiente virtual

**Em Windows:**

Comando: python -m venv venv

depois você faz:

Comando: venv\Scripts\activate


### 4. Instale as dependências

Comando: pip install -r requirements.txt

### 5. Configure o banco de dados

Comando: python manage.py migrate


### 6. Crie um superusuário (opcional)

Para acessar o admin do Django:

Comando: python manage.py createsuperuser


### 7. Rode o servidor de desenvolvimento

Comando: python manage.py runserver

e depois acesse o localhost em algum navegadoir para visualizar.

### 8. Faça suas modificações

- Crie uma nova branch: `git checkout -b feature/nome-da-funcionalidade`
- Edite o código
- Teste localmente: `python manage.py test`
- Commit: `git commit -m "Descrição clara da mudança"`
- Push: `git push origin feature/nome-da-funcionalidade`

### 9. Abra um Pull Request

Vá até o repositório no GitHub e clique em "Compare & pull request".

(Nunca esqueça de abrir um Pull Reuquest antes de fazer uma modificação, isso faz parte das regras de conduta, ajudando na analise e no controle do código)

## Como rodar os testes automatizados

Os testes são muito importantes para garantir a qualidade e estabilidade do código. Sempre rode os testes antes de abrir um Pull Request, isso está nas regras de conduta!!

### Como executar todos os testes do projeto

Basta rodar o seguinte comando: 
python manage.py test

### Como executar testes de um app específico

Se acababou trabalhando apenas em um app, pode rodar só os testes desse app:

Aqui estão alguns exemplos de comando para apps existentes: 
python manage.py test sessaodeestudos
python manage.py test provas
python manage.py test flashcards

### O que verificar antes de enviar código

- Todos os testes passam sem erros  
- Adicionou testes para novas funcionalidades  
- Não quebrou testes existentes  
- O código roda sem erros no servidor local (é so utilizar o comando: python manage.py runserver)

## Obrigada por querer contribuir!
Esse foi o manual de contribuição do EducaFast, obrigada por querer fazer parte desse projeto tão especial. Apenas preste atenção nas regras e requsiitos do nosso projeto e aproveite bastante!

