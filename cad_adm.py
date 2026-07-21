# Bibliotecas

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print
from stdiomask import getpass
from hashlib import sha256
from time import sleep
import platform
import json
import os

# Variaveis

adms = []

local_script = os.path.dirname(os.path.abspath(__file__))

arquivo_json = os.path.join(local_script, "admins.json")

#region Caracteres para Senhas ↓

minusculas = "abcdefghijklmnopqrstuvwxyz"
maiusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numeros = "0123456789"
simbolos = '!@#$%^&*()-_=+[]{}|;:,.<>?/~'
caracters = minusculas + maiusculas + numeros + simbolos

#endregion

# Classes


class Adm:
    id = 1

    def __init__(self, admin, senha):
        self.id = Adm.id
        Adm.id += 1
        self.admin = admin
        self.__senha = senha

    def ver_admin(self):
        return self.admin

    def ver_senha(self):
        return self.__senha

    def alterar_admin(self, admin):
        self.admin = admin

    def alterar_senha(self, senha):
        self.__senha = senha


# Funções


def limpar_terminal():
    if platform.system() == "Windows":
        os.system("cls")

    else:
        os.system("clear")


def crip_senha(senha):
    return sha256(senha.encode()).hexdigest()


def validar_senha(senha):
    if len(senha) < 8:
        return False, "A senha deve ter no mínimo 8 caracteres."
    
    tem_minuscula = any(c in minusculas for c in senha)
    tem_maiuscula = any(c in maiusculas for c in senha)
    tem_numero = any(c in numeros for c in senha)
    tem_simbolo = any(c in simbolos for c in senha)
    
    if not (tem_minuscula and tem_maiuscula and tem_numero and tem_simbolo):
        return False, "A senha deve conter letras maiúsculas, minúsculas, números e símbolos."
    
    for caractere in senha:
        if caractere not in caracters:
            return False, f"O caractere '{caractere}' não é permitido na senha."
            
    return True, "Senha válida! Cadastro concluído."


def escrever_json():
    with open(arquivo_json, "w", encoding="utf-8") as arq:
        json.dump(adms, arq, indent=4, ensure_ascii=False)


def carregar_json():
    global adms

    try:
        with open(arquivo_json, "r", encoding="utf-8") as arq:
            adms = json.load(arq)

    except FileNotFoundError:
        escrever_json()


def achar_adm(adm):
    for i, item in enumerate(adms):
        if item["Admin"] == adm:
            return i
    return -1


def menu():
    print(Panel("|1| Cadastrar\n|2| Remover\n|3| Cadastrados\n|0| Sair", title="Menu", width=20))

    opc = int(input("Escolha uma Opção: "))
    return opc


def cadastrar():
    limpar_terminal()
    
    while True:
        admin = input("Digite um Nome de Usuário (|0| pra voltar!): ").strip()

        if admin == "0":
            return

        if not admin or not admin.isalpha():
            print("\nTipo de Usuário Invalido!")
            input("'Enter' para continuar...")
            limpar_terminal()
            continue

        idx = achar_adm(admin)

        if idx != -1:
            print("O Adm ja existe!")
            input("'Enter' para continuar...")
            limpar_terminal()
            continue

        senha = getpass(prompt="Crie uma Senha (8 Caracteres): ", mask="•").strip()

        valida, msg = validar_senha(senha)

        if not valida:
            print(f"Tipo de Senha Invalida! {msg}")
            input("'Enter' para continuar...")
            limpar_terminal()
            continue

        print("\nADM Criado com Sucesso!")
        input("'Enter' para continuar...")
        break

    adm = Adm(admin, crip_senha(senha))
    adms.append({"ID": adm.id, "Admin": adm.ver_admin(), "Senha": adm.ver_senha()})
    escrever_json()


def remover():
    limpar_terminal()
    
    if not adms:
        print("Lista de Admins Vazia!")
        return

    while True:
        admin = input("Admin a Remover (|0| para voltar!): ").strip()

        if admin == "0":
            return

        if not admin:
            limpar_terminal()
            continue
        break
        
    senha = getpass(prompt="Senha: ", mask="•")
    
    idx = achar_adm(admin)
        
    if idx != -1 and adms[idx]["Senha"] == crip_senha(senha):
        while True:
            remover = (
                input("Tem certeza que deseja excluir a conta? ([S] || [N]): ")
                .strip()
                .upper()
            )
            match remover:
                case "S":
                    adms.pop(idx)
                    escrever_json()
                    print("\nAdmin Removido com Sucesso!")
                    input("'Enter' para continuar...")
                    break

                case "N":
                    print("Voltando ao menu...")
                    sleep(1)
                    break

                case _:
                    limpar_terminal()
                    continue
    
    else:
        print("Admin ou Senha Invalida!")
        input("'Enter' para continuar...")


def cadastrados():
    limpar_terminal()
    console = Console()
    tb = Table(title="Admins")

    tb.add_column("ID")
    tb.add_column("Adms")
    for item in adms:
        tb.add_row(
            f"{item['ID']}",
            f"{item['Admin']}",
        )
    
    console.print(tb)
    
    input("'Enter' para continuar...")
    return


# Main

carregar_json()

while True:
    try:
        limpar_terminal()
        opcao = menu()

        match opcao:
            case 1:
                cadastrar()

            case 2:
                remover()

            case 3:
                cadastrados()

            case 0:
                print("Saindo...")
                sleep(1)
                limpar_terminal()
                break
            
            case _:
                print("Digite apenas uma das opções apresentadas!")
                input("'Enter' para continuar...")

    except ValueError as erro:
        print(erro)
        print("Digite apenas uma das opções apresentadas!")
        input("'Enter' para continuar...")
        continue