from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(150), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(150), nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    usuarios = relationship(
        "Usuario",
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
        back_populates="usuarios"
    )