from datetime import datetime
from abc import ABC, abstractmethod

# CLASSES

class Historico:
    def __init__(self):
        self.transacoes = []

    def transacoes_do_dia(self):
        hoje = datetime.now().strftime("%d/%m/%Y")
        return [t for t in self.transacoes if t["data"] == hoje]

    def pode_transacionar(self):
        return len(self.transacoes_do_dia()) < 10

    def adicionar_transacao(self, tipo, valor):
        if not self.pode_transacionar():
            print("⚠️ Limite diário de 10 transações atingido.")
            return False

        data_tempo = datetime.now()
        self.transacoes.append({
            "tipo": tipo,
            "valor": valor,
            "data": data_tempo.strftime("%d/%m/%Y"),
            "hora": data_tempo.strftime("%H:%M:%S")
        })
        return True

    def extrato(self, conta):
        print(f"\n--- EXTRATO ---")
        print(f"AGÊNCIA {conta._agencia} CONTA N° {conta._numero}")
        for t in self.transacoes:
            print(f"{t['tipo']} de R${t['valor']:.2f} data: {t['data']} horário: {t['hora']}")
        print(f"Saldo atual: R${conta._saldo:.2f}\n")


class Conta:
    def __init__(self, numero, agencia, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    def deposito(self, valor):
        if valor <= 0:
            print("Valor inválido para depósito.")
            return False

        if self._historico.adicionar_transacao("Depósito", valor):
            self._saldo += valor
            print(f"Depósito de R${valor:.2f} realizado.")
            return True
        return False

    def saque(self, valor, limite=500, limite_saques=3):
        saques_do_dia = len([t for t in self._historico.transacoes_do_dia() if t["tipo"] == "Saque"])

        if valor <= 0:
            print("Valor inválido para saque.")
            return False
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False
        if valor > limite:
            print("O valor do saque excede o limite permitido.")
            return False
        if saques_do_dia >= limite_saques:
            print("Limite de saques diários atingido.")
            return False

        if self._historico.adicionar_transacao("Saque", valor):
            self._saldo -= valor
            print(f"Saque de R${valor:.2f} realizado.")
            return True
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite=500, limite_saques=3):
        super().__init__(numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques


class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco, senha):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.senha = senha
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    pass


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta: Conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta: Conta):
        conta.deposito(self._valor)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta: Conta):
        conta.saque(self._valor)


# MENU PRINCIPAL

clientes = []
contas = []
prox_numero_conta = 1


def encontrar_cliente(cpf, senha=None):
    for cliente in clientes:
        if cliente.cpf == cpf and (senha is None or cliente.senha == senha):
            return cliente
    return None


def menu_principal():
    global prox_numero_conta

    while True:
        print("""
1 - LOGIN
2 - REGISTRO
3 - SAIR
""")
        opcao = input("--> ")

        if opcao == "1":  # login
            cpf = input("CPF:\n--> ")
            senha = input("SENHA:\n--> ")
            cliente = encontrar_cliente(cpf, senha)
            if cliente:
                print(f"\nBem-vindo(a), {cliente.nome}!\n")
                menu_conta(cliente)
            else:
                print("CPF ou senha inválidos!")

        elif opcao == "2":  # registro
            nome = input("NOME:\n--> ")

            # validar data de nascimento
            while True:
                data_nasc = input("DATA DE NASCIMENTO (dd/mm/aaaa):\n--> ")
                try:
                    dia, mes, ano = map(int, data_nasc.split("/"))
                    datetime(ano, mes, dia)  # tenta criar uma data válida
                    break
                except (ValueError, TypeError):
                    print("Data de nascimento inválida. Use o formato dd/mm/aaaa.")

            # validar CPF
            while True:
                cpf = input("CPF (11 dígitos):\n--> ")
                if cpf.isdigit() and len(cpf) == 11:
                    if encontrar_cliente(cpf):
                        print("Já existe um cliente com esse CPF.")
                    else:
                        break
                else:
                    print("CPF inválido. Deve conter 11 números.")

            # validar senha
            while True:
                senha = input("SENHA (8 dígitos):\n--> ")
                if senha.isdigit() and len(senha) == 8:
                    break
                else:
                    print("Senha inválida. Deve conter 8 números.")

            endereco = input("ENDEREÇO:\n--> ")

            # criar cliente e conta
            cliente = PessoaFisica(nome, cpf, data_nasc, endereco, senha)
            clientes.append(cliente)

            conta = ContaCorrente(numero=prox_numero_conta, agencia="0001", cliente=cliente)
            cliente.adicionar_conta(conta)
            contas.append(conta)
            prox_numero_conta += 1

            print("Conta criada com sucesso!\n")

        elif opcao == "3":
            print("Fim do programa.")
            break
        else:
            print("Opção inválida!")


def menu_conta(cliente):
    conta = cliente.contas[0]  # por enquanto cada cliente só tem 1 conta

    while True:
        print("""
1 - DEPOSITO
2 - SAQUE
3 - EXTRATO
4 - SAIR DA CONTA
""")
        opcao = input("--> ")

        if opcao == "1":
            valor_str = input("Valor do depósito: R$")
            if not valor_str.strip():  # vazio
                print("Valor inválido.")
                continue
            try:
                valor = float(valor_str)
            except ValueError:
                print("Valor inválido.")
                continue
            deposito = Deposito(valor)
            deposito.registrar(conta)

        elif opcao == "2":
            valor_str = input("Valor do saque: R$")
            if not valor_str.strip():  # vazio
                print("Valor inválido.")
                continue
            try:
                valor = float(valor_str)
            except ValueError:
                print("Valor inválido.")
                continue
            saque = Saque(valor)
            saque.registrar(conta)

        elif opcao == "3":
            conta._historico.extrato(conta)

        elif opcao == "4":
            print("Saindo da conta...\n")
            break
        else:
            print("Opção inválida!")



if __name__ == "__main__":
    menu_principal()
    