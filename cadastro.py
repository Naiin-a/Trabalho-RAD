class Cadastro:
    nome = ""
    email = ""
    login = ""
    senha = ""
    cpf = ""
    numeroAp = int
    bloco = int

    def __init__(self, cpf, login, nome, senha, bloco, numeroAp, email):
        self.cpf = cpf
        self.login = login
        self.nome = nome
        self.__senha = senha  # privado
        self.bloco = bloco
        self.numeroAp = numeroAp
        self.email = email

    def get_senha(self):
        return self.__senha

    def set_senha(self, senha):
        self.__senha = senha