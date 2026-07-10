# Bibliotecas ↓

from rich.live import Live
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Prompt
from rich import print

from stdiomask import getpass
from hashlib import sha256

from time import sleep
import platform
import os
import sys
import json

# Variaveis ↓

contas = []

if getattr(sys, "frozen", False):
    local_script = os.path.dirname(
        sys.executable
    )  # Localiza o diretorio do programa se (execultavel)

else:
    local_script = os.path.dirname(
        os.path.abspath(__file__)
    )  # Localiza o diretorio do programa se (srcipt)

arquivo_json = os.path.join(local_script, "contas.json")

# Funcões ↓


def limpar_terminal():
    if platform.system() == "Windows":
        os.system("cls")

    else:
        os.system("clear")


def loading():  # Barra de Loading similar ao usando no tqdm
    with Live("", refresh_per_second=30) as live:
        for n in range(101):
            i = "■" * (n * 25 // 101)
            if n < 33:
                live.update(f"|{n}%|[[rgb(200,0,200)]{i}[/]]")

            else:
                live.update(f"|{n}%|[[rgb(200,0,200)]{i}[/]]")

            sleep(0.01)
        live.update(f"|{n}%|[[rgb(200,0,200)]{i}[/]]")


def cor_alerta(texto):  # Converte um Texto em uma msg de alerta piscando em vermelho
    with Live("", refresh_per_second=20) as live:
        cores = ["[rgb(85,0,0)]", "[rgb(170,0,0)]", "[rgb(255,0,0)]"]
        for i in range(10):
            for cor in cores:
                live.update(f"{cor}{texto}[/]")
                sleep(0.05)


def continuar():
    Prompt.ask("Aperte [cyan]ENTER[/] para continuar")
    limpar_terminal()


def criptografar(senha):
    return sha256(senha.encode()).hexdigest()


def escrever_json():
    with open(arquivo_json, "w", encoding="utf-8") as arq:
        json.dump(contas, arq, indent=4, ensure_ascii=False)


def carregar_json():
    global contas

    try:
        with open(arquivo_json, "r", encoding="utf-8") as arq:
            contas = json.load(arq)

    except FileNotFoundError:
        escrever_json()


def menu_principal():
    while True:
        print(
            Panel(
                """|[cyan]1[/]| [white]:desktop_computer: Acessar Conta[/]   ([white]Aperte[/] '[green]+[/]' [white]para ADM[/])
|[cyan]2[/]| [white]:dollar: Sacar[/]
|[cyan]3[/]| [white]:moneybag: Depositar[/]
|[cyan]4[/]| [white]:money_with_wings: Transferir[/]
|[red]0[/]| [red]:x: Sair[/]""",
                title="[cyan]A[/][white]LPHA[/] [rgb(160,0,160)]B[/][white]ANK[/] :bank:",
                style="rgb(180,0,135)",
                width=50,
            )
        )
        opc = input("Opção: ").strip()

        if opc == "+":
            break

        elif not opc.isdecimal() or len(opc) != 1:
            cor_alerta("[white]Opção[/] Invalida!")
            continuar()
            continue
        break
    
    return opc

# Classes ↓


class Conta_Bancaria:
    _proximo_id = 1

    def __init__(self, saldo=0):
        self.__id = Conta_Bancaria._proximo_id
        Conta_Bancaria._proximo_id += 1
        self.__saldo = saldo

    def exibir_id(self):
        return self.__id

    def exibir_saldo(self):
        return self.__saldo

    def alterar_saldo(self, valor):
        self.__saldo = valor


class Titular(Conta_Bancaria):
    def __init__(self, saldo=0, email="", usuario="", senha=""):
        super().__init__(saldo)
        self.__email = email
        self.__usuario = usuario
        self.__senha = senha
        self.__cartao_inserido = False

    def exibir_email(self):
        return self.__email

    def exibir_usuario(self):
        return self.__usuario

    def exibir_conta(self):
        print(
            f"ID: {self.exibir_id()}, Email: {self.exibir_email()}, Titular: {self.exibir_usuario()}, Saldo: R${self.exibir_saldo():.2f}"
        )

    def validar_senha(self):
        while True:
            senha = input("Senha: ").strip()

            if not senha.isnumeric() or senha != self.__senha:
                print("Senha Invalida!")
                continue

            break

    def inserir_cartao(self):
        self.__cartao_inserido = True
        return self.__cartao_inserido

    def remover_cartao(self):
        self.__cartao_inserido = False
        return self.__cartao_inserido

    def cartao_ativo(self):
        return self.__cartao_inserido

    def sacar(self, valor):
        if self.cartao_ativo():
            print(f"Bem Vindo {self.exibir_usuario()}!")

            self.validar_senha()

            if valor <= 0:
                print("Valor Invalido!")

            if valor <= self.exibir_saldo():
                self.alterar_saldo(self.exibir_saldo() - valor)
                print(
                    f"Você sacou R${valor:.2f}, seu novo saldo e de R${self.exibir_saldo():.2f}"
                )
            else:
                print(f"Valor do saque acima do seu saldo R${self.exibir_saldo():.2f}")

        else:
            print("Insira o Cartão Para Sacar!")

    def depositar(self, valor):
        print(f"Bem Vindo {self.exibir_usuario()}!")

        self.validar_senha()

        if self.cartao_ativo():
            if valor <= 0:
                print("Valor Invalido!")

            else:
                self.alterar_saldo(self.exibir_saldo() + valor)
                print(
                    f"Você depositou R${valor:.2f}, seu novo saldo e de R${self.exibir_saldo():.2f}"
                )

        else:
            print("Insira o Cartão Para Depositar!")


# Main ↓
loading()
sleep(1)
menu_principal()

# titular1 = Titular(email="exemplo1@gmail.com", usuario="Exemplo 1", senha="09072026")
# titular2 = Titular(email="exemplo2@gmail.com", usuario="Exemplo 2", senha="09072026")
# titular3 = Titular(email="exemplo3@gmail.com", usuario="Exemplo 3", senha="09072026")

# loading()

# titular1.exibir_conta()
# titular2.exibir_conta()
# titular3.exibir_conta()

# titular1.inserir_cartao()
# titular1.depositar(500)
# titular1.sacar(200)
