"""Sistema Bancário CLI - versão POO (Semana 4 / Trilha NTT DATA)."""

import sys

from models.cliente import PessoaFisica
from models.conta import ContaCorrente
from models.transacao import Deposito, Saque


def filtrar_cliente(cpf: str, clientes: list):
    clientes_filtrados = [c for c in clientes if c.cpf == cpf]

    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n❌ Cliente não possui conta cadastrada!")
        return None

    return cliente.contas[0]


def depositar(clientes: list):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: R$ "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes: list):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: R$ "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes: list):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    print("\n================ EXTRATO ================")

    transacoes = conta.historico.transacoes

    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(
                f"\n{transacao['tipo']}:"
                f"\n\tR$ {transacao['valor']:.2f}"
                f" ({transacao['data']})"
            )

    print(f"\nSaldo atual:\tR$ {conta.saldo:.2f}")
    print("=========================================")


def criar_cliente(clientes: list):
    cpf = input("Informe o CPF (somente números): ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n❌ Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input(
        "Informe a data de nascimento (dd-mm-aaaa): "
    ).strip()
    endereco = input(
        "Informe o endereço "
        "(logradouro, nro - bairro - cidade/sigla estado): "
    ).strip()

    cliente = PessoaFisica(
        nome=nome,
        data_nascimento=data_nascimento,
        cpf=cpf,
        endereco=endereco,
    )

    clientes.append(cliente)

    print("\n✅ Cliente criado com sucesso!")


def criar_conta(numero_conta: int, clientes: list, contas: list):
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(
            "\n❌ Cliente não encontrado! "
            "Cadastre o cliente primeiro."
        )
        return

    conta = ContaCorrente.nova_conta(
        cliente=cliente,
        numero=numero_conta,
    )

    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(
        f"\n✅ Conta C/C nº {numero_conta} "
        f"criada com sucesso para {cliente.nome}!"
    )


def listar_contas(contas: list):
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return

    print("\n================ LISTA DE CONTAS ================")

    for conta in contas:
        print("=" * 45)
        print(str(conta))


def main():
    clientes = []
    contas = []

    menu = """
================ MENU ================
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova Conta
[lc] Listar Contas
[nu] Novo Cliente
[q] Sair
=>
"""

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema bancário!")
            sys.exit()

        else:
            print(
                "\n❌ Opção inválida, "
                "por favor selecione novamente."
            )


if __name__ == "__main__":
    main()