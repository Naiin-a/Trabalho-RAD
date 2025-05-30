class Cadastro:
    nome = ""
    email = ""
    login = ""
    senha = ""
    cpf = ""
    numeroAp = int
    bloco = int

    def __init__(self, cpf, login, nome, senha, bloco, numeroAp, email, data_cadastro):
        self.cpf = cpf
        self.login = login
        self.nome = nome
        self.__senha = senha  # privado
        self.bloco = bloco
        self.numeroAp = numeroAp
        self.email = email
        self.data_cadastro = data_cadastro

    def get_senha(self):
        return self.__senha

    def set_senha(self, senha):
        self.__senha = senha


class Cadastro_adm:
    nome = ""
    login = ""
    senha = ""
    cpf = ""


    def __init__(self, cpf, login, nome, senha, data_cadastro):
        self.cpf = cpf
        self.login = login
        self.nome = nome
        self.__senha = senha  # privado
        self.data_cadastro = data_cadastro

    def get_senha(self):
        return self.__senha

    def set_senha(self, senha):
        self.__senha = senha

