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
saldo = 0.0
limite = 0.0
extrato_bancario = [[[],[],[],[]]]
email_senha_usuario = [["python@gmail.com"],["12345678"],["Python"]]
sistema = True
quantia_de_saques_realizados_no_dia = 0

def validador_de_valor_de_entrada(valor):
    if type(valor) is float and valor > 0:
        return valor
    elif type(valor) is int and valor > 0:
        return float(valor)
    else:
        return 0.0
    
def deposito(valor, index_email):
    if valor > 0 and extrato_bancario[index_email][1].count(datetime.now().strftime("%d/%m/%Y")) < 10:
        print(f"Deposio de R${valor:.2f} realizado.")
        acrescentar_no_extrato(valor, True, index_email)
        return True, valor
    elif valor > 0 and extrato_bancario[index_email][1].count(datetime.now().strftime("%d/%m/%Y")) >= 10:
        print("Deposito negado, limite de transações realizadas.")
        return False, 0
    else:
        print("Deposito negado, tente novamente.")
        return False, 0

def saque(valor, saldo, quantia_de_saques_realizados_no_dia, index_email):
    transacoes_do_dia = extrato_bancario[index_email][1].count(datetime.now().strftime("%d/%m/%Y"))
    saque_valido = valor <= saldo and valor > 0 and valor <= 500 and quantia_de_saques_realizados_no_dia < 3 and transacoes_do_dia < 10
    saque_limite_transacao = valor > 0 and valor > 500 and quantia_de_saques_realizados_no_dia < 3 and quantia_de_saques_realizados_no_dia  < 10
    saque_limite_monetario = valor > 0 and valor > 500 and quantia_de_saques_realizados_no_dia < 3
    saque_limite_diario = valor > 0 and quantia_de_saques_realizados_no_dia >=3
    if saque_valido:
        print(f"Saque de R${valor:.2f} realizado.")
        acrescentar_no_extrato(valor, False, index_email)
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

def acrescentar_no_extrato(valor, valor_positivo_negativo, index_email):
    data_tempo = datetime.now()
    extrato_bancario[index_email][0].append(valor)
    extrato_bancario[index_email][1].append(data_tempo.strftime("%d/%m/%Y"))
    extrato_bancario[index_email][2].append(data_tempo.strftime("%H:%M:%S"))
    extrato_bancario[index_email][3].append(valor_positivo_negativo)

def extrato(index_email):    
    for x in range(len(extrato_bancario[0])):
            if extrato_bancario[index_email][3][x] == True:
                print(f"Deposito de R${extrato_bancario[index_email][0][x]:.2f} data: {extrato_bancario[index_email][1][x]} horario: {extrato_bancario[index_email][2][x]}")
            else:
                print(f"Saque de R${extrato_bancario[index_email][0][x]:.2f} data: {extrato_bancario[index_email][1][x]} horario: {extrato_bancario[index_email][2][x]}")       
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
    if email in email_senha_usuario[0] and email_senha_usuario[1][email_senha_usuario[0].index(email)] == senha:
        print("Login autorizado!")
        return True
    else:
        print("Login negado, email ou senha invalida!")
        return False


while sistema == True:
    
    match tela:
        case 0:
            opcoes_menu_0 = ["1","2","3"]
            opcao = input(telas[tela])
            if opcao in opcoes_menu_0:
                match opcao:
                    case "1":                
                        email = input("Email:\n-->")
                        senha = input("Senha:\n-->")
                        if validar_login(email, senha) == True:
                            tela = 1
                            nome = email_senha_usuario[2][email_senha_usuario[0].index(email)]

                    case "2":
                        nome = input("Nome:\n-->")
                        email = input("Email:\n-->")
                        senha = input("Senha:\n-->")
                        if validar_registro(email, senha) == True:
                            email_senha_usuario[0].append(email)
                            email_senha_usuario[1].append(senha)
                            email_senha_usuario[2].append(nome)
                            extrato_bancario.append([[],[],[],[]])
                            tela = 1
                            print(email_senha_usuario, extrato_bancario)

                    case "3":
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
                        resposta_do_deposito = deposito(validador_de_valor_de_entrada(float(input("Valor do Deposito\n-->R$"))), email_senha_usuario.index(email))
                        if resposta_do_deposito[0] == True:
                            saldo += resposta_do_deposito[1]
                    case "2" : 
                        resposta_do_saque = saque(validador_de_valor_de_entrada(float(input("Valor do Saque\n-->R$"))), saldo, quantia_de_saques_realizados_no_dia, email_senha_usuario.index(email))
                        if resposta_do_saque[0] == True:
                            saldo -= resposta_do_saque[1]
                            quantia_de_saques_realizados_no_dia += 1
                    case "3" :
                        extrato(email_senha_usuario.index(email))
                    case "4" :
                        tela = 0

            else:
                print("Opção invalida! ")