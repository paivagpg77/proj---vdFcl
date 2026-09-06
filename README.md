# 🛒 VendeFácil

Sistema de gestão para pequenos negócios, desenvolvido para centralizar clientes, produtos, estoque e pedidos em uma única plataforma.

O projeto busca simplificar tarefas do dia a dia de pequenos comerciantes, oferecendo uma interface web conectada a uma API e a um banco de dados PostgreSQL.

---

## 🎯 Objetivo

O VendeFácil tem como objetivo facilitar o controle operacional de pequenos negócios.

A plataforma permite:

* Gerenciar clientes
* Cadastrar produtos
* Controlar estoque
* Registrar pedidos
* Acompanhar vendas
* Visualizar informações através de um dashboard
* Identificar produtos com estoque baixo
* Automatizar processos futuramente

---

## 🚀 Funcionalidades

### 🔐 Autenticação

* Cadastro de usuário
* Cadastro da empresa
* Login
* Autenticação utilizando JWT
* Senhas armazenadas utilizando hash
* Proteção das rotas privadas

### 👥 Clientes

* Cadastrar clientes
* Listar clientes
* Consultar clientes
* Atualizar clientes
* Excluir clientes
* Armazenar telefone, e-mail, CPF, endereço e observações

### 📦 Produtos

* Cadastrar produtos
* Listar produtos
* Consultar produtos
* Atualizar produtos
* Excluir produtos
* Controle de preço
* Controle de estoque
* Definição de estoque mínimo
* Categorias
* Identificação de produtos com estoque baixo

### 🛒 Pedidos

O módulo de pedidos está sendo desenvolvido para permitir:

* Seleção de clientes
* Seleção de produtos
* Definição de quantidades
* Cálculo automático do total
* Controle de status
* Atualização do estoque
* Validação de estoque disponível

Status planejados:

* Pendente
* Confirmado
* Preparando
* Enviado
* Concluído
* Cancelado

### 📊 Dashboard

O dashboard será responsável por apresentar informações como:

* Vendas do dia
* Vendas do mês
* Total de pedidos
* Pedidos pendentes
* Pedidos concluídos
* Total de clientes
* Total de produtos
* Produtos com estoque baixo

---

## 🧱 Arquitetura

O projeto utiliza uma arquitetura dividida em três partes principais:

```text
┌──────────────────────────────┐
│          FRONTEND            │
│        HTML / CSS / JS       │
└──────────────┬───────────────┘
               │
               │ HTTP / JSON
               ▼
┌──────────────────────────────┐
│           BACKEND            │
│       Python + FastAPI       │
└──────────────┬───────────────┘
               │
               │ SQLAlchemy
               ▼
┌──────────────────────────────┐
│         POSTGRESQL           │
│          Banco de dados      │
└──────────────────────────────┘
```

Futuramente, o projeto também poderá utilizar o **n8n** como camada de automação:

```text
Frontend
    ↓
FastAPI
    ↓
PostgreSQL
    ↓
Webhook
    ↓
n8n
    ↓
Automações
```

---

## 🛠️ Tecnologias

### Frontend

* HTML5
* CSS3
* JavaScript
* Fetch API
* LocalStorage

### Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* Pydantic
* JWT
* Passlib
* bcrypt

### Banco de dados

* PostgreSQL

### Automação futura

* n8n

---

## 📁 Estrutura do projeto

```text
VdFcl/
│
├── backend/
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   │
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── empresas.py
│   │       ├── clientes.py
│   │       ├── produtos.py
│   │       └── pedidos.py
│   │
│   ├── .env
│   ├── requirements.txt
│   └── README.md
│
└── front/
    │
    ├── index.html
    ├── login.html
    ├── cadastro.html
    ├── dashboard.html
    ├── clientes.html
    ├── produtos.html
    ├── pedidos.html
    │
    ├── css/
    │   ├── style.css
    │   ├── login.css
    │   ├── cadastro.css
    │   ├── dashboard.css
    │   ├── clientes.css
    │   ├── produtos.css
    │   └── pedidos.css
    │
    └── js/
        ├── api.js
        ├── login.js
        ├── cadastro.js
        ├── dashboard.js
        ├── clientes.js
        ├── produtos.js
        └── pedidos.js
```

---

## ⚙️ Configuração do Backend

Entre na pasta:

```bash
cd backend
```

