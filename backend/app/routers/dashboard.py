from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..auth import decode_token
from ..database import get_db
from ..models import Cliente, ItemPedido, Pedido, Produto


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
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


@router.get("/resumo")
def resumo_dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    empresa_id = obter_empresa_id(credentials)

    agora = datetime.utcnow()

    inicio_dia = datetime(
        agora.year,
        agora.month,
        agora.day
    )

    inicio_mes = datetime(
        agora.year,
        agora.month,
        1
    )

    # =========================
    # VENDAS DE HOJE
    # =========================

    vendas_hoje = (
        db.query(
            func.coalesce(
                func.sum(Pedido.total),
                0
            )
        )
        .filter(
            Pedido.empresa_id == empresa_id,
            Pedido.created_at >= inicio_dia,
            Pedido.status != "Cancelado"
        )
        .scalar()
    )

    # =========================
    # VENDAS DO MÊS
    # =========================

    vendas_mes = (
        db.query(
            func.coalesce(
                func.sum(Pedido.total),
                0
            )
        )
        .filter(
            Pedido.empresa_id == empresa_id,
            Pedido.created_at >= inicio_mes,
            Pedido.status != "Cancelado"
        )
        .scalar()
    )

    # =========================
    # PEDIDOS
    # =========================

    total_pedidos = (
        db.query(func.count(Pedido.id))
        .filter(
            Pedido.empresa_id == empresa_id
        )
        .scalar()
    )

    pedidos_pendentes = (
        db.query(func.count(Pedido.id))
        .filter(
            Pedido.empresa_id == empresa_id,
            Pedido.status == "Pendente"
        )
        .scalar()
    )

    pedidos_concluidos = (
        db.query(func.count(Pedido.id))
        .filter(
            Pedido.empresa_id == empresa_id,
            Pedido.status == "Concluído"
        )
        .scalar()
    )

    # =========================
    # CLIENTES
    # =========================

    total_clientes = (
        db.query(func.count(Cliente.id))
        .filter(
            Cliente.empresa_id == empresa_id,
            Cliente.ativo == True
        )
        .scalar()
    )

    # =========================
    # PRODUTOS
    # =========================

    total_produtos = (
        db.query(func.count(Produto.id))
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.ativo == True
        )
        .scalar()
    )

    # =========================
    # ESTOQUE BAIXO
    # =========================

    produtos_estoque_baixo = (
        db.query(func.count(Produto.id))
        .filter(
            Produto.empresa_id == empresa_id,
            Produto.ativo == True,
            Produto.estoque <= Produto.estoque_minimo
        )
        .scalar()
    )

    # =========================
    # RETORNO
    # =========================

    return {
        "vendas": {
            "hoje": float(vendas_hoje or 0),
            "mes": float(vendas_mes or 0)
        },

        "pedidos": {
            "total": total_pedidos or 0,
            "pendentes": pedidos_pendentes or 0,
            "concluidos": pedidos_concluidos or 0
        },

        "clientes": {
            "total": total_clientes or 0
        },

        "produtos": {
            "total": total_produtos or 0,
            "estoque_baixo": produtos_estoque_baixo or 0
        }
    }