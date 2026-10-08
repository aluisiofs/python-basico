from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class ContaBase(BaseModel):
    agencia: str = Field(default="0001", max_length=10)


class ContaCreate(ContaBase):
    cliente_id: int = Field(..., gt=0)


class ContaResponse(ContaBase):
    id: int
    numero_conta: int
    saldo: float
    cliente_id: int

    model_config = ConfigDict(from_attributes=True)
