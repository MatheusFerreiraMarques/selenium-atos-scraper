from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, UniqueConstraint
from database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    password = Column(String(255))

class Atos(Base):
    __tablename__ = "atos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    tipo_ato = Column(String(100), nullable=False)
    numero_ato = Column(Integer, nullable=False)
    orgao = Column(String(150), nullable=False)
    publicacao = Column(Date, nullable=False)
    ementa = Column(Text, nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "numero_ato",
            "publicacao",
            "orgao",
            name="uq_numero_publicacao_orgao"
        ),
    )