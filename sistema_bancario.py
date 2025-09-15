from datetime import datetime
telas = ["""
1 - LOGIN
2 - REGISTRO
3 - SAIR DO APP

-->""","""
1 - DEPOSITO
2 - SAQUE
3 - EXTRATO
4 - SAIR DA CONTA

-->"""]
tela = 0
nome = ""
cpf = ""
extrato_bancario = [[[],[],[],[]]] #valor, data, hora, bool
saldo_e_quantia_de_saques = [[[0.0],[0]]]
#cpf, senha, nome, data_de_nascimento, endereço, data_de_criação_da_conta, número_da_conta, agência 0001
usuario = [["00000000000"],["12345678"],["Python"],[["01","01","1990"]],[["rua","01","Py","Pylandia","Pylandia"]],[datetime.now()],[1],["0001"]]
index = 0
sistema = True
quantia_de_saques_realizados_no_dia = 0

def validador_de_valor_de_entrada(self, valor):
    if type(valor) is float and valor > 0:
        return valor
    elif type(valor) is int and valor > 0:
        return float(valor)
    else:
        return 0.0
    
def deposito(self, valor, index):
    if valor > 0 and extrato_bancario[index][1].count(datetime.now().strftime("%d/%m/%Y")) < 10:
        print(f"Deposio de R${valor:.2f} realizado.")
        acrescentar_no_extrato(valor, True, index)
        return True, valor
    elif valor > 0 and extrato_bancario[index][1].count(datetime.now().strftime("%d/%m/%Y")) >= 10:
        print("Deposito negado, limite de transações realizadas.")
        return False, 0
    else:
        print("Deposito negado, tente novamente.")
        return False, 0

def saque(self, valor, saldo, quantia_de_saques_realizados_no_dia, index):
    transacoes_do_dia = extrato_bancario[index][1].count(datetime.now().strftime("%d/%m/%Y"))
    saque_valido = valor <= saldo and valor > 0 and valor <= 500 and quantia_de_saques_realizados_no_dia < 3 and transacoes_do_dia < 10
    saque_limite_transacao = valor > 0 and valor > 500 and quantia_de_saques_realizados_no_dia < 3 and quantia_de_saques_realizados_no_dia  < 10
    saque_limite_monetario = valor > 0 and valor > 500 and quantia_de_saques_realizados_no_dia < 3
    saque_limite_diario = valor > 0 and quantia_de_saques_realizados_no_dia >=3
    if saque_valido:
        print(f"Saque de R${valor:.2f} realizado.")
        acrescentar_no_extrato(valor, False, index)
        quantia_de_saques_realizados_no_dia
        return True, valor
    elif saque_limite_transacao:
        print("Deposito negado, limite de transações realizadas.")
        return False, 0
    elif saque_limite_monetario:
        print("O valor do saque inserido é maior do que o valor permitido.")
        return False, 0
    elif saque_limite_diario:
        print("Saques negado, limite de saques atingido.")
        return False, 0
    else:
        print("Saque negado, tente novamente.")
        return False, 0

class conta:

    def __init__(self, saldo, numero, agencia, cliente, historico):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico
        
class historico:
    def adcionar_transacao():
        pass 
    pass

class conta_corrente:
    def __init__(self, limite, limite_saques):
        self._limite = limite
        self._limite_saques = limite_saques
        pass
    pass

class deposito:
    def __init__(self, valor):
        self._valor = valor
        pass
    pass

class saque:
    def __init__(self, valor):
        self._valor = valor
        pass
    pass

class transacao:
    def registrar(self, conta : conta):
        pass
    pass

class client:
    pass

class pessoa_fisica:
    pass

def acrescentar_no_extrato(valor, valor_positivo_negativo, index):
    data_tempo = datetime.now()
    extrato_bancario[index][0].append(valor)
    extrato_bancario[index][1].append(data_tempo.strftime("%d/%m/%Y"))
    extrato_bancario[index][2].append(data_tempo.strftime("%H:%M:%S"))
    extrato_bancario[index][3].append(valor_positivo_negativo)

def extrato(index, saldo):
    print(f"AGÊNCIA {usuario[7][index]} CONTA N° {usuario[6][index]}")
    for x in range(len(extrato_bancario[index][0])):
            if extrato_bancario[index][3][x] == True:
                print(f"Deposito de R${extrato_bancario[index][0][x]:.2f} data: {extrato_bancario[index][1][x]} horario: {extrato_bancario[index][2][x]}")
            else:
                print(f"Saque de R${extrato_bancario[index][0][x]:.2f} data: {extrato_bancario[index][1][x]} horario: {extrato_bancario[index][2][x]}")       
    print(f"saldo: R${saldo:.2f}")

