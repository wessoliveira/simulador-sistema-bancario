import textwrap
from datetime import datetime
from abc import ABC, abstractmethod

LARGURA_PRINT = 80
AGENCIA = "0001-1"

def menu():

    menu = f"""
    {" Menu ".center(LARGURA_PRINT, "=")}
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    [u] Criar Usuário
    [l] Listar Usuários
    [c] Criar Conta
    [k] Listar Contas
    => """
    return input(textwrap.dedent(menu))

class Cliente:
    def __init__(self, endereco, conta=None):
        self._endereco = endereco
        self._contas = []
        if conta:
            self._contas.append(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    @property
    def endereco(self):
        return self._endereco
    
    @property
    def contas(self):
        return self._contas

    def __str__(self):
        stringa = f"""{"Cliente".center(30, "-")}
        Endereço: {self._endereco}
        Contas: {len(self._contas)}"""
        return textwrap.dedent(stringa)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco, conta=None):
        super().__init__(endereco, conta)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y").date()

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    def __str__(self):
        stringa = f"""
        {"PessoaFisica".center(30, "-")}
        CPF: {self._cpf}
        Nome: {self._nome}
        Nascimento: {self._data_nascimento}
        Endereço: {self._endereco}
        Contas: {len(self._contas)}"""
        return textwrap.dedent(stringa)

