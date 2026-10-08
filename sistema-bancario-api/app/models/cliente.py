from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

# Importação "falsa" usada apenas para o MyPy conseguir ler os tipos
if TYPE_CHECKING:
    from app.models.conta import ContaModel


class ClienteModel(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, index=True, nullable=False)
    data_nascimento: Mapped[str] = mapped_column(String(10), nullable=False)
    endereco: Mapped[str] = mapped_column(String(255), nullable=False)

    # Corrigido para list nativo do Python 3.9+
    contas: Mapped[list["ContaModel"]] = relationship(
        back_populates="titular",
        cascade="all, delete-orphan",
    )