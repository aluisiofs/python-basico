from pydantic import BaseModel, ConfigDict, Field, constr
from typing import List, Optional


class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    cpf: str = Field(..., min_length=11, max_length=11, pattern=r"^\d{11}$")
    data_nascimento: str = Field(..., pattern=r"^\d{2}/\d{2}/\d{4}$")
    endereco: str = Field(..., min_length=5, max_length=255)


class ClienteCreate(ClienteBase):
    pass


class ClienteResponse(ClienteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
