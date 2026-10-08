from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException

from app.schemas.cliente import ClienteCreate
from app.schemas.conta import ContaCreate
from app.schemas.transacao import TransacaoCreate
from app.services.conta_service import BancoService


@pytest.mark.asyncio
async def test_criar_cliente_sucesso():
    session = AsyncMock()
    session.add = Mock()

    resultado = Mock()
    resultado.scalar_one_or_none.return_value = None
    session.execute.return_value = resultado

    dados = ClienteCreate(
        nome="Aluisio Felipe",
        cpf="12345678909",
        data_nascimento="01/01/1990",
        endereco="Rua NTT DATA, 100 - SP",
    )

    cliente = await BancoService.criar_cliente(session, dados)

    assert cliente is not None
    assert cliente.nome == "Aluisio Felipe"
    assert cliente.cpf == "12345678909"

    session.add.assert_called_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_criar_cliente_cpf_duplicado():
    session = AsyncMock()
    session.add = Mock()

    resultado = Mock()
    resultado.scalar_one_or_none.return_value = object()
    session.execute.return_value = resultado

    dados = ClienteCreate(
        nome="Aluisio Felipe",
        cpf="12345678909",
        data_nascimento="01/01/1990",
        endereco="Rua NTT DATA, 100 - SP",
    )

    with pytest.raises(HTTPException) as exc:
        await BancoService.criar_cliente(session, dados)

    assert exc.value.status_code == 400
    assert exc.value.detail == "CPF já cadastrado no sistema."

    session.add.assert_not_called()


@pytest.mark.asyncio
async def test_criar_conta_cliente_inexistente():
    session = AsyncMock()
    session.add = Mock()
    session.get.return_value = None

    dados = ContaCreate(
        agencia="0001",
        cliente_id=999999,
    )

    with pytest.raises(HTTPException) as exc:
        await BancoService.criar_conta(session, dados)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Cliente informado não encontrado."

    session.add.assert_not_called()


@pytest.mark.asyncio
async def test_criar_conta_sucesso():
    session = AsyncMock()
    session.add = Mock()
    session.get.return_value = object()

    dados = ContaCreate(
        agencia="0001",
        cliente_id=1,
    )

    with patch(
        "app.services.conta_service.random.randint",
        return_value=12345,
    ):
        conta = await BancoService.criar_conta(session, dados)

    assert conta.numero_conta == 12345
    assert conta.agencia == "0001"
    assert conta.saldo == 0.0
    assert conta.cliente_id == 1

    session.add.assert_called_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_realizar_deposito_sucesso():
    session = AsyncMock()

    conta = SimpleNamespace(
        id=1,
        saldo=0.0,
    )

    session.get.return_value = conta

    dados = TransacaoCreate(
        tipo="deposito",
        valor=500.0,
    )

    transacao = await BancoService.realizar_transacao(
        session,
        conta_id=1,
        dados=dados,
    )

    assert conta.saldo == 500.0
    assert transacao.tipo == "deposito"
    assert transacao.valor == 500.0
    assert transacao.conta_id == 1

    session.add.assert_called_once()
    session.commit.assert_awaited_once()
    session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_realizar_saque_sucesso():
    session = AsyncMock()
    session.add = Mock()

    conta = SimpleNamespace(
        id=1,
        saldo=500.0,
    )

    session.get.return_value = conta

    dados = TransacaoCreate(
        tipo="saque",
        valor=200.0,
    )

    transacao = await BancoService.realizar_transacao(
        session,
        conta_id=1,
        dados=dados,
    )

    assert conta.saldo == 300.0
    assert transacao.tipo == "saque"
    assert transacao.valor == 200.0
    assert transacao.conta_id == 1


@pytest.mark.asyncio
async def test_realizar_saque_sem_saldo():
    session = AsyncMock()
    session.add = Mock()

    conta = SimpleNamespace(
        id=1,
        saldo=100.0,
    )

    session.get.return_value = conta

    dados = TransacaoCreate(
        tipo="saque",
        valor=200.0,
    )

    with pytest.raises(HTTPException) as exc:
        await BancoService.realizar_transacao(
            session,
            conta_id=1,
            dados=dados,
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "Saldo insuficiente para realizar o saque."

    assert conta.saldo == 100.0
    session.add.assert_not_called()


@pytest.mark.asyncio
async def test_realizar_transacao_conta_inexistente():
    session = AsyncMock()
    session.add = Mock()
    session.get.return_value = None
    

    dados = TransacaoCreate(
        tipo="deposito",
        valor=100.0,
    )

    with pytest.raises(HTTPException) as exc:
        await BancoService.realizar_transacao(
            session,
            conta_id=999999,
            dados=dados,
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Conta bancária não encontrada."

    session.add.assert_not_called()
