from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..auth import decode_token
from ..database import get_db
from ..models import Cliente, ItemPedido, Pedido, Produto
from ..schemas import (
    PedidoCreate,
    PedidoResponse,
    PedidoStatusUpdate
)


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

security = HTTPBearer()


STATUS_VALIDOS = [
    "Pendente",
    "Confirmado",
    "Preparando",
    "Enviado",
    "Concluído",
    "Cancelado"
]


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


# =========================
# CRIAR PEDIDO
# =========================

@router.post(
    "/",
    response_model=PedidoResponse,
    status_code=201
)
def criar_pedido(
    dados: PedidoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    if not dados.itens:
        raise HTTPException(
            status_code=400,
            detail="O pedido precisa ter pelo menos um produto."
        )

    cliente = (
        db.query(Cliente)
        .filter(
            Cliente.id == dados.cliente_id,
            Cliente.empresa_id == empresa_id,
            Cliente.ativo == True
        )
        .first()
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado."
        )

    pedido = Pedido(
        cliente_id=cliente.id,
        empresa_id=empresa_id,
        status="Pendente",
        total=0,
        estoque_baixado=False
    )

    db.add(pedido)
    db.flush()

    total = 0

    for item in dados.itens:

        if item.quantidade <= 0:
            raise HTTPException(
                status_code=400,
                detail="A quantidade deve ser maior que zero."
            )

        produto = (
            db.query(Produto)
            .filter(
                Produto.id == item.produto_id,
                Produto.empresa_id == empresa_id,
                Produto.ativo == True
            )
            .first()
        )

        if not produto:
            raise HTTPException(
                status_code=404,
                detail=f"Produto {item.produto_id} não encontrado."
            )

        if item.quantidade > produto.estoque:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Estoque insuficiente para o produto "
                    f"'{produto.nome}'. "
                    f"Disponível: {produto.estoque}."
                )
            )

        preco = produto.preco
        subtotal = preco * item.quantidade

        novo_item = ItemPedido(
            pedido_id=pedido.id,
            produto_id=produto.id,
            quantidade=item.quantidade,
            preco_unitario=preco,
            subtotal=subtotal
        )

        db.add(novo_item)

        total += subtotal

    pedido.total = total

    db.commit()
    db.refresh(pedido)

    return pedido


# =========================
# LISTAR PEDIDOS
# =========================

@router.get(
    "/",
    response_model=list[PedidoResponse]
)
def listar_pedidos(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    pedidos = (
        db.query(Pedido)
        .filter(
            Pedido.empresa_id == empresa_id
        )
        .order_by(
            Pedido.id.desc()
        )
        .all()
    )

    return pedidos


# =========================
# BUSCAR PEDIDO
# =========================

@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse
)
def buscar_pedido(
    pedido_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    pedido = (
        db.query(Pedido)
        .filter(
            Pedido.id == pedido_id,
            Pedido.empresa_id == empresa_id
        )
        .first()
    )

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    return pedido


# =========================
# ALTERAR STATUS
# =========================

@router.put(
    "/{pedido_id}/status",
    response_model=PedidoResponse
)
def atualizar_status(
    pedido_id: int,
    dados: PedidoStatusUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    if dados.status not in STATUS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Status inválido. "
                f"Use: {', '.join(STATUS_VALIDOS)}"
            )
        )

    pedido = (
        db.query(Pedido)
        .filter(
            Pedido.id == pedido_id,
            Pedido.empresa_id == empresa_id
        )
        .first()
    )

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    # Não permite alterar pedido cancelado
    if pedido.status == "Cancelado":
        raise HTTPException(
            status_code=400,
            detail="Um pedido cancelado não pode ser alterado."
        )

    # =========================
    # CONFIRMAR PEDIDO
    # =========================

    if (
        dados.status == "Confirmado"
        and not pedido.estoque_baixado
    ):

        for item in pedido.itens:

            produto = (
                db.query(Produto)
                .filter(
                    Produto.id == item.produto_id,
                    Produto.empresa_id == empresa_id
                )
                .first()
            )

            if not produto:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Produto {item.produto_id} "
                        "não encontrado."
                    )
                )

            if item.quantidade > produto.estoque:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Estoque insuficiente para "
                        f"'{produto.nome}'. "
                        f"Disponível: {produto.estoque}."
                    )
                )

        # Só baixa o estoque depois de validar TODOS
        for item in pedido.itens:

            produto = (
                db.query(Produto)
                .filter(
                    Produto.id == item.produto_id,
                    Produto.empresa_id == empresa_id
                )
                .first()
            )

            produto.estoque -= item.quantidade

        pedido.estoque_baixado = True

    # =========================
    # CANCELAMENTO
    # =========================

    if dados.status == "Cancelado":

        # Se o estoque já foi baixado,
        # devolvemos os produtos
        if pedido.estoque_baixado:

            for item in pedido.itens:

                produto = (
                    db.query(Produto)
                    .filter(
                        Produto.id == item.produto_id,
                        Produto.empresa_id == empresa_id
                    )
                    .first()
                )

                if produto:
                    produto.estoque += item.quantidade

            pedido.estoque_baixado = False

    pedido.status = dados.status

    db.commit()
    db.refresh(pedido)

    return pedido


# =========================
# EXCLUIR PEDIDO
# =========================

@router.delete(
    "/{pedido_id}"
)
def excluir_pedido(
    pedido_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    empresa_id = obter_empresa_id(credentials)

    pedido = (
        db.query(Pedido)
        .filter(
            Pedido.id == pedido_id,
            Pedido.empresa_id == empresa_id
        )
        .first()
    )

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado."
        )

    # Se o estoque já foi baixado,
    # devolvemos antes de excluir
    if pedido.estoque_baixado:

        for item in pedido.itens:

            produto = (
                db.query(Produto)
                .filter(
                    Produto.id == item.produto_id,
                    Produto.empresa_id == empresa_id
                )
                .first()
            )

            if produto:
                produto.estoque += item.quantidade

    db.delete(pedido)

    db.commit()

    return {
        "message": "Pedido excluído com sucesso."
    }