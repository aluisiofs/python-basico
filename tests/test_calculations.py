"""Testes unitários para o módulo de cálculos."""

import pytest
from src.modules.calculations import dividir, multiplicar, somar, subtrair


def test_somar():
    assert somar(10, 5) == 15
    assert somar(-2, 5) == 3


def test_subtrair():
    assert subtrair(10, 5) == 5


def test_multiplicar():
    assert multiplicar(10, 5) == 50


def test_dividir():
    assert dividir(10, 2) == 5.0


def test_dividir_por_zero():
    with pytest.raises(ValueError, match="Não é possível dividir por zero."):
        dividir(10, 0)