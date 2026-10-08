from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.cliente import ClienteModel
    from app.models.transacao import TransacaoModel


class ContaModel(Base):
    __tablename__ = "contas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    agencia: Mapped[str] = mapped_column(String(10), default="0001", nullable=False)
    numero_conta: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)
    saldo: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)

    titular: Mapped["ClienteModel"] = relationship(back_populates="contas")
    transacoes: Mapped[list["TransacaoModel"]] = relationship(
        back_populates="conta",
        cascade="all, delete-orphan",
    )