Crie e ative o ambiente virtual:

```powershell
python -m venv venv
venv\Scripts\activate
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

---

## 🔑 Variáveis de ambiente

Crie um arquivo `.env` dentro da pasta `backend`.

Exemplo:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=SUA_SENHA
DB_NAME=vendefacil

SECRET_KEY=SUA_CHAVE_SECRETA
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

O arquivo `.env` não deve ser enviado para o GitHub.

---

## 🗄️ Banco de dados

Crie um banco PostgreSQL chamado:

```text
vendefacil
```

As tabelas são criadas pela aplicação através do SQLAlchemy.

---

## ▶️ Executando o Backend

Com o ambiente virtual ativado:

```powershell
uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

Documentação interativa:

```text
http://127.0.0.1:8000/docs
```

---

## ▶️ Executando o Frontend

Abra outro terminal.

Entre na pasta:

```powershell
cd C:\vendaFacil\VdFcl\front
```

Execute:

```powershell
python -m http.server 5500
```

O frontend ficará disponível em:

```text
http://127.0.0.1:5500
```

---

## 🔄 Execução completa

É necessário manter o backend e o frontend rodando simultaneamente.

### Terminal 1

```powershell
cd C:\vendaFacil\VdFcl\backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

### Terminal 2

```powershell
cd C:\vendaFacil\VdFcl\front
python -m http.server 5500
```

Depois acesse:

```text
http://127.0.0.1:5500
```

---

## 🔐 Fluxo de autenticação

O sistema utiliza JWT para autenticação.

```text
Cadastro
   ↓
FastAPI
   ↓
Senha transformada em hash
   ↓
PostgreSQL
```

No login:

```text
E-mail + senha
      ↓
FastAPI
      ↓
Verificação da senha
      ↓
JWT
      ↓
Frontend
      ↓
LocalStorage
```

As requisições protegidas utilizam:

```http
Authorization: Bearer TOKEN
```

---

## 🌐 CORS

Durante o desenvolvimento, o backend permite comunicação com o frontend executado na porta `5500`.

```text
Frontend
127.0.0.1:5500

        ↓

Backend
127.0.0.1:8000
```

---

## 📌 Estado atual

### Concluído

* [x] Estrutura inicial do projeto
* [x] PostgreSQL configurado
* [x] Conexão com banco
* [x] FastAPI configurado
* [x] Autenticação
* [x] Cadastro
* [x] Login
* [x] JWT
* [x] Clientes
* [x] Produtos
* [x] Controle de estoque mínimo
* [x] Frontend integrado à API
* [x] CORS configurado
* [x] Página inicial
* [x] Dashboard visual
* [x] Página de pedidos

### Em desenvolvimento

* [ ] Backend completo de pedidos
* [ ] Criação de pedidos
* [ ] Itens dos pedidos
* [ ] Atualização automática do estoque
* [ ] Alteração de status dos pedidos
* [ ] Dashboard conectado aos dados reais
* [ ] Gráficos
* [ ] Melhorias de responsividade
* [ ] Sistema de automações com n8n

---

## 🤖 Automação com n8n

Uma das próximas etapas do projeto é utilizar o n8n para automatizar tarefas.

Exemplo:

```text
Novo pedido
     ↓
FastAPI
     ↓
Evento/Webhook
     ↓
n8n
     ↓
Automação
```

O n8n será utilizado como camada de automação, enquanto o FastAPI continuará responsável pelas regras principais do sistema.

---

## 🔮 Futuras funcionalidades

Algumas funcionalidades planejadas:

* Dashboard avançado
* Relatórios
* Gráficos de vendas
* Histórico de pedidos
* Busca e filtros
* Controle financeiro
* Notificações
* Integração com WhatsApp
* Automações com n8n
* Sistema de permissões
* Multiusuário
* Deploy em produção
* Backup do banco
* Melhorias de segurança

---

## 📚 Objetivo do projeto

O VendeFácil também possui finalidade educacional e prática, permitindo aplicar conhecimentos de:

* Desenvolvimento Web
* APIs REST
* Python
* Banco de dados
* Autenticação
* JavaScript
* Arquitetura de software
* Automação
* Segurança da informação

---

## 👨‍💻 Desenvolvimento

Projeto desenvolvido como uma aplicação web de gestão para pequenos negócios.

**VendeFácil — simplificando a gestão para vender melhor.**