class Conta:
    def __init__(self, numero, agencia, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(cls, cliente, numero):
        conta = cls(numero, AGENCIA, cliente)
        return conta
    
    def sacar(self, valor):
        if valor > self._saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@\n")
        elif valor <= 0:
            print("\n@@@ Operação falhou! Informe um número maior que zero. @@@\n")
        else:
            self._saldo -= valor
            return True
        return False

    def depositar(self, valor):
        if valor <= 0:
            return False
        self._saldo += valor
        return True

    def __str__(self):
        stringa = f"""
        {"Conta".center(30, "-")}
        Saldo: {self._saldo}
        Número: {self._numero}
        Agência: {self._agencia}
        Cliente: {self._cliente}
        Histórico: {len(self._historico._transacoes)}"""
        return textwrap.dedent(stringa)

class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite=500, limite_saques=3):
        super().__init__(numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    def sacar(self, valor):
        saques_realizados_hoje = [
            t for t in self._historico._transacoes 
            if t["data_transacao"].date() == datetime.now().date() and isinstance(t["transacao"], Saque)
            ]
        if valor > self._limite:
            print(f"\n@@@ Operação falhou! O valor informado é maior que o limite de R$ {self._limite:.2f}. @@@\n")
        elif len(saques_realizados_hoje) >= self._limite_saques:
            print(f"\n@@@ Operação falhou! Número máximo de saques diários ({self._limite_saques}) atingido. @@@\n")
            return False
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        stringa = f"""
        {"ContaCorrente".center(30, "-")}
        Saldo: {self.saldo}
        Número: {self._numero}
        Agência: {self._agencia}
        Cliente: {self._cliente._nome}
        Histórico: {len(self._historico._transacoes)}
        Limite: {self._limite}
        Limite de Saques: {self._limite_saques}"""
        return textwrap.dedent(stringa)

class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        deposito_ok = conta.depositar(self._valor)
        if deposito_ok:
            print(f"\n=== Depósito de R$ {self._valor:.2f} realizado com sucesso! ===\n")
            conta.historico.adicionar_transacao(self)
        else:
            print("\n@@@ Operação falhou! Informe um número maior que zero. @@@\n")
    
    def __str__(self): 
        return f"Depósito:\t R$ {self._valor:.2f}"

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        saque_ok = conta.sacar(self._valor)
        if saque_ok:
            print(f"\n=== Saque de R$ {self._valor:.2f} realizado com sucesso! ===\n")
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"Saque:\t\t R$ {self._valor:.2f}"

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append({"transacao": transacao, "data_transacao": datetime.now()})

    def __str__(self):
        return "\n\n".join(
            str(t["transacao"]) + 
            f"\n\t\t{t['data_transacao'].strftime('%d/%m/%Y %H:%M:%S')}" 
            for t in self._transacoes
            ) or "Não foram realizadas movimentações." 

def criar_usuario(lista_usuarios):
    cpf = input("Informe o CPF (apenas números): ")
    lista_busca = [u for u in lista_usuarios if u.cpf == cpf]
    if lista_busca:
        print("\n@@@ Usuário já existe! @@@")
    else:
        nome = input("Informe o nome: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        usuario = PessoaFisica(cpf, nome, data_nascimento, endereco)
        lista_usuarios.append(usuario)
        print("\n=== Usuário criado com sucesso! ===")

def listar_usuarios(lista_usuarios):
    print("\n", " Lista de Usuários ".center(LARGURA_PRINT, "="), sep="")
    for u in lista_usuarios:
        info_usuario = f"""
        {"-" * (LARGURA_PRINT - 2)}
        CPF: {u.cpf}
        Nome: {u.nome}
        Data de Nascimento: {u.data_nascimento.strftime('%d/%m/%Y')}
        Endereço: {u.endereco}
        Contas: {len(u.contas)}"""
        print(textwrap.dedent(info_usuario))
    print("\n" + "=" * LARGURA_PRINT)

def criar_conta(lista_usuarios, sequencia_contas):
    numero_conta = sequencia_contas + 1
    cpf = input("Informe o CPF do usuário: ")
    cli = [u for u in lista_usuarios if u.cpf == cpf]
    if cli:
        conta = ContaCorrente.nova_conta(cli[0], numero_conta)
        cli[0].adicionar_conta(conta)
        print("\n=== Conta criada com sucesso! ===")
        return numero_conta
    else:
        print("\n@@@ Usuário não encontrado, por favor verifique o CPF informado. @@@")
        return sequencia_contas

def listar_contas(lista_usuarios):
    print("\n", " Lista de Contas ".center(LARGURA_PRINT, "="), sep="")
    
    for u in lista_usuarios:
        for c in u.contas:
            info_conta = f"""
            {"-" * (LARGURA_PRINT - 2)}
            Agência:\t\t {c.agencia}
            Conta:\t\t\t {c.numero}
            Cliente:\t\t {c.cliente.nome}
            CPF:\t\t\t {c.cliente.cpf}"""
            info_conta_adicional = ""
            if isinstance(c, ContaCorrente):
                info_conta_adicional = f"""
                Limite:\t\t\t R$ {c.limite:.2f}
                Limite Qtd. Saques:\t {c.limite_saques}
                """
            print(textwrap.dedent(info_conta), textwrap.dedent(info_conta_adicional))
    print("\n" + "=" * LARGURA_PRINT)


def mostrar_extrato(conta):
    print("\n", " Extrato ".center(LARGURA_PRINT, "="), sep="")
    print(conta.historico)
    print(f"\nSaldo:\t\t R$ {conta.saldo:.2f}")
    print("=" * LARGURA_PRINT)

def main(objeto = None):
    lista_usuarios = objeto[0].copy() if objeto is not None else []
    sequencia_contas = objeto[1] if objeto is not None else 0

    while True:

        opcao = menu()

        if opcao == "s":
            if len(lista_usuarios) == 0:
                print("\n@@@ Nenhum usuário cadastrado. Por favor, crie um usuário antes de realizar um saque. @@@")
                continue
            
            cpf = input("Informe o CPF do usuário: ")
            cli = [u for u in lista_usuarios if u.cpf == cpf]
            if cli:
                if len(cli[0].contas) == 0:
                    print("\n@@@ Usuário não possui contas cadastradas. @@@")
                else:
                    valor_saque = round(float(input("Informe o valor do saque: ")), 2)
                    cli[0].realizar_transacao(cli[0].contas[0], Saque(valor_saque))
            else:
                print("\n@@@ Usuário não encontrado, por favor verifique o CPF informado. @@@")

        elif opcao == "d":
            if len(lista_usuarios) == 0:
                print("\n@@@ Nenhum usuário cadastrado. Por favor, crie um usuário antes de realizar um depósito. @@@")
                continue
            cpf = input("Informe o CPF do usuário: ")
            cli = [u for u in lista_usuarios if u.cpf == cpf]
            if cli:
                if len(cli[0].contas) == 0:
                    print("\n@@@ Usuário não possui contas cadastradas. @@@")
                else:
                    valor_deposito = round(float(input("Informe o valor do depósito: ")), 2)
                    cli[0].realizar_transacao(cli[0].contas[0], Deposito(valor_deposito))
            else:
                print("\n@@@ Usuário não encontrado, por favor verifique o CPF informado. @@@")

        elif opcao == "e":
            if len(lista_usuarios) == 0:
                print("\n@@@ Nenhum usuário cadastrado. Por favor, crie um usuário antes de exibir o extrato. @@@")
                continue
            cpf = input("Informe o CPF do usuário: ")
            cli = [u for u in lista_usuarios if u.cpf == cpf]
            if cli:
                if len(cli[0].contas) == 0:
                    print("\n@@@ Usuário não possui contas cadastradas. @@@")
                else:
                    mostrar_extrato(cli[0].contas[0])
            else:
                print("\n@@@ Usuário não encontrado, por favor verifique o CPF informado. @@@")

        elif opcao == "u":
            criar_usuario(lista_usuarios)

        elif opcao == "l":
            if len(lista_usuarios) == 0:
                print("\n@@@ Nenhum usuário cadastrado. Por favor, crie um usuário antes de listar os usuários. @@@")
                continue
            listar_usuarios(lista_usuarios)

        elif opcao == "c":
            if len(lista_usuarios) == 0:
                print("\n@@@ Nenhum usuário cadastrado. Por favor, crie um usuário antes de criar uma conta. @@@")
                continue
            sequencia_contas = criar_conta(lista_usuarios, sequencia_contas)

        elif opcao == "k":
            if len(lista_usuarios) == 0:
                print("\n@@@ Nenhum usuário cadastrado. Por favor, crie um usuário antes de listar as contas. @@@")
                continue
            listar_contas(lista_usuarios)

        elif opcao == "q":
            print("Sair...")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")
    return (lista_usuarios, sequencia_contas)

def simular_sistema():
    sistema = main()
    return sistema

def continuar_simulacao(sistema_anterior):
    sistema = main(sistema_anterior)
    return sistema
