from src.utils.validators import validar_numero


def somar(a, b):
    """Retorna a soma de dois números."""
    validar_numero(a)
    validar_numero(b)

    return a + b


def subtrair(a, b):
    """Retorna a diferença entre dois números."""
    validar_numero(a)
    validar_numero(b)

    return a - b


def multiplicar(a, b):
    """Retorna o produto de dois números."""
    validar_numero(a)
    validar_numero(b)

    return a * b


def dividir(a, b):
    """Retorna a divisão entre dois números."""
    validar_numero(a)
    validar_numero(b)

    if b == 0:
        raise ValueError("Não é possível dividir por zero.")

    return a / b