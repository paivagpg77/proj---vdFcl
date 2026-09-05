from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routers import auth
from .routers import empresas
from .routers import produtos
from .routers import clientes


# Cria as tabelas do banco de dados
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="VendeFácil API",
    description="API do sistema VendeFácil",
    version="1.0.0"
)


# Rotas
app.include_router(auth.router)
app.include_router(empresas.router)
app.include_router(produtos.router)
app.include_router(clientes.router)


@app.get("/")
def root():
    return {
        "message": "VendeFácil API funcionando!",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "online"
    }