from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import relationship

from .database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(150), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    usuarios = relationship(
        "Usuario",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )

    produtos = relationship(
        "Produto",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )

    clientes = relationship(
        "Cliente",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )

    pedidos = relationship(
        "Pedido",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    senha_hash = Column(String(255), nullable=False)

    ativo = Column(Boolean, default=True)

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    empresa = relationship(
        "Empresa",
        back_populates="usuarios"
    )


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)

    descricao = Column(Text, nullable=True)

    preco = Column(
        Float,
        nullable=False,
        default=0
    )

    estoque = Column(
        Integer,
        nullable=False,
        default=0
    )

    estoque_minimo = Column(
        Integer,
        nullable=False,
        default=5
    )

    categoria = Column(
        String(100),
        nullable=True
    )

    ativo = Column(
        Boolean,
        default=True
    )

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    empresa = relationship(
        "Empresa",
        back_populates="produtos"
    )


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)

    telefone = Column(String(20), nullable=True)

    email = Column(String(150), nullable=True)

    cpf = Column(String(14), nullable=True)

    endereco = Column(String(255), nullable=True)

    observacoes = Column(Text, nullable=True)

    ativo = Column(Boolean, default=True)

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    empresa = relationship(
        "Empresa",
        back_populates="clientes"
    )


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    cliente_id = Column(
        Integer,
        ForeignKey("clientes.id"),
        nullable=False
    )

    empresa_id = Column(
        Integer,
        ForeignKey("empresas.id"),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="Pendente"
    )

    total = Column(
        Float,
        nullable=False,
        default=0
    )

    estoque_baixado = Column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    empresa = relationship(
        "Empresa",
        back_populates="pedidos"
    )

    cliente = relationship(
        "Cliente"
    )

    itens = relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    pedido_id = Column(
        Integer,
        ForeignKey("pedidos.id"),
        nullable=False
    )

    produto_id = Column(
        Integer,
        ForeignKey("produtos.id"),
        nullable=False
    )

    quantidade = Column(
        Integer,
        nullable=False
    )

    preco_unitario = Column(
        Float,
        nullable=False
    )

    subtotal = Column(
        Float,
        nullable=False
    )

    pedido = relationship(
        "Pedido",
        back_populates="itens"
    )

    produto = relationship(
        "Produto"
    )