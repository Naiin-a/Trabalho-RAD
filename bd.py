import sqlite3
import os
from cadastro import Cadastro
class BancoDeDados:
        def __init__(self, nome_banco="banco.sqlite"):
            self.nome_banco = os.path.join(os.path.dirname(__file__), nome_banco)
            self.conn = None

        def conectar(self):
            try:
                self.conn = sqlite3.connect(self.nome_banco)
            except sqlite3.Error as e:
                print(f"Erro ao conectar ao banco de dados: {e}")

        def criar_tabelas(self):
            self.cadastrar()


        def cadastrar(self):
            if self.conn:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute(
                        """CREATE TABLE IF NOT EXISTS Pessoa(
                        cpf INTEGER PRIMARY KEY,
                        nome TEXT NOT NULL,
                        login TEXT NOT NULL UNIQUE,
                        senha TEXT NOT NULL,
                        bloco INTEGER,
                        numeroAp INTEGER,
                        email TEXT NOT NULL UNIQUE
                        )"""
                    )
                    self.conn.commit()
                except sqlite3.Error as e:
                    print(f"Erro ao criar tabela Pessoa: {e}")

        def inserir_pessoa(self, pessoa: Cadastro):
            if self.conn:
                try:
                    cursor = self.conn.cursor()
                    cursor.execute(
                        "INSERT INTO Pessoa (cpf, nome, login, senha, bloco, numeroAp, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (pessoa.cpf, pessoa.nome, pessoa.login, pessoa.get_senha(), pessoa.bloco, pessoa.numeroAp,
                         pessoa.email)
                    )
                    self.conn.commit()
                    print("Pessoa inserida com sucesso!")
                except sqlite3.Error as e:
                    print(f"Erro ao inserir pessoa: {e}")


def validar_login(login, senha):
    conn = sqlite3.connect('banco.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Pessoa WHERE login = ? AND senha = ?", (login, senha))
    pessoa = cursor.fetchone()

    if pessoa:
        print("Login bem-sucedido!")
        return True
    else:
        print("Login ou senha inválidos.")
        return False