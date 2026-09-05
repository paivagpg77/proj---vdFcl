# 🛒 VendeFácil

Sistema de gestão e automação para pequenos negócios, desenvolvido com o objetivo de centralizar **clientes, produtos, estoque, pedidos e informações de vendas** em uma única plataforma.

O VendeFácil possui uma API REST desenvolvida em **Python + FastAPI**, utilizando **PostgreSQL** como banco de dados e autenticação baseada em **JWT**.

---

## 📌 Sobre o projeto

O VendeFácil foi criado para facilitar o gerenciamento de pequenos negócios que precisam controlar suas operações de forma simples e organizada.

A plataforma permite:

* 👥 Gerenciar clientes
* 📦 Gerenciar produtos
* 📊 Controlar estoque
* 🛒 Criar e gerenciar pedidos
* 💰 Calcular automaticamente o valor dos pedidos
* ⚠️ Identificar produtos com estoque baixo
* 🔐 Realizar cadastro e login de usuários
* 🏢 Separar os dados de cada empresa
* 📈 Consultar informações para o dashboard

---

## 🚀 Tecnologias utilizadas

### Backend

* **Python 3.12**
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **psycopg2**
* **Pydantic**
* **JWT**
* **Passlib**
* **Uvicorn**
* **python-dotenv**

### Frontend

O frontend será desenvolvido utilizando:

* HTML5
* CSS3
* JavaScript
* Fetch API

---

## 🏗️ Arquitetura

O projeto está organizado separando o backend da aplicação:

```text
VendeFacil/
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
│   │       ├── produtos.py
│   │       ├── clientes.py
│   │       ├── pedidos.py
│   │       └── dashboard.py
│   │
│   ├── .env
│   ├── requirements.txt
│   └── README.md
│
└── frontend/
    └── Em desenvolvimento
```

---

# 🔐 Autenticação

O sistema utiliza **JWT (JSON Web Token)** para autenticar os usuários.

O fluxo de autenticação funciona da seguinte forma:

```text
Cadastro
   ↓
Usuário + Empresa
   ↓
Login
   ↓
JWT
   ↓
Acesso às rotas protegidas
```

Cada token possui informações que permitem identificar:

* Usuário
* Empresa

Isso permite que cada empresa tenha acesso somente aos seus próprios dados.

---

# 🏢 Empresas

Cada usuário cadastrado está associado a uma empresa.

As informações da empresa incluem:

* Nome
* CNPJ
* Telefone
* E-mail

Endpoint disponível:

```http
GET /empresas/minha-empresa
```

---

# 👥 Clientes

O sistema possui CRUD completo para clientes.

Cada cliente pode possuir:

* Nome
* Telefone
* E-mail
* CPF
* Endereço
* Observações
* Status ativo/inativo

### Endpoints

```http
POST   /clientes/
GET    /clientes/
GET    /clientes/{cliente_id}
PUT    /clientes/{cliente_id}
DELETE /clientes/{cliente_id}
```

---

# 📦 Produtos

O gerenciamento de produtos permite controlar informações como:

* Nome
* Descrição
* Preço
* Estoque
* Estoque mínimo
* Categoria
* Status

### Endpoints

```http
POST   /produtos/
GET    /produtos/
GET    /produtos/{produto_id}
PUT    /produtos/{produto_id}
DELETE /produtos/{produto_id}
```

Também existe uma rota para identificar produtos que estão com estoque baixo:

```http
GET /produtos/alertas/estoque-baixo
```

Um produto é considerado com estoque baixo quando:

```text
estoque <= estoque_minimo
```

---

# 🛒 Pedidos

O módulo de pedidos conecta clientes e produtos.

Um pedido possui:

* Cliente
* Produtos
* Quantidades
* Preço unitário
* Subtotal
* Total
* Status
* Data de criação

### Status disponíveis

```text
Pendente
Confirmado
Preparando
Enviado
Concluído
Cancelado
```

### Endpoints

```http
POST   /pedidos/
GET    /pedidos/
GET    /pedidos/{pedido_id}
PUT    /pedidos/{pedido_id}/status
DELETE /pedidos/{pedido_id}
```

---

# 📊 Controle automático de estoque

O sistema possui integração entre pedidos e estoque.

Quando um pedido passa para:

```text
Confirmado
```

o sistema verifica se existe estoque suficiente.

Caso exista:

```text
Estoque atual
      ↓
Quantidade do pedido
      ↓
Novo estoque
```

Por exemplo:

```text
Produto: Camiseta
Estoque: 20

Pedido: 3 unidades

Novo estoque:
20 - 3 = 17
```

O sistema também evita que o estoque seja descontado novamente caso o pedido seja atualizado posteriormente.

---

# 🔄 Cancelamento de pedidos

Caso um pedido confirmado seja cancelado, os produtos que haviam sido retirados do estoque são devolvidos.

Exemplo:

```text
Estoque antes:
20

Pedido confirmado:
- 3

Estoque:
17

Pedido cancelado:
+ 3

Estoque novamente:
20
```

---

# 📈 Dashboard

O sistema possui uma API específica para fornecer informações para o dashboard.

Endpoint:

```http
GET /dashboard/resumo
```

Atualmente fornece:

