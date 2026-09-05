from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import (
    create_access_token,
    hash_password,
    verify_password
)

from ..database import get_db
from ..models import Empresa, Usuario
from ..schemas import (
    CadastroRequest,
    LoginRequest,
    TokenResponse,
    UsuarioResponse
)

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post(
    "/cadastro",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar(
    dados: CadastroRequest,
    db: Session = Depends(get_db)
):

    usuario_existente = (
        db.query(Usuario)
        .filter(
            Usuario.email == dados.email
        )
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Este e-mail já está cadastrado."
        )

    empresa = Empresa(
        nome=dados.empresa_nome,
        cnpj=dados.empresa_cnpj,
        telefone=dados.empresa_telefone,
        email=dados.email
    )

    db.add(empresa)
    db.flush()

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_password(dados.senha),
        empresa_id=empresa.id
    )

    db.add(usuario)

    db.commit()
    db.refresh(usuario)

    return usuario


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):

    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.email == dados.email
        )
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    if not verify_password(
        dados.senha,
        usuario.senha_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    if not usuario.ativo:
        raise HTTPException(
            status_code=403,
            detail="Usuário desativado."
        )

    token = create_access_token(
        {
            "sub": str(usuario.id),
            "empresa_id": usuario.empresa_id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }