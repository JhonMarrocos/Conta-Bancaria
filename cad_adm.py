# Bibliotecas

from stdiomask import getpass
from hashlib import sha256
import platform
import json
import os

# Variaveis

adms = []

local_script = os.path.dirname(os.path.abspath(__file__))

arquivo_json = os.path.join(local_script, "admins.json")

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


def cadastrar():
    while True:
        print(10 * "=", "Cadastro de Admin", 10 * "=")
        print()
        admin = input("Digite um Usuário: ").strip()

        if not admin or not admin.isalpha():
            print("Usuário Invalido!")
            continue

        senha = getpass(prompt="Crie uma Senha (8 Caracteres): ", mask="•").strip()

        if not senha or len(senha) < 8:
            print("Senha Invalida!")
            continue

        print("ADM Criado com Sussesso!")
        break

    adm = Adm(admin, crip_senha(senha))
    adms.append({"ID": adm.id, "Admin": adm.ver_admin(), "Senha": adm.ver_senha()})
    escrever_json()


# Main

limpar_terminal()
cadastrar()

for item in adms:
    print(f"|{item['ID']}| - {item['Admin']}")
