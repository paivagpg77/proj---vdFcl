from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..auth import decode_token
from ..database import get_db
from ..models import Produto
from ..schemas import (
    ProdutoCreate,
    ProdutoResponse,
    ProdutoUpdate
)


router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
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
    response_model=ProdutoResponse,
    status_code=201
)
def criar_produto(
    dados: ProdutoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    if dados.preco < 0:
        raise HTTPException(
            status_code=400,
            detail="O preço não pode ser negativo."
        )

    if dados.estoque < 0:
        raise HTTPException(
            status_code=400,
            detail="O estoque não pode ser negativo."
        )

    if dados.estoque_minimo < 0:
        raise HTTPException(
            status_code=400,
            detail="O estoque mínimo não pode ser negativo."
        )

    produto = Produto(
        nome=dados.nome,
        descricao=dados.descricao,
        preco=dados.preco,
        estoque=dados.estoque,
        estoque_minimo=dados.estoque_minimo,
        categoria=dados.categoria,
        empresa_id=empresa_id
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


@router.get(
    "/",
    response_model=list[ProdutoResponse]
)
def listar_produtos(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    produtos = (
        db.query(Produto)
        .filter(
            Produto.empresa_id == empresa_id
        )
        .order_by(Produto.id.desc())
        .all()
    )

    return produtos


@router.get(
    "/{produto_id}",
    response_model=ProdutoResponse
)
def buscar_produto(
    produto_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    produto = (
        db.query(Produto)
        .filter(
            Produto.id == produto_id,
            Produto.empresa_id == empresa_id
        )
        .first()
    )

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    return produto


@router.put(
    "/{produto_id}",
    response_model=ProdutoResponse
)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    produto = (
        db.query(Produto)
        .filter(
            Produto.id == produto_id,
            Produto.empresa_id == empresa_id
        )
        .first()
    )

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    valores = dados.model_dump(
        exclude_unset=True
    )

    if "preco" in valores and valores["preco"] < 0:
        raise HTTPException(
            status_code=400,
            detail="O preço não pode ser negativo."
        )

    if "estoque" in valores and valores["estoque"] < 0:
        raise HTTPException(
            status_code=400,
            detail="O estoque não pode ser negativo."
        )

    if (
        "estoque_minimo" in valores
        and valores["estoque_minimo"] < 0
    ):
        raise HTTPException(
            status_code=400,
            detail="O estoque mínimo não pode ser negativo."
        )

    for campo, valor in valores.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto


@router.delete(
    "/{produto_id}"
)
def excluir_produto(
    produto_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    produto = (
        db.query(Produto)
        .filter(
            Produto.id == produto_id,
            Produto.empresa_id == empresa_id
        )
        .first()
    )

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    db.delete(produto)
    db.commit()

    return {
        "message": "Produto excluído com sucesso."
    }


@router.get(
    "/alertas/estoque-baixo",
    response_model=list[ProdutoResponse]
)
def estoque_baixo(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    produtos = (
        db.query(Produto)
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.ativo == True,
            Produto.estoque <= Produto.estoque_minimo
        )
        .order_by(Produto.estoque.asc())
        .all()
    )

    return produtos