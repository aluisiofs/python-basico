import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_fluxo_bancario_completo(client: AsyncClient):
    # 1. Criação do cliente com a data de nascimento no padrão brasileiro exigido pela API
    response_cliente = await client.post("/api/v1/clientes/", json={
        "nome": "Aluisio Felipe",
        "cpf": "12345678909",
        "data_nascimento": "01/01/1990", # <- Alterado para o formato DD/MM/YYYY
        "endereco": "Rua NTT DATA, 100 - SP"
    })
    
    if response_cliente.status_code != 201:
        print("\nERRO DE VALIDAÇÃO PYDANTIC:", response_cliente.json())
        
    assert response_cliente.status_code == 201
    cliente_id = response_cliente.json()["id"]

    # 2. Abertura da conta associada ao cliente
    response_conta = await client.post("/api/v1/contas/", json={
        "numero_conta": 1001,
        "agencia": "0001",
        "cliente_id": cliente_id
    })
    assert response_conta.status_code == 201
    conta_id = response_conta.json()["id"]
    assert response_conta.json()["saldo"] == 0.0

    # 3. Transação de depósito (regras ACID)
    response_deposito = await client.post(f"/api/v1/contas/{conta_id}/transacoes", json={
        "tipo": "deposito",
        "valor": 500.00
    })
    assert response_deposito.status_code == 201
    assert response_deposito.json()["valor"] == 500.00

    # 4. Transação de saque com saldo suficiente
    response_saque = await client.post(f"/api/v1/contas/{conta_id}/transacoes", json={
        "tipo": "saque",
        "valor": 200.00
    })
    assert response_saque.status_code == 201

    # 5. Validação de regra de negócio: bloqueio de saque sem saldo suficiente
    response_falha = await client.post(f"/api/v1/contas/{conta_id}/transacoes", json={
        "tipo": "saque",
        "valor": 400.00
    })
    assert response_falha.status_code == 400
    assert response_falha.json()["detail"] == "Saldo insuficiente para realizar o saque."

    # 6. Consultar conta existente (Cobre a rota GET)
    response_get_conta = await client.get(f"/api/v1/contas/{conta_id}")
    assert response_get_conta.status_code == 200
    assert response_get_conta.json()["id"] == conta_id

    # 7. Tentar consultar uma conta que não existe (Cobre a exceção 404 Not Found)
    response_404 = await client.get("/api/v1/contas/999999")
    assert response_404.status_code == 404
    
    # 8. Listar todos os clientes (Cobre a rota GET All)
    response_lista_clientes = await client.get("/api/v1/clientes/")
    assert response_lista_clientes.status_code == 200
    assert len(response_lista_clientes.json()) > 0