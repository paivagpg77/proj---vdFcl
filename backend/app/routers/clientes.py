from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..auth import decode_token
from ..database import get_db
from ..models import Cliente
from ..schemas import (
    ClienteCreate,
    ClienteResponse,
    ClienteUpdate
)


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

security = HTTPBearer()


def obter_empresa_id(
    credentials: HTTPAuthorizationCredentials
):
    token = credentials.credentials

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado."
        )

    empresa_id = payload.get("empresa_id")

    if not empresa_id:
        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )

    return int(empresa_id)


@router.post(
    "/",
    response_model=ClienteResponse,
    status_code=201
)
def criar_cliente(
    dados: ClienteCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    cliente = Cliente(
        nome=dados.nome,
        telefone=dados.telefone,
        email=dados.email,
        cpf=dados.cpf,
        endereco=dados.endereco,
        observacoes=dados.observacoes,
        empresa_id=empresa_id
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    return cliente


@router.get(
    "/",
    response_model=list[ClienteResponse]
)
def listar_clientes(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    clientes = (
        db.query(Cliente)
        .filter(
            Cliente.empresa_id == empresa_id
        )
        .order_by(Cliente.id.desc())
        .all()
    )

    return clientes


@router.get(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def buscar_cliente(
    cliente_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    cliente = (
        db.query(Cliente)
        .filter(
            Cliente.id == cliente_id,
            Cliente.empresa_id == empresa_id
        )
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    return cliente


@router.put(
    "/{cliente_id}",
    response_model=ClienteResponse
)
def atualizar_cliente(
    cliente_id: int,
    dados: ClienteUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    cliente = (
        db.query(Cliente)
        .filter(
            Cliente.id == cliente_id,
            Cliente.empresa_id == empresa_id
        )
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    valores = dados.model_dump(
        exclude_unset=True
    )

    for campo, valor in valores.items():
        setattr(cliente, campo, valor)

    db.commit()
    db.refresh(cliente)

    return cliente


@router.delete(
    "/{cliente_id}"
)
def excluir_cliente(
    cliente_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    cliente = (
        db.query(Cliente)
        .filter(
            Cliente.id == cliente_id,
            Cliente.empresa_id == empresa_id
        )
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    db.delete(cliente)
    db.commit()

    return {
        "message": "Cliente excluído com sucesso."
    }