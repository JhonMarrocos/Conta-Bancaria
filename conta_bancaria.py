# region Bibliotecas ↓

from rich.text import Text
from rich.table import Table
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
# endregion

# region Variaveis ↓

adm = []
contas = []
console = Console()

if getattr(sys, "frozen", False):
    local_script = os.path.dirname(
        sys.executable
    )  # Localiza o diretorio do programa se (execultavel)

else:
    local_script = os.path.dirname(
        os.path.abspath(__file__)
    )  # Localiza o diretorio do programa se (srcipt)

contas_json = os.path.join(local_script, "contas.json")

admins_json = os.path.join(local_script, "admins.json")
# endregion

# region Classes ↓


class ContaBancaria:
    def __init__(self, id=0, saldo=0):
        self.__id = id
        self.__saldo = saldo

    def exibir_id(self):
        return self.__id

    def alterar_id(self, id):
        self.__id = id

    def exibir_saldo(self):
        return self.__saldo

    def alterar_saldo(self, valor):
        self.__saldo = valor


class Titular(ContaBancaria):
    def __init__(self, id=0, saldo=0, usuario="", senha=""):
        super().__init__(id, saldo)
        self.__usuario = usuario
        self.__senha = senha

    def exibir_usuario(self):
        return self.__usuario

    def alterar_usuario(self, titular):
        self.__usuario = titular

    def exibir_senha(self):
        return self.__senha

    def alterar_senha(self, senha):
        self.__senha = senha

    def exibir_conta(self):
        return f"ID: {self.exibir_id()}, Titular: {self.exibir_usuario()}, Saldo: R${self.exibir_saldo():.2f}"

    def sacar(self, valor):

        if valor <= 0:
            return "Valor Invalido!"

        elif valor <= self.exibir_saldo():
            self.alterar_saldo(self.exibir_saldo() - valor)
            return f"Você sacou R${valor:.2f}, seu novo saldo e de R${self.exibir_saldo():.2f}"

        else:
            return f"Valor do saque acima do seu saldo R${self.exibir_saldo():.2f}"

    def depositar(self, valor):

        if valor <= 0:
            return "Valor Invalido!"

        else:
            self.alterar_saldo(self.exibir_saldo() + valor)
            return f"Você depositou R${valor:.2f}, seu novo saldo e de R${self.exibir_saldo():.2f}"

    def transferir(self, conta, valor):

        if valor <= 0:
            return "Valor Invalido!"

        if valor <= self.exibir_saldo():
            self.alterar_saldo(self.exibir_saldo() - valor)
            conta.alterar_saldo(conta.exibir_saldo() + valor)

        else:
            return f"Valor de transferencia acima do seu saldo R${self.exibir_saldo():.2f}"

# endregion

# region Funcões ↓


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


def cor_destaque(texto):  # Converte um Texto em uma msg em destaque piscando em verde
    with Live("", refresh_per_second=20) as live:
        cores = ["[rgb(0,85,0)]", "[rgb(0,170,0)]", "[rgb(0,255,0)]"]
        for i in range(5):
            for cor in cores:
                live.update(f"{cor}{texto}[/]")
                sleep(0.1)


def continuar():
    Prompt.ask("Aperte [cyan]ENTER[/] para continuar")
    limpar_terminal()


def criptografar(senha):
    return sha256(str(senha).encode()).hexdigest()


def escrever_json():
    with open(contas_json, "w", encoding="utf-8") as arq:
        json.dump(contas, arq, indent=4, ensure_ascii=False)


def carregar_json():
    global contas

    try:
        with open(contas_json, "r", encoding="utf-8") as arq:
            contas = json.load(arq)

    except FileNotFoundError:
        escrever_json()


def carregar_adm():
    global adm

    try:
        with open(admins_json, "r", encoding="utf-8") as arq:
            adm = json.load(arq)

    except FileNotFoundError:
        print("Nenhum Admin Cadastrado!")
        continuar()
        return 0


def encontrar_titular(titular):
    for i, item in enumerate(contas):
        if item["Titular"] == titular:
            return i
    return -1


def logar_titular():
    if not contas:
        cor_alerta("[white]A lista de Contas está[/] Vazia!")
        continuar()
        return 0

    while True:
        titular = str(input('Titular da Conta ([0] para voltar): ')).title().strip()
        
        if titular == '0':
            return 0
        
        elif not titular:
            limpar_terminal()
            continue
        
        senha = getpass(prompt='Digite sua Senha: ', mask='•')
        
        idx = encontrar_titular(titular)

        if idx != -1 and contas[idx]["Senha"] == criptografar(senha):
            cor_destaque(f"[cyan]Seja Bem Vindo![/] {titular}")
            continuar()
            break

        else:
            cor_alerta("[white]Titular ou Senha[/] Invalida!")
            continuar()
            continue
    
    return titular


