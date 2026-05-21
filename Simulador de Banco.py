#Calculadora de Gastos Pessoas!

import json
import os

# Nome do arquivo onde os dados serão salvos
ARQUIVO_DADOS = "dados_banco.json"

# --- FUNÇÕES DE PRESISTÊNCIA (SALVAR E CARREGAR) ---

def carregar_dados():
    '''Carrega os dadss do arquivo JSON. Se o arquivo não existir, define valores padrão'''

    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                return dados["saldo"], dados["investimentos"], dados["historico_gastos"]
        except (json.JSONDecodeError, KeyError):
            print("[Aviso] Erro ao ler o arquivo de dados. Iniciando com valores padrão.")

    # Valores iniciais padrão caso seja a primeira vez rodando o programa
    return 1000.00, 500.00, []

def salvar_dados():
    '''Salva o estado atual das variáveis no arquivo JSON.'''
    dados = {
        "saldo": saldo,
        "investimentos": investimentos,
        "historico_gastos": historico_gastos
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

# --- INICIALIZAÇÃO DOS DADOS ---
# o PROGRAMA COMEÇA CARREGANDO O QUE ESTAVA SALVO ANTERIORMENTE
saldo, investimentos, historico_gastos = carregar_dados()

# --- INTERFACE E FUNÇÕES DO BANCO ---

def exibir_menu():
    os.system('cls')
    print('''
    =========================================
               FEDRIGUISON BANK           
    =========================================
    [1] Consultar Saldo e Extrato
    [2] Registrar Ganho (Depósito/Salário)
    [3] Registrar Gasto (Categorias)
    [4] Transferir para Investimentos
    [5] Sair
    =========================================''')

def consultar_saldo():
    os.system('cls')
    global saldo, investimentos, historico_gastos
    print(f"\n--- SEU SALDO ATUAL ---")
    print(f"Conta Corrente: R$ {saldo:.2f}")
    print(f"Investimentos : R$ {investimentos:.2f}")
    
    print("\n--- ÚLTIMOS GASTOS REGISTRADOS ---")
    if not historico_gastos:
        print("Nenhum gasto registrado ainda.")
    else:
        for gasto in historico_gastos:
            print(f"- {gasto['categoria']}: R$ {gasto['valor']:.2f}")

def registrar_ganho():
    os.system('cls')
    global saldo
    print("\n--- REGISTRAR ENTRADA ---")
    try:
        valor = float(input("Digite o valor do depósito: R$ "))
        if valor > 0:
            saldo += valor
            salvar_dados()
            print(f"Sucesso! R$ {valor:.2f} adicionados à sua conta.")
        else:
            print("O valor precisa ser maior que zero.")
    except ValueError:
        print("Entrada inválida. Digite apenas números.")

def registrar_gastos():
    os.system('cls')
    global saldo, historico_gastos
    print("\n--- REGISTRAR GASTO ---")
    print("Escolha a categoria: \n[1] Habitação\n[2] Alimentação\n[3] Transporte\n[4] Lazer")
    
    op_cat = input("Digite a opção desejada: ").strip()
    categorias = {"1": "Habitação", "2": "Alimentação", "3": "Transporte", "4": "Lazer"}
    
    if op_cat in categorias:
        categoria_escolhida = categorias[op_cat]
        try:
            valor = float(input(f"Valor do gasto em {categoria_escolhida}: R$ "))
            if valor > 0:
                if valor <= saldo:
                    saldo -= valor
                    historico_gastos.append({"categoria": categoria_escolhida, "valor": valor})
                    salvar_dados()
                    print(f"Gasto de R$ {valor:.2f} registrado com sucesso!")
                else: 
                    print('Saldo insuficiente para realizar esse gasto.')
            else:
                print("O valor deve ser maior que zero.")
        except ValueError:
            print("Entrada inválida. Digite apenas números.")
    else:
        print("Categoria Inválida.")

def transferir_investimentos():
    os.system('cls')
    global saldo, investimentos
    print("\n--- APLICAR EM INVESTIMENTOS ---")
    try:
        valor = float(input("Quanto deseja transferir para investimentos? \nR$ "))
        if valor > 0:
            if valor <= saldo:
                saldo -= valor
                investimentos += valor
                salvar_dados()
                print(f"Sucesso! R$ {valor:.2f} aplicados com rendimento.")
            else:
                print("Saldo insuficiente na conta corrente.")
        else:
            print("O valor deve ser maior que zero.")
    except ValueError:
        print("Entrada inválida. Digite apenas números.")

# --- LOOP PRINCIPAL DO PROGRAMA ----
while True:
    exibir_menu()
    opcao = input("Digite o número da opção desejada: ").strip()

    if opcao == '1':
        consultar_saldo()
    elif opcao == '2':
        registrar_ganho()
    elif opcao == '3':
        registrar_gastos()
    elif opcao == '4':
        transferir_investimentos()
    elif opcao == '5':
        os.system('cls')
        print("==*==" * 14)
        print("Dados salvos com segurança. Obrigado por utilizar o Fedriguison Bank!")
        print("==*==" * 14)
        break
    else:
        print("\n[ERRO] Opção Inválida. Escolha um número de 1 a 5.")
    
    input("\nPressione ENTER para voltar ao menu...")