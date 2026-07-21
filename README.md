# 🏦 Alpha Bank

> Sistema Bancário desenvolvido em Python com foco em Programação Orientada a Objetos, persistência de dados em JSON e interface interativa no terminal.

## 📖 Sobre o projeto

O **Alpha Bank** é um sistema bancário desenvolvido para praticar conceitos fundamentais de desenvolvimento de software utilizando Python.

O projeto simula operações bancárias através de um terminal interativo, permitindo o gerenciamento de contas, autenticação de administradores e armazenamento permanente dos dados.

Além das funcionalidades do sistema, o objetivo principal foi aplicar boas práticas de programação, organização de código e Programação Orientada a Objetos.

---

## 🚀 Tecnologias utilizadas

- Python 3
- Rich (Interface no Terminal)
- JSON
- Hashlib (Criptografia SHA-256)
- stdiomask
- Programação Orientada a Objetos (POO)

---

## 🧠 Conceitos aplicados

- ✔️ Herança
- ✔️ Encapsulamento
- ✔️ Classes e Objetos
- ✔️ Persistência de dados em JSON
- ✔️ Hash de senhas com SHA-256
- ✔️ Manipulação de arquivos
- ✔️ Tratamento de exceções
- ✔️ Menus interativos
- ✔️ Organização do código em funções

---

## ⚙️ Funcionalidades

### Área Administrativa

- Cadastro de titulares
- Remoção de contas
- Listagem de contas cadastradas
- Login de administrador
- Senhas criptografadas

### Área do Cliente

- Inserção e remoção de cartão
- Controle de saldo
- Estrutura preparada para:
  - Saques
  - Depósitos
  - Transferências

---

## 🔐 Segurança

O projeto utiliza criptografia SHA-256 para armazenar senhas, evitando que sejam salvas em texto puro.

Exemplo:

```
Senha original:
123456

Armazenada como:
8d969eef6ecad3c29a3a629280e686cff8ca...
```

---

## 💾 Armazenamento

Os dados são persistidos em arquivos JSON.

```
admins.json
contas.json
```

Assim, mesmo após fechar o programa, os cadastros permanecem salvos.

---

## 📂 Estrutura do projeto

```
AlphaBank/
│
├── main.py
├── contas.json
├── admins.json
└── README.md
```

---

## 📌 Melhorias futuras

- Implementar saque
- Implementar depósito
- Implementar transferência
- Consulta de saldo
- Extrato bancário
- Histórico de transações
- Interface gráfica
- Banco de dados SQL (PostgreSQL)

---

## ▶️ Como executar

Clone o repositório

```bash
git clone https://github.com/seuusuario/AlphaBank.git
```

Acesse a pasta

```bash
cd AlphaBank
```

Instale as dependências

```bash
pip install rich stdiomask
```

Execute

```bash
python main.py
```

---

## 📷 Preview

> Em breve serão adicionados GIFs e imagens demonstrando o funcionamento do sistema.

---

## 👨‍💻 Autor

**Jonathas Marrocos**

Estudante de Análise e Desenvolvimento de Sistemas.

Desenvolvendo projetos para consolidar conhecimentos em Python, Programação Orientada a Objetos e Banco de Dados.

GitHub:
https://github.com/JhonMarrocos
