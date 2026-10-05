"""Módulo de validações e leitura segura de dados."""


def validar_numero(valor):
    """Verifica se o valor é int ou float.

    Lança TypeError se não for.
    """
    if not isinstance(valor, (int, float)):
        raise TypeError(f"O valor {valor} não é um número válido.")

    return True


def ler_numero(mensagem: str) -> float:
    """Solicita uma entrada no terminal e garante a conversão para float
    sem interromper o sistema em caso de entrada inválida.
    """
    while True:
        try:
            entrada = input(mensagem)
            return float(entrada)

        except ValueError:
            print("❌ [ERRO] Entrada inválida! " "Por favor, digite apenas números.")
