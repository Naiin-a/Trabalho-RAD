import sqlite3
from bd import BancoDeDados
from cadastro import Cadastro
from login import Login
import validacao


conn = sqlite3.connect('banco.sqlite')  # ou o caminho completo se não estiver no mesmo diretório
cursor = conn.cursor()

bd = BancoDeDados()
bd.conectar()
bd.criar_tabelas()
while True:
    n = validacao.input_inteiro("Digite 1 para cadastrar ou 2 para logar")

    if (n == 1):
        pessoa = Cadastro(
            cpf = validacao.input_texto("Digite seu cpf: "),
            login = validacao.input_texto("Digite seu login: "),
            nome = validacao.input_texto("Digite seu nome: "),
            senha = validacao.input_texto("Digite sua senha, estaremos olhando: "),
            bloco = validacao.input_inteiro("Digite o numero do seu bloco: "),
            numeroAp = validacao.input_inteiro("Digite o numero do seu apartamento: "),
            email = validacao.input_texto("Digite seu email: "))
        bd.inserir_pessoa(pessoa)
        break
    elif (n == 2):
        pessoa = Login(
            login = validacao.input_texto("Digite seu login: "),
            senha = validacao.input_texto("Digite sua senha: ")
        )
        cursor.execute("SELECT * FROM Pessoa WHERE login = ? AND senha = ?", (pessoa.login, pessoa.senha))
        resultado = cursor.fetchone()
        if resultado:
            print("Login bem-sucedido!")
        else:
            print("Login ou senha inválidos.")
        break
    else:
        print("Opção invalida")
    # Caminho para o banco





# Ver tabelas existentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tabelas:", cursor.fetchall())

# Mostrar os dados da tabela Pessoa
cursor.execute("SELECT * FROM Pessoa;")
pessoas = cursor.fetchall()
for p in pessoas:
    print(p)

# Fechar conexão
conn.close()