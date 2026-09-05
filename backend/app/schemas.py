from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class CadastroRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str

    empresa_nome: str
    empresa_cnpj: Optional[str] = None
    empresa_telefone: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    empresa_id: int
    ativo: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class EmpresaResponse(BaseModel):
    id: int
    nome: str
    cnpj: Optional[str]
    telefone: Optional[str]
    email: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)