### Vendas

* Vendas do dia
* Vendas do mês

### Pedidos

* Total de pedidos
* Pedidos pendentes
* Pedidos concluídos

### Clientes

* Total de clientes ativos

### Produtos

* Total de produtos ativos
* Produtos com estoque baixo

Exemplo de resposta:

```json
{
  "vendas": {
    "hoje": 0,
    "mes": 0
  },
  "pedidos": {
    "total": 0,
    "pendentes": 0,
    "concluidos": 0
  },
  "clientes": {
    "total": 0
  },
  "produtos": {
    "total": 0,
    "estoque_baixo": 0
  }
}
```

---

# 🗄️ Banco de dados

O projeto utiliza **PostgreSQL**.

Principais tabelas:

```text
empresas
   │
   ├── usuarios
   ├── produtos
   ├── clientes
   └── pedidos
           │
           └── itens_pedido
```

### Empresas

Armazena os dados das empresas cadastradas.

### Usuários

Armazena os usuários responsáveis pelo acesso ao sistema.

### Produtos

Armazena produtos e informações de estoque.

### Clientes

Armazena os clientes das empresas.

### Pedidos

Armazena os pedidos realizados.

### Itens do pedido

Relaciona os produtos aos pedidos.

---

# ⚙️ Configuração

## 1. Clonar o projeto

```bash
git clone https://github.com/seu-usuario/vendefacil.git
```

Entre na pasta:

```bash
cd vendefacil/backend
```

---

## 2. Criar ambiente virtual

No Windows:

```powershell
python -m venv venv
```

Ative:

```powershell
venv\Scripts\activate
```

---

## 3. Instalar dependências

```powershell
pip install -r requirements.txt
```

---

## 4. Configurar o PostgreSQL

Crie um banco de dados chamado:

```text
vendefacil
```

Depois configure o arquivo `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=SUA_SENHA
DB_NAME=vendefacil

SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> ⚠️ O arquivo `.env` não deve ser enviado para o GitHub. Adicione `.env` ao `.gitignore`.

---

# ▶️ Executando o projeto

Com o ambiente virtual ativado:

```powershell
uvicorn app.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

---

# 📚 Documentação da API

O FastAPI gera automaticamente a documentação utilizando Swagger.

Acesse:

```text
http://127.0.0.1:8000/docs
```

Também existe a documentação alternativa:

```text
http://127.0.0.1:8000/redoc
```

---

# ❤️ Health Check

Para verificar se a API está funcionando:

```http
GET /health
```

Resposta:

```json
{
  "status": "online"
}
```

---

# 🧪 Fluxo para testar a API

Uma sequência recomendada para testar o sistema:

```text
1. Cadastro
      ↓
2. Login
      ↓
3. Copiar JWT
      ↓
4. Autorizar no Swagger
      ↓
5. Criar cliente
      ↓
6. Criar produto
      ↓
7. Criar pedido
      ↓
8. Confirmar pedido
      ↓
9. Verificar estoque
      ↓
10. Consultar dashboard
```

---

# 🔒 Segurança

O projeto possui algumas medidas básicas de segurança:

* Autenticação utilizando JWT
* Senhas armazenadas com hash
* Rotas protegidas
* Separação dos dados por empresa
* Validação através do Pydantic
* Verificação de estoque
* Proteção contra acesso a dados de outra empresa

---

# 🛣️ Roadmap

## ✅ Backend

* [x] Configuração do PostgreSQL
* [x] Conexão com banco de dados
* [x] Cadastro
* [x] Login
* [x] JWT
* [x] Empresas
* [x] Produtos
* [x] Estoque
* [x] Clientes
* [x] Pedidos
* [x] Controle automático de estoque
* [x] Dashboard básico

## 🚧 Frontend

* [ ] Página inicial
* [ ] Cadastro
* [ ] Login
* [ ] Dashboard
* [ ] Página de clientes
* [ ] Página de produtos
* [ ] Página de pedidos
* [ ] Página de estoque
* [ ] Integração com a API

## 🔮 Futuro

* [ ] Relatórios
* [ ] Gráficos de vendas
* [ ] Histórico de pedidos
* [ ] Sistema de notificações
* [ ] Automação de atendimento
* [ ] Integração com WhatsApp
* [ ] Integração com pagamentos
* [ ] Controle financeiro
* [ ] Multiusuário
* [ ] Permissões de acesso
* [ ] Deploy em produção

---

# 🎯 Objetivo

O objetivo do VendeFácil é criar uma plataforma simples e acessível para ajudar pequenos negócios a:

* Organizar clientes
* Controlar produtos
* Controlar estoque
* Gerenciar pedidos
* Acompanhar vendas
* Automatizar tarefas
* Tomar decisões através de dados

---

# 👨‍💻 Desenvolvimento

Projeto desenvolvido como aplicação prática de desenvolvimento de sistemas, envolvendo:

* Desenvolvimento Backend
* APIs REST
* Banco de dados
* Autenticação
* Modelagem de dados
* CRUD
* Controle de estoque
* Integração entre entidades
* Desenvolvimento Frontend

---

## 📄 Licença

Este projeto está em desenvolvimento e pode receber novas funcionalidades e melhorias ao longo do tempo.
