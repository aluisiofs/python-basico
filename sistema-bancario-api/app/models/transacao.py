from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.conta import ContaModel


class TransacaoModel(Base):
    __tablename__ = "transacoes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 'deposito' ou 'saque'
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    data_hora: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    conta_id: Mapped[int] = mapped_column(ForeignKey("contas.id"), nullable=False)

    conta: Mapped["ContaModel"] = relationship(back_populates="transacoes")
