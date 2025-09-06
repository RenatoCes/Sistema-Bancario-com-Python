from datetime import datetime
menu_operacoes = """
1 - DEPOSITO
2 - SAQUE
3 - EXTRATO
4 - SAIR DA CONTA

-->"""

menu_inicial="""
1 - LOGIN
2 - REGISTRO
3 - SAIR DO APP

-->"""

saldo = 0.0
limite = 0.0
extrato_bancario = [[],[],[],[]]
email_senha_usuario = [[],[],[]]



def validador_de_valor_de_entrada(valor):
    if type(valor) is float and valor > 0:
        return valor
    elif type(valor) is int and valor > 0:
        return float(valor)
    else:
        return 0.0
    
def deposito(valor):
    if valor > 0 and extrato_bancario[1].count(datetime.now().strftime("%d/%m/%Y")) < 10:
        print(f"Deposio de R${valor:.2f} realizado.")
        return valor, True
    elif valor > 0 and extrato_bancario[1].count(datetime.now().strftime("%d/%m/%Y")) >= 10:
        print("Deposito negado, limite de tranzações realizadas.")
        return 0.0, False
    else:
        print("Deposito negado, tente novamente.")
        return 0.0, False

def saque(valor, saldo, quantia_de_saques_realizados_no_dia):
    saque_valido = valor <= saldo and valor > 0 and valor <= 500 and quantia_de_saques_realizados_no_dia < 3 and extrato_bancario[1].count(datetime.now().strftime("%d/%m/%Y")) < 10
    saque_limite_transacao = valor > 0 and valor > 500 and quantia_de_saques_realizados_no_dia < 3 and extrato_bancario[1].count(datetime.now().strftime("%d/%m/%Y")) < 10
    saque_limite_monetario = valor > 0 and valor > 500 and quantia_de_saques_realizados_no_dia < 3
    saque_limite_diario = valor > 0 and quantia_de_saques_realizados_no_dia >=3
    if saque_valido:
        print(f"Saque de R${valor:.2f} realizado.")
        return valor, True, 1
    elif saque_limite_transacao:
        print("Deposito negado, limite de tranzações realizadas.")
        return 0.0, False, 0
    elif saque_limite_monetario:
        print("O valor do saque inserido é maior do que o valor permitido.")
        return 0.0, False, 0
    elif saque_limite_diario:
        print("Saques negado, limite de saques atingido.")
        return 0.0, False, 0
    else:
        print("Saque negado, tente novamente.")
        return 0.0, False, 0

def acrescentar_no_extrato(valor, valor_deposito_saque):
    data_tempo = datetime.now()
    extrato_bancario[0].append(valor)
    extrato_bancario[1].append(data_tempo.strftime("%d/%m/%Y"))
    extrato_bancario[2].append(data_tempo.strftime("%H:%M:%S"))
    extrato_bancario[3].append(valor_deposito_saque)

def extrato():    
    for x in range(len(extrato_bancario[0])):
            if extrato_bancario[3][x] == True:
                print(f"Deposito de R${extrato_bancario[0][x]:.2f} data: {extrato_bancario[1][x]} horario: {extrato_bancario[2][x]}")
            else:
                print(f"Saque de R${extrato_bancario[0][x]:.2f} data: {extrato_bancario[1][x]} horario: {extrato_bancario[2][x]}")       
    print(f"saldo: R${saldo:.2f}")

def validar_registro(email, senha):
    email_senha_valida = email not in email_senha_usuario[0] and (email[-9:] == "gmail.com" or email[-11:] == "hotmail.com") and len(senha) == 8
    if email_senha_valida:
        print("Registro autorizado!")
        return True
    else:
        print("registro negado, email ou senha invalida!")
        return False
    
def validar_login(email, senha):
    if email in email_senha_usuario[0] and email_senha_usuario[0].index(email) == senha:
        print("Login autorizado!")
        return True
    else:
        print("Login negado, email ou senha invalida!")
        return False


    
    

def chamar_menu_operacoes(nome):
    opcoes_menu_operacoes = ["1","2","3","4"]
    nome_atual = nome
    print(f"Bem vindo {nome}")
    opcao = input(menu_operacoes)
    if(opcao in opcoes_menu_operacoes):
        match opcao:
            case "1" :
                deposito_extrato = deposito(validador_de_valor_de_entrada(float(input("Valor do Deposito\n-->R$"))))
                saldo += deposito_extrato[0]
                if deposito_extrato[1] == True:
                    saldo += deposito_extrato[0]
                    acrescentar_no_extrato(deposito_extrato[0], True)
                    chamar_menu_operacoes(nome_atual)
                else:
                    chamar_menu_operacoes(nome_atual)
            case "2" : 
                saque_saques_extrato= saque(validador_de_valor_de_entrada(float(input("Valor do Saque\n-->R$"))), saldo,quantia_de_saques_realizados_no_dia)
                saldo -= saque_saques_extrato[0]
                quantia_de_saques_realizados_no_dia += saque_saques_extrato[1]
                if saque_saques_extrato[2] == True:
                    acrescentar_no_extrato(saque_saques_extrato[0], False)
                    chamar_menu_operacoes(nome_atual)
                else:
                    chamar_menu_operacoes(nome_atual)
            case "3" :
                extrato()
                chamar_menu_operacoes(nome_atual)
            case "4" :
                chamar_menu_inicial()

    else:
        print("Opção invalida! ")
        chamar_menu_operacoes(nome)

def chamar_menu_inicial():
    opcoes_menu_inicial = ["1","2","3"]
    opcao = input(menu_inicial)
    if opcao in opcoes_menu_inicial:
        match opcao:
            case "1":                
                email = input("Email:\n-->")
                senha = input("Senha:\n-->")
                if validar_login(email, senha) == True:
                    chamar_menu_operacoes(email_senha_usuario[2][(email_senha_usuario[0].index(email))])
                else:
                    chamar_menu_inicial()

            case "2":
                nome = input("Nome:\n-->")
                email = input("Email:\n-->")
                senha = input("Senha:\n-->")
                if validar_registro(email, senha) == True:
                    email_senha_usuario[0].append(email)
                    email_senha_usuario[1].append(senha)
                    email_senha_usuario[2].append(nome)
                    print(email_senha_usuario)
                    chamar_menu_operacoes(nome)
                else:
                    chamar_menu_inicial()

            case "3":
                exit()
    else:
        print("Opção invalida!")
        chamar_menu_inicial()

chamar_menu_inicial()