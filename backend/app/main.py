from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from . import models

from .routers import auth
from .routers import empresas
from .routers import produtos
from .routers import clientes
from .routers import pedidos


# ==========================================
# CRIAÇÃO DAS TABELAS
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# APLICAÇÃO
# ==========================================

app = FastAPI(
    title="VendeFácil API",
    description="API do sistema VendeFácil",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# ROTAS DA API
# ==========================================

app.include_router(auth.router)

app.include_router(empresas.router)

app.include_router(produtos.router)

app.include_router(clientes.router)

app.include_router(pedidos.router)


# ==========================================
# ROTA PRINCIPAL
# ==========================================

@app.get("/")
def root():
    return {
        "message": "VendeFácil API funcionando!",
        "version": "1.0.0"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "online"
    }