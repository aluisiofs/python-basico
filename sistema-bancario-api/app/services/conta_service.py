import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.conta import ContaModel
from app.models.transacao import TransacaoModel
from app.models.cliente import ClienteModel
from app.schemas.transacao import TransacaoCreate
from app.schemas.conta import ContaCreate
from app.schemas.cliente import ClienteCreate

class BancoService:
    @staticmethod
    async def criar_cliente(session: AsyncSession, dados: ClienteCreate) -> ClienteModel:
        stmt = select(ClienteModel).where(ClienteModel.cpf == dados.cpf)
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CPF já cadastrado no sistema."
            )
        
        novo_cliente = ClienteModel(**dados.model_dump())
        session.add(novo_cliente)
        await session.commit()
        await session.refresh(novo_cliente)
        return novo_cliente

    @staticmethod
    async def criar_conta(session: AsyncSession, dados: ContaCreate) -> ContaModel:
        cliente = await session.get(ClienteModel, dados.cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente informado não encontrado."
            )

        nova_conta = ContaModel(
            numero_conta=random.randint(10000, 99999), # Gera número da conta automaticamente
            agencia=dados.agencia,
            saldo=0.0,
            cliente_id=dados.cliente_id
        )
        session.add(nova_conta)
        await session.commit()
        await session.refresh(nova_conta)
        return nova_conta

    @staticmethod
    async def realizar_transacao(session: AsyncSession, conta_id: int, dados: TransacaoCreate) -> TransacaoModel:
        conta = await session.get(ContaModel, conta_id)
        if not conta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conta bancária não encontrada."
            )

        if dados.tipo.lower() == "deposito":
            conta.saldo += dados.valor

        elif dados.tipo.lower() == "saque":
            if conta.saldo < dados.valor:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Saldo insuficiente para realizar o saque."
                )
            conta.saldo -= dados.valor
        
        transacao = TransacaoModel(
            tipo=dados.tipo.lower(),
            valor=dados.valor,
            conta_id=conta.id
        )
        session.add(transacao)
        
        await session.commit()
        await session.refresh(transacao)
        return transacao