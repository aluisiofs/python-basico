from abc import ABC

from models.historico import Historico


class Conta(ABC):

    def __init__(self, numero: int, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self) -> Historico:
        return self._historico

    def sacar(self, valor: float) -> bool:
        excedeu_saldo = valor > self.saldo

        if excedeu_saldo:
            print("\n❌ Operação falhou! Você não tem saldo suficiente.")
            return False

        elif valor > 0:
            self._saldo -= valor
            print(f"\n✅ Saque de R$ {valor:.2f} realizado com sucesso!")
            return True

        else:
            print("\n❌ Operação falhou! O valor informado é inválido.")
            return False

    def depositar(self, valor: float) -> bool:
        if valor > 0:
            self._saldo += valor
            print(f"\n✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
            return True

        else:
            print("\n❌ Operação falhou! O valor informado é inválido.")
            return False


class ContaCorrente(Conta):

    def __init__(
        self,
        numero: int,
        cliente,
        limite: float = 500.0,
        limite_saques: int = 3,
    ):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [
                t
                for t in self.historico.transacoes
                if t["tipo"] == "Saque"
            ]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print(
                f"\n❌ Operação falhou! "
                f"O valor excede o limite de R$ {self._limite:.2f}."
            )
            return False

        elif excedeu_saques:
            print(
                "\n❌ Operação falhou! "
                "Número máximo de saques diários atingido."
            )
            return False

        return super().sacar(valor)

    def __str__(self):
        return (
            f"Agência:\t{self.agencia}\n"
            f"C/C:\t\t{self.numero}\n"
            f"Titular:\t{self.cliente.nome}"
        )