def validar_registro(cpf, senha):
    cpf_e_senha_valida = cpf not in usuario[0] and len(cpf) == 11
    if cpf_e_senha_valida:
        print("Registro autorizado!")
        return True
    else:
        print("registro negado, cpf ou senha invalida!")
        return False
    
def validar_login(cpf, senha):
    if cpf in usuario[0] and usuario[1][usuario[0].index(cpf)] == senha:
        print("Login autorizado!")
        return True
    else:
        print("Login negado, cpf ou senha invalida!")
        return False

def criar_conta(cpf, senha, nome, data_de_nascimento, endereco):

    extrato_bancario.append([[],[],[],[]])
    saldo_e_quantia_de_saques.append([[0.0],[0]])
    usuario[0].append(cpf)
    usuario[1].append(senha)
    usuario[2].append(nome)
    usuario[3].append(data_de_nascimento)
    usuario[4].append(endereco)
    usuario[5].append(datetime.now())
    usuario[6].append(len(usuario[6])+1)
    usuario[7].append("0001")


def formatador_de_endereco():
    rua = input("NOME DA RUA:\n-->")
    numero = input("NÚMERO:\n-->")
    bairro = input("NOME DO BAIRRO:\n-->")
    cidade = input("NOME DA CIDADE:\n-->")
    estado = input("NOME DO ESTADO:\n-->")
    return rua, numero, bairro, cidade, estado

def formatador_de_data_de_nascimento():
    dia = input("DIA DA DATA DO SEU NASCIMENTO:\n-->")
    mes = input("MÊS DA DATA DO SEU NASCIMENTO:\n-->")
    ano = input("ANO DA DATA DO SEU NASCIMENTO:\n-->")
    return dia, mes, ano

while sistema == True:
    
    match tela:
        case 0:
            opcoes_menu_0 = ["1","2","3"]
            opcao = input(telas[tela])
            if opcao in opcoes_menu_0:
                match opcao:
                    case "1":                
                        cpf = input("CPF:\n-->")
                        senha = input("SENHA DE 8 DÍGITOS:\n-->")
                        if validar_login(cpf, senha) == True:
                            tela = 1
                            nome = usuario[2][usuario[0].index(cpf)]
                            index = usuario[0].index(cpf)

                    case "2":
                        nome = input("NOME:\n-->")
                        data_de_nascimento = formatador_de_data_de_nascimento()
                        cpf = input("CPF:\n-->")
                        senha = input("SENHA DE 8 DÍGITOS:\n-->")
                        endereco = formatador_de_endereco()
                        if validar_registro(cpf, senha) == True:
                            criar_conta(cpf, senha, nome, data_de_nascimento, endereco)
                            index = usuario[0].index(cpf)
                            tela = 1

                    case "3":
                        print("Fim do Programa")
                        exit()
            else:
                print("Opção invalida!")
        case 1:
            opcoes_menu_operacoes = ["1","2","3","4"]
            print(f"Bem vindo(a). {nome.upper()}!")
            opcao = input(telas[tela])
            if(opcao in opcoes_menu_operacoes):
                match opcao:
                    case "1" :
                        resposta_do_deposito = deposito(validador_de_valor_de_entrada(float(input("Valor do Deposito\n-->R$"))), usuario[0].index(cpf))
                        if resposta_do_deposito[0] == True:
                            saldo_e_quantia_de_saques[index][0][0] += resposta_do_deposito[1]
                    case "2" : 
                        resposta_do_saque = saque(validador_de_valor_de_entrada(float(input("Valor do Saque\n-->R$"))), saldo_e_quantia_de_saques[index][0][0], saldo_e_quantia_de_saques[index][1][0], usuario[0].index(cpf))
                        if resposta_do_saque[0] == True:
                            saldo_e_quantia_de_saques[index][0][0] -= resposta_do_saque[1]
                            saldo_e_quantia_de_saques[index][1][0] += 1
                    case "3" :
                        extrato(usuario[0].index(cpf), saldo_e_quantia_de_saques[index][0][0])
                    case "4" :
                        tela = 0

            else:
                print("Opção invalida! ")