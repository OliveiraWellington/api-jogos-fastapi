# API de Jogos — Python e FastAPI

## Sobre o projeto

Este projeto foi desenvolvido durante meus estudos em Análise e Desenvolvimento de Sistemas (ADS), com o objetivo de aprender na prática como criar uma API REST utilizando Python, FastAPI e MySQL.

A API trabalha com um banco de dados de jogos que já utilizo em outro projeto pessoal desenvolvido com PHP.

## Tecnologias utilizadas

- Python
- FastAPI
- MySQL
- MySQL Connector
- Swagger UI
- Git e GitHub

## Funcionalidades

- Listar os jogos cadastrados.
- Cadastrar novos jogos.
- Atualizar os dados de um jogo.
- Excluir jogos.
- Validar os dados recebidos pela API.
- Verificar se os gêneros e as produtoras informados existem no banco de dados.
- Tratar erros de jogos inexistentes e dados inválidos.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/OliveiraWellington/api-jogos-fastapi.git
```

### 2. Entrar na pasta do projeto

```bash
cd api-jogos-fastapi
```

### 3. Criar um ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 6. Configurar o banco de dados

O projeto utiliza MySQL. Para executar a API, é necessário ter o MySQL instalado e em funcionamento, além de um banco de dados chamado `bd_games` com as tabelas utilizadas pelo projeto.

A conexão está configurada no arquivo `database.py`. Caso necessário, ajuste os dados de conexão para o seu ambiente.

### 7. Executar a API

```bash
fastapi dev main.py
```

## Documentação

Com a API em execução, acesse:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

A documentação permite visualizar os endpoints e testar as requisições diretamente pelo navegador.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/jogos` | Lista os jogos |
| POST | `/jogos` | Cadastra um jogo |
| PUT | `/jogos/{jogo_id}` | Atualiza um jogo |
| DELETE | `/jogos/{jogo_id}` | Exclui um jogo |

## Objetivo de aprendizado

Com este projeto, estou praticando desenvolvimento de APIs REST, integração com banco de dados, validação de dados, tratamento de erros e organização de código Python.

Pretendo continuar evoluindo o projeto conforme avanço nos estudos e aprendo novas ferramentas e boas práticas de desenvolvimento.

---

**Desenvolvido por Wellington Oliveira**

GitHub: [OliveiraWellington](https://github.com/OliveiraWellington)