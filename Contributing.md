# Bem-vindo ao EducaFast 
Esse é o manual de contribuição, do nosso projeto. Nesse documento vamos falar sobre:

- as regras de conduta do projeto.
- Como usar o GitHub para reportar problemas.
- Como clonar o repositório principal.
- como executar o conjunto de testes.
- Como ajudar a resolver problemas existentes.
- Como contribuir para o código do EducaFast.

EducaFast é uma aplicação web desenvolvida para facilitar, organizar e acelerar os estudos de vestibulandos, reunindo em um único ambiente diversas ferramentas essenciais para a preparação acadêmica. A plataforma foi criada com o objetivo de centralizar recursos de estudo, evitando que estudantes precisem utilizar vários aplicativos ou sites diferentes para revisar conteúdos, resolver provas antigas e acompanhar seu desempenho. 

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

(Nunca esqueça de abrir um Pull Reuquest antes de fazer uma modificação, isso ajuda na analise e no controle do código)



## Regras de conduta
## Como rodar os testes automatizados
## Como reportar problemas
## Como resolver problemas existentes


