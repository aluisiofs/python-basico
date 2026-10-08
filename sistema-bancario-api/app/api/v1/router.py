from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db_session
from app.services.conta_service import BancoService

# Importação dos schemas
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.schemas.conta import ContaCreate, ContaResponse
from app.schemas.transacao import TransacaoCreate, TransacaoResponse

# Importação dos models corrigida para o sufixo "Model"
from app.models.cliente import ClienteModel
from app.models.conta import ContaModel

router = APIRouter(prefix="/v1")


@router.post(
    "/clientes",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Clientes"],
)
async def cadastrar_cliente(
    dados: ClienteCreate, db: AsyncSession = Depends(get_db_session)
):
    return await BancoService.criar_cliente(db, dados)


@router.post(
    "/contas",
    response_model=ContaResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Contas"],
)
async def abrir_conta(dados: ContaCreate, db: AsyncSession = Depends(get_db_session)):
    return await BancoService.criar_conta(db, dados)


@router.post(
    "/contas/{conta_id}/transacoes",
    response_model=TransacaoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Transações"],
)
async def efetuar_transacao(
    conta_id: int, dados: TransacaoCreate, db: AsyncSession = Depends(get_db_session)
):
    return await BancoService.realizar_transacao(db, conta_id, dados)


@router.get(
    "/clientes", 
    response_model=List[ClienteResponse], 
    status_code=status.HTTP_200_OK,
    tags=["Clientes"]
)
async def listar_clientes(db: AsyncSession = Depends(get_db_session)):
    """Retorna a lista de todos os clientes cadastrados."""
    # Usando ClienteModel
    result = await db.execute(select(ClienteModel))
    clientes = result.scalars().all()
    return clientes


@router.get(
    "/contas/{conta_id}", 
    response_model=ContaResponse, 
    status_code=status.HTTP_200_OK,
    tags=["Contas"]
)
async def obter_conta(conta_id: int, db: AsyncSession = Depends(get_db_session)):
    """Busca uma conta específica pelo ID."""
    # Usando ContaModel
    result = await db.execute(select(ContaModel).where(ContaModel.id == conta_id))
    conta = result.scalar_one_or_none()
    
    if not conta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conta não encontrada")
        
    return conta