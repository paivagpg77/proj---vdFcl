from fastapi import APIRouter, Header, HTTPException

router = APIRouter(
    prefix="/webhooks/n8n",
    tags=["n8n"]
)


@router.post("/pedido")
def receber_pedido(
    dados: dict,
    x_n8n_secret: str | None = Header(default=None)
):
    if x_n8n_secret != "TESTE-VENDEFACIL":
        raise HTTPException(
            status_code=401,
            detail="Webhook não autorizado."
        )

    return {
        "status": "recebido",
        "origem": "n8n",
        "dados": dados
    }