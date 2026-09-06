from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from sqlalchemy.orm import Session

from ..auth import decode_token
from ..database import get_db
from ..models import (
    Pedido,
    ItemPedido,
    Cliente,
    Produto
)

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


# ==========================================
# CRIAR PEDIDO
# ==========================================

@router.post(
    "/",
    response_model=PedidoResponse,
    status_code=status.HTTP_201_CREATED
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

    # --------------------------------------
    # Verifica cliente
    # --------------------------------------

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

    # --------------------------------------
    # Evita produto duplicado
    # --------------------------------------

    produtos_ids = [
        item.produto_id
        for item in dados.itens
    ]

    if len(produtos_ids) != len(set(produtos_ids)):
        raise HTTPException(
            status_code=400,
            detail="Não é permitido repetir o mesmo produto no pedido."
        )

    # --------------------------------------
    # Cria pedido inicialmente
    # --------------------------------------

    pedido = Pedido(
        cliente_id=dados.cliente_id,
        empresa_id=empresa_id,
        total=0,
        status="Pendente",
        estoque_baixado=False
    )

    db.add(pedido)

    db.flush()

    total = 0

    # --------------------------------------
    # Adiciona produtos
    # --------------------------------------

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

        if produto.estoque < item.quantidade:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Estoque insuficiente para o produto "
                    f"'{produto.nome}'. "
                    f"Disponível: {produto.estoque}."
                )
            )

        preco = float(produto.preco)

        subtotal = preco * item.quantidade

        total += subtotal

        item_pedido = ItemPedido(
            pedido_id=pedido.id,
            produto_id=produto.id,
            quantidade=item.quantidade,
            preco_unitario=preco,
            subtotal=subtotal
        )

        db.add(item_pedido)

    pedido.total = total

    db.commit()

    db.refresh(pedido)

    return pedido


# ==========================================
# LISTAR PEDIDOS
# ==========================================

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


# ==========================================
# BUSCAR PEDIDO
# ==========================================

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


# ==========================================
# ALTERAR STATUS
# ==========================================

@router.put(
    "/{pedido_id}/status",
    response_model=PedidoResponse
)
def alterar_status(
    pedido_id: int,
    dados: PedidoStatusUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    empresa_id = obter_empresa_id(credentials)

    novo_status = dados.status

    if novo_status not in STATUS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail="Status inválido."
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

    status_anterior = pedido.status

    # --------------------------------------
    # Não permite alterar pedido concluído
    # --------------------------------------

    if status_anterior == "Concluído":
        raise HTTPException(
            status_code=400,
            detail="Um pedido concluído não pode ser alterado."
        )

    # --------------------------------------
    # Não faz nada se for o mesmo status
    # --------------------------------------

    if status_anterior == novo_status:
        return pedido

    # --------------------------------------
    # CANCELAMENTO
    # --------------------------------------

    if novo_status == "Cancelado":

        # Se estoque já foi baixado,
        # devolve os produtos ao estoque.

        if pedido.estoque_baixado:

            for item in pedido.itens:

                produto = (
                    db.query(Produto)
                    .filter(
                        Produto.id == item.produto_id,
                        Produto.empresa_id == empresa_id
                    )
                    .with_for_update()
                    .first()
                )

                if produto:
                    produto.estoque += item.quantidade

            pedido.estoque_baixado = False

        pedido.status = "Cancelado"

        db.commit()
        db.refresh(pedido)

        return pedido

    # --------------------------------------
    # PEDIDO CANCELADO
    # --------------------------------------

    if status_anterior == "Cancelado":
        raise HTTPException(
            status_code=400,
            detail="Um pedido cancelado não pode voltar para outro status."
        )

    # --------------------------------------
    # CONFIRMAR PEDIDO
    # --------------------------------------

    if novo_status == "Confirmado":

        if not pedido.estoque_baixado:

            produtos = []

            for item in pedido.itens:

                produto = (
                    db.query(Produto)
                    .filter(
                        Produto.id == item.produto_id,
                        Produto.empresa_id == empresa_id
                    )
                    .with_for_update()
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

                if produto.estoque < item.quantidade:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"Estoque insuficiente para "
                            f"'{produto.nome}'. "
                            f"Disponível: {produto.estoque}."
                        )
                    )

                produtos.append(
                    (produto, item.quantidade)
                )

            # Só baixa depois de validar TODOS

            for produto, quantidade in produtos:
                produto.estoque -= quantidade

            pedido.estoque_baixado = True

    # --------------------------------------
    # ALTERA STATUS
    # --------------------------------------

    pedido.status = novo_status

    db.commit()

    db.refresh(pedido)

    return pedido


# ==========================================
# EXCLUIR PEDIDO
# ==========================================

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

    if pedido.estoque_baixado:
        raise HTTPException(
            status_code=400,
            detail=(
                "Este pedido já baixou o estoque. "
                "Cancele o pedido antes de removê-lo."
            )
        )

    db.delete(pedido)

    db.commit()

    return {
        "message": "Pedido excluído com sucesso."
    }