def encontrar_adm(admin):
    for i, item in enumerate(adm):
        if item["Admin"] == admin:
            return i
    return -1


def verificar_adm():
    if not adm:
        cor_alerta("[white]A lista de Admins está[/] Vazia!")
        continuar()
        return
    
    while True:
        login = str(input("Admin ([0] para voltar): ")).strip().title()
        
        if login == '0':
            limpar_terminal()
            return 0

        if not login:
            limpar_terminal()
            continue

        senha = getpass(prompt="Senha: ", mask="•")

        idx = encontrar_adm(login)

        if idx != -1 and adm[idx]["Senha"] == criptografar(senha):
            cor_destaque(f"[cyan]Seja Bem Vindo![/] {login}")
            continuar()
            break

        else:
            cor_alerta("[white]Usuario ou Senha[/] Invalida!")
            continuar()
            return 0


def menu_principal():
    print(
        Panel(
            """\n|[cyan]1[/]|[white]:mag_right: Verificar Saldo[/]  [[white]Aperte[/] |[rgb(0,255,0)]9[/]| [white]menu[/] [rgb(0,200,0)]ADM[/]]\n|[cyan]2[/]|[white]:dollar: Sacar[/]\n|[cyan]3[/]|[white]:moneybag: Depositar[/]\n|[cyan]4[/]|[white]:money_with_wings: Transferir[/]\n|[red]0[/]|[red]:x: Sair[/]\n""",
            title="[cyan]A[/][white]LPHA[/] [rgb(160,0,160)]B[/][white]ANK[/] :bank:",
            style="rgb(180,0,135)",
            width=50,
        )
    )
    opc = int(input("Opção: "))
    return opc


def verificar_saldo():
    limpar_terminal()
    logar = logar_titular()

    if logar == 0:
        return 0
    
    titular = Titular()
    
    for i, item in enumerate(contas):
        if item["Titular"] == logar:
            titular.alterar_id(item["ID"])
            titular.alterar_usuario(item["Titular"])
            titular.alterar_senha(item["Senha"])
            titular.alterar_saldo(item["Saldo"])

        console.print(Panel(Text.from_markup(f'[green]R$[/] [white]{titular.exibir_saldo():.2f}[/]', justify="center"), title="[green]Saldo[/] :dollar:", style="rgb(180,0,135)", width=30))
        continuar()


def sacar():
    input('Em Breve...')
    pass


def depositar():
    input('Em Breve...')
    pass


def transferir():
    input('Em Breve...')
    pass


def menu_adm():
    print(
        Panel(
            """\n|[cyan]1[/]|[white]:writing_hand:  Cadastrar Titular[/]\n|[cyan]2[/]|[white] :wastebasket: Remover Titular[/]\n|[cyan]3[/]|[white]:clipboard: Lista de Contas[/]\n|[yellow]0[/]|[yellow]:back: Menu Anterior[/]\n""",
            title="[rgb(0,200,0)]=ADM=[/]",
            style="rgb(180,0,135)",
            width=30,
        )
    )
    opc = int(input("Opção: "))
    return opc


def cadastrar():
    limpar_terminal()

    while True:
        usuario = (
            str(input("Digite o Nome do Titular ([0] para sair!): ")).strip().title()
        )

        if usuario == "0":
            limpar_terminal()
            return

        if not usuario:
            limpar_terminal()
            continue

        elif usuario.isnumeric():
            cor_alerta("\n[white]Nome[/] Invalido!")
            continuar()
            continue

        achar = encontrar_titular(usuario.title())

        if achar != -1:
            cor_alerta("[white]O Titular já[/] existe!")
            continuar()
            continue

        break

    while True:
        try:
            senha = int(
                getpass(
                    prompt="Cadastre uma senha de 6 Digitos ([0] para sair!): ",
                    mask="•",
                )
            )
            if senha == 0:
                limpar_terminal()
                return

            if not senha:
                limpar_terminal()
                continue

            elif len(str(senha)) != 6:
                cor_alerta("[white]Forma de Senha[/] Invalida!")
                print("A senha deve conter apenas 6 digitos!")
                continuar()
                continue

        except ValueError as erro:
            cor_alerta(
                f"[white]Digite Apenas[/] [green]Numeros![/]\n[yellow]ERRO: {erro}"
            )
            continuar()
            continue
        break
    titular = Titular(id=1, usuario=usuario, senha=criptografar(senha))

    id_atual = titular.exibir_id()

    for i, item in enumerate(contas):
        if item["ID"] >= id_atual:
            id_atual = item["ID"] + 1

    contas.append(
        {
            "ID": id_atual,
            "Titular": titular.exibir_usuario(),
            "Senha": titular.exibir_senha(),
            "Saldo": round(float(titular.exibir_saldo()), 2),
        }
    )

    escrever_json()
    cor_destaque("[white]Conta Cadastrada Com[/] Suscesso!")
    continuar()


def remover():
    if not contas:
        cor_alerta("[white]A lista de Contas está[/] Vazia!")
        continuar()
        return

    limpar_terminal()
    while True:
        try:
            achar_id = int(
                input("Qual ID você gostaria de remover? ([0] para sair!): ")
            )

            if achar_id == 0:
                limpar_terminal()
                return

            if not achar_id:
                limpar_terminal()
                continue

            while True:
                cor_destaque(
                    "[white]Antes de Remover, e recomendado que o[/] [cyan]Titular[/] [white]saque seu[/] saldo!"
                )
                sleep(1)

                escolha = (
                    str(
                        input(
                            "Tem certeza que deseja excluir a conta? ([S]Sim | [N] Não) "
                        )
                    )
                    .strip()
                    .upper()
                )

                match escolha:
                    case "S":
                        break

                    case "N":
                        print("Voltando ao Menu...")
                        sleep(1)
                        limpar_terminal()
                        return

                    case _:
                        limpar_terminal()
                        continue

            for i, item in enumerate(contas):
                if item["ID"] == achar_id:
                    cor_destaque(
                        f"[white]Titular[/] {item['Titular']} [white]Removido com[/] [cyan]Sucesso![/]"
                    )
                    contas.pop(i)
            escrever_json()
            continuar()

        except ValueError as erro:
            limpar_terminal()
            cor_alerta(f"[white]Digite um ID Valido![/]\n[yellow]Erro:[/] {erro}")
            continuar()
            continue
        break


def lista_contas():
    if not contas:
        cor_alerta("[white]A lista de Contas está[/] Vazia!")
        continuar()
        return

    limpar_terminal()

    tabela = Table(title="[white bold]Contas[/]", style="rgb(180,0,135)")

    tabela.add_column("[rgb(180,0,135)]ID[/]", justify="center")
    tabela.add_column("[blue]Titular[/]", justify="center")
    tabela.add_column("[green]Saldo[/]", justify="center")

    for i, item in enumerate(contas):
        tabela.add_row(
            f"[cyan]{item['ID']}[/]",
            f"[white]{item['Titular']}[/]",
            f"[green]R$[/] [white]{item['Saldo']:.2f}[/]",
        )

    console.print(tabela)
    continuar()


# endregion

# region Main ↓

limpar_terminal()
loading()
carregar_json()
sleep(1)

while True:
    try:
        limpar_terminal()
        opcao_mp = menu_principal()

        match opcao_mp:
            case 1:
                verificar = verificar_saldo()

                if verificar == 0:
                    continue

                continue

            case 2:
                input('Em Breve...')
                pass

            case 3:
                input('Em Breve...')
                pass

            case 4:
                input('Em Breve...')
                pass

            case 9:
                limpar_terminal()
                tentativa = carregar_adm()

                if tentativa == 0:
                    continue

                altenticar = verificar_adm()

                if altenticar == 0:
                    continue

                while True:
                    opcao_madm = menu_adm()

                    match opcao_madm:
                        case 1:
                            cadastrar()
                            continue

                        case 2:
                            remover()
                            continue

                        case 3:
                            lista_contas()
                            continue

                        case 0:
                            break

                        case _:
                            cor_alerta(
                                f"[white]A Opção[/] [cyan]{opcao_madm}[/] não existe!"
                            )
                            continuar()
                            continue

            case 0:
                limpar_terminal()
                print("Saindo...")

                with Live("", refresh_per_second=20) as live:
                    tchau = [":hand:", ":wave:"]
                    for v in range(3):
                        for i in tchau:
                            live.update(f"Ate Mais!{i}")
                            sleep(0.3)
                break

            case _:
                cor_alerta(f"[white]A Opção[/] [cyan]{opcao_mp}[/] não existe!")
                continuar()

    except ValueError as erro:
        limpar_terminal()
        cor_alerta(
            f"[cyan]Digite Somente uma das Opções Apresentadas![/]\n[yellow]Erro:[/] {erro}"
        )
        continuar()
# endregion

limpar_terminal()
