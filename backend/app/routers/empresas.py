from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..auth import decode_token
from ..database import get_db
from ..models import Empresa
from ..schemas import EmpresaResponse


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)

security = HTTPBearer()


@router.get(
    "/minha-empresa",
    response_model=EmpresaResponse
)
def minha_empresa(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
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

    empresa = (
        db.query(Empresa)
        .filter(
            Empresa.id == empresa_id
        )
        .first()
    )

    if not empresa:
        raise HTTPException(
            status_code=404,
            detail="Empresa não encontrada."
        )

    return empresa