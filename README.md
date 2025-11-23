# Entrega Ágil - Backend API


System: PostgreSQL

Server: entrega_postgres

Username: entrega

Password: entrega123

Database: entrega_db


# 📦 Entrega Ágil — Backend API  
Sistema inteligente para gestão de encomendas com OCR e notificações automatizadas.  
Backend desenvolvido em **FastAPI + PostgreSQL + Docker**.

---

# 🏗️ Arquitetura Geral do Projeto

O backend roda dentro de uma arquitetura baseada em **3 containers principais**, cada um com uma responsabilidade específica:

## 1️⃣ PostgreSQL (`entrega_postgres`)
- Banco de dados principal do sistema
- Armazena:
  - usuários
  - encomendas
  - notificações
  - logs de OCR
- Porta exposta: **5432**
- Volume persistente: `./database`  
  (não versionado no GitHub — ignorado pelo `.gitignore`)

## 2️⃣ Adminer (`entrega_adminer`)
- Interface web para acessar o banco de dados
- Permite visualizar tabelas, editar dados e executar SQL
- Acessível em:  
  **http://<seu-ip>:8080**

## 3️⃣ Backend FastAPI (`entrega_backend`)
- API principal do sistema
- Linguagem: **Python 3.12**
- Framework: **FastAPI**
- ORM: **SQLAlchemy**
- Porta exposta: **8000**
- Rotas disponíveis em:  
  **http://<seu-ip>:8000/docs**

---

# 📁 Estrutura de Diretórios

/app
├── backend
│ ├── app
│ │ ├── main.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── validators.py
│ │ ├── database.py
│ ├── requirements.txt
│ ├── Dockerfile
├── docker-compose.yml
├── README.md
├── .gitignore




---

# 📌 Descrição dos Arquivos Importantes

## 🐍 `/backend/app/main.py`
Arquivo PRINCIPAL da API FastAPI.

Contém:
- inicialização da aplicação
- conexão com o banco
- endpoints:
  - `/` → status da API  
  - `/usuarios` → cadastro de usuários  
  - `/encomendas` → cadastro manual de encomendas  
  - `/encomendas/pendentes` → listar pendentes  
  - `/encomendas/{id}/retirar` → marcar retirada  

---

## 🗂️ `/backend/app/models.py`
Modelos de banco de dados (SQLAlchemy):

- `Usuario`:  
  nome, cpf_cnpj (único), apartamento, bloco, telefone, e-mail  

- `Encomenda`:  
  recebe usuário_id, data_recebimento, data_retirada, status  
  (pendente/retirada)

- `Notificacao`:  
  registra histórico de notificações enviadas

- `LogOCR`:  
  salva informações sobre resultados do OCR

---

## 📦 `/backend/app/schemas.py`
Modelos de entrada/saída (Pydantic):

- `UsuarioCreate`, `UsuarioRead`
- `EncomendaCreate`, `EncomendaRead`, `EncomendaList`

São usados no Swagger e na validação da API.

---

## 🧠 `/backend/app/validators.py`
Validador de CPF/CNPJ:

- remove máscara  
- valida dígitos verificadores  
- aceita automaticamente CPF ou CNPJ  

---

## 🔧 `/backend/app/database.py`
Gerencia:

- engine do SQLAlchemy  
- SessionLocal  
- criação das tabelas  

---

## 🐳 `/backend/Dockerfile`
Define a imagem do backend:

- Python 3.12  
- instala dependências  
- copia código  
- executa uvicorn  

---

## 🧩 `docker-compose.yml`
Orquestra os 3 containers:

- Postgres
- Adminer
- Backend FastAPI

E cria a rede interna `entrega_net`.

---

# 🚀 Como rodar o sistema

Dentro da pasta `/app`:

```bash
docker compose up -d --build

Verificar containers ativos:

docker ps
