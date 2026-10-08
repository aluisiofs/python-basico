# sistema-bancario-api/app/schemas/conta.py
from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.cliente import ClienteResponse


class ContaBase(BaseModel):
    agencia: str = Field(default="0001", max_length=10)


class ContaCreate(ContaBase):
    cliente_id: int = Field(..., gt=0)


class ContaResponse(ContaBase):
    id: int
    numero_conta: int
    saldo: float
    cliente_id: int

    class Config:
        from_attributes = True
