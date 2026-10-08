from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.services.conta_service import BancoService
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.schemas.conta import ContaCreate, ContaResponse
from app.schemas.transacao import TransacaoCreate, TransacaoResponse

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
    # Linha dados.conta_id = conta_id removida
    return await BancoService.realizar_transacao(db, conta_id, dados)
