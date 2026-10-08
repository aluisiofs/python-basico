from pydantic import BaseModel, Field
from datetime import datetime


class TransacaoBase(BaseModel):
    valor: float = Field(
        ..., gt=0, description="O valor da transação deve ser maior que zero"
    )


class TransacaoCreate(TransacaoBase):
    # conta_id removido daqui, pois ele virá pela URL
    tipo: str = Field(..., pattern="^(deposito|saque)$")


class TransacaoResponse(TransacaoBase):
    id: int
    tipo: str
    data_hora: datetime
    conta_id: int

    class Config:
        from_attributes = True
