"""Ponto de Entrada da Aplicação CLI - NTT DATA."""

from src.modules.calculations import (
    dividir,
    multiplicar,
    somar,
    subtrair,
)

from src.utils.validators import ler_numero


def exibir_menu():
    """Exibe o menu principal da calculadora."""
    print("\n" + "=" * 40)
    print("     NTT DATA - CALCULADORA CLI v1.0")
    print("=" * 40)
    print("1. Somar")
    print("2. Subtrair")
    print("3. Multiplicar")
    print("4. Dividir")
    print("0. Sair")
    print("=" * 40)


def main():
    """Executa o fluxo principal da aplicação."""
    while True:
        exibir_menu()

        opcao = input("Escolha uma opção (0-4): ").strip()

        if opcao == "0":
            print("\nEncerrando a aplicação... Até logo!")
            break

        if opcao not in ["1", "2", "3", "4"]:
            print(
                "❌ [ERRO] Opção inválida! "
                "Escolha um número entre 0 e 4."
            )
            continue

        # Leitura segura de dados
        a = ler_numero("Digite o primeiro número: ")
        b = ler_numero("Digite o segundo número: ")

        # Processamento com tratamento de exceções
        try:
            if opcao == "1":
                resultado = somar(a, b)
                print(f"👉 Resultado: {a} + {b} = {resultado}")

            elif opcao == "2":
                resultado = subtrair(a, b)
                print(f"👉 Resultado: {a} - {b} = {resultado}")

            elif opcao == "3":
                resultado = multiplicar(a, b)
                print(f"👉 Resultado: {a} * {b} = {resultado}")

            elif opcao == "4":
                resultado = dividir(a, b)
                print(f"👉 Resultado: {a} / {b} = {resultado}")

        except ValueError as e:
            print(f"❌ [REGRA DE NEGÓCIO]: {e}")

        except Exception as e:
            print(f"❌ [ERRO INESPERADO]: {e}")


if __name__ == "__main__":
    main()