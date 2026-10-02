"""Sistema Bancário CLI - Protótipo v1 (Semana 2)."""

import sys


def main():
    menu = """
================ MENU ================
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=>
"""

    saldo = 0.0
    limite = 500.0
    extrato = []
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: R$ "))

            if valor > 0:
                saldo += valor
                extrato.append(f"Depósito: R$ {valor:.2f}")
                print(
                    f"\n✅ Depósito de R$ {valor:.2f} realizado com sucesso!"
                )
            else:
                print("\n❌ Operação falhou! O valor informado é inválido.")

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: R$ "))

            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                print("\n❌ Operação falhou! Você não tem saldo suficiente.")

            elif excedeu_limite:
                print(
                    f"\n❌ Operação falhou! "
                    f"O valor excede o limite de R$ {limite:.2f}."
                )

            elif excedeu_saques:
                print(
                    "\n❌ Operação falhou! "
                    "Número máximo de saques diários atingido."
                )

            elif valor > 0:
                saldo -= valor
                extrato.append(f"Saque: R$ {valor:.2f}")
                numero_saques += 1

                print(
                    f"\n✅ Saque de R$ {valor:.2f} realizado com sucesso!"
                )

            else:
                print("\n❌ Operação falhou! O valor informado é inválido.")

        elif opcao == "e":
            print("\n================ EXTRATO ================")

            if not extrato:
                print("Não foram realizadas movimentações.")
            else:
                for movimentacao in extrato:
                    print(movimentacao)

            print(f"\nSaldo atual: R$ {saldo:.2f}")
            print("=========================================")

        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema bancário!")
            sys.exit()

        else:
            print(
                "\n❌ Opção inválida, por favor selecione novamente "
                "a operação desejada."
            )


if __name__ == "__main__":
    main()