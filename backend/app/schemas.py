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


class ProdutoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int = 0
    estoque_minimo: int = 5
    categoria: Optional[str] = None


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None
    estoque_minimo: Optional[int] = None
    categoria: Optional[str] = None
    ativo: Optional[bool] = None


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    preco: float
    estoque: int
    estoque_minimo: int
    categoria: Optional[str]
    ativo: bool
    empresa_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ClienteCreate(BaseModel):
    nome: str
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    endereco: Optional[str] = None
    observacoes: Optional[str] = None


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    endereco: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None


class ClienteResponse(BaseModel):
    id: int
    nome: str
    telefone: Optional[str]
    email: Optional[EmailStr]
    cpf: Optional[str]
    endereco: Optional[str]
    observacoes: Optional[str]
    ativo: bool
    empresa_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)