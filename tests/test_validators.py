"""Testes unitários para o módulo de validações."""

import pytest
from src.utils.validators import validar_numero


def test_validar_numero_inteiro():
    assert validar_numero(10) is True


def test_validar_numero_float():
    assert validar_numero(3.14) is True


def test_validar_numero_string_lanca_type_error():
    with pytest.raises(TypeError):
        validar_numero("10")