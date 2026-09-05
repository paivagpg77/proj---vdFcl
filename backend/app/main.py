from fastapi import FastAPI

from .database import Base, engine
from . import models

from .routers import auth
from .routers import empresas


# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="VendeFácil API",
    description="API do sistema VendeFácil",
    version="1.0.0"
)


# Rotas
app.include_router(auth.router)
app.include_router(empresas.router)


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