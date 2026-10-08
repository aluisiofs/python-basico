import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_fluxo_bancario_completo(client: AsyncClient):
    # ==========================================
    # 1. TESTES DE CLIENTE
    # ==========================================
    payload_cliente = {
        "nome": "Aluisio Felipe",
        "cpf": "12345678909",
        "data_nascimento": "01/01/1990",
        "endereco": "Rua NTT DATA, 100 - SP",
    }

    # 1.1 Criar cliente com sucesso
    response_cliente = await client.post("/api/v1/clientes", json=payload_cliente)
    assert response_cliente.status_code == 201
    cliente_id = response_cliente.json()["id"]

    # 1.2 FORÇAR ERRO: Tentar cadastrar o mesmo CPF novamente
    response_cliente_duplicado = await client.post(
        "/api/v1/clientes", json=payload_cliente
    )
    assert response_cliente_duplicado.status_code == 400
    assert (
        response_cliente_duplicado.json()["detail"] == "CPF já cadastrado no sistema."
    )

    # ==========================================
    # 2. TESTES DE CONTA
    # ==========================================
    # 2.1 Criar conta com sucesso
    response_conta = await client.post(
        "/api/v1/contas", json={"agencia": "0001", "cliente_id": cliente_id}
    )
    assert response_conta.status_code == 201
    conta_id = response_conta.json()["id"]

    # 2.2 FORÇAR ERRO: Tentar criar conta para cliente que não existe
    response_conta_erro = await client.post(
        "/api/v1/contas", json={"agencia": "0002", "cliente_id": 999999}
    )
    assert response_conta_erro.status_code == 404
    assert response_conta_erro.json()["detail"] == "Cliente informado não encontrado."

    # ==========================================
    # 3. TESTES DE TRANSAÇÕES
    # ==========================================
    # 3.1 Sucesso: Depósito
    response_deposito = await client.post(
        f"/api/v1/contas/{conta_id}/transacoes",
        json={"tipo": "deposito", "valor": 500.00},
    )
    assert response_deposito.status_code == 201

    # 3.2 Sucesso: Saque
    response_saque = await client.post(
        f"/api/v1/contas/{conta_id}/transacoes", json={"tipo": "saque", "valor": 200.00}
    )
    assert response_saque.status_code == 201

    # 3.3 FORÇAR ERRO: Saque sem saldo
    response_falha_saldo = await client.post(
        f"/api/v1/contas/{conta_id}/transacoes", json={"tipo": "saque", "valor": 400.00}
    )
    assert response_falha_saldo.status_code == 400
    assert (
        response_falha_saldo.json()["detail"]
        == "Saldo insuficiente para realizar o saque."
    )

    # 3.4 FORÇAR ERRO: Transação em conta que não existe
    response_transacao_erro = await client.post(
        "/api/v1/contas/999999/transacoes", json={"tipo": "deposito", "valor": 100.00}
    )
    assert response_transacao_erro.status_code == 404
    assert response_transacao_erro.json()["detail"] == "Conta bancária não encontrada."

    # ==========================================
    # 4. TESTES DE CONSULTA (GET / ROUTER)
    # ==========================================
    # 4.1 Consultar conta existente
    response_get_conta = await client.get(f"/api/v1/contas/{conta_id}")
    assert response_get_conta.status_code == 200

    # 4.2 Consultar conta inexistente
    response_get_conta_erro = await client.get("/api/v1/contas/999999")
    assert response_get_conta_erro.status_code == 404

    # 4.3 Listar todos os clientes
    response_lista_clientes = await client.get("/api/v1/clientes")
    assert response_lista_clientes.status_code == 200
