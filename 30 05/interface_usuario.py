import tkinter as tk
from tkinter import messagebox
from bd import BancoDeDados
from cadastro import Cadastro
from datetime import datetime



# Iniciar banco de dados
bd = BancoDeDados()
bd.conectar()
bd.criar_tabelas()

# Janela principal


def mostrar_dados_usuario(dados):
    nome, cpf, bloco, numero_ap, email = dados

    janela_dados = tk.Toplevel()
    janela_dados.title("Dados do Usuário")
    janela_dados.geometry("350x250")

    tk.Label(janela_dados, text=f"Nome: {nome}").pack(pady=5)
    tk.Label(janela_dados, text=f"CPF: {cpf}").pack(pady=5)
    tk.Label(janela_dados, text=f"Bloco: {bloco}").pack(pady=5)
    tk.Label(janela_dados, text=f"Apartamento: {numero_ap}").pack(pady=5)
    tk.Label(janela_dados, text=f"Email: {email}").pack(pady=5)


def abrir_cadastro():
    cadastro_window = tk.Toplevel()
    cadastro_window.title("Cadastro")
    cadastro_window.geometry("350x400")

    def cadastrar():
        try:
            pessoa = Cadastro(
                cpf=entry_cpf.get(),
                login=entry_login_cad.get(),
                nome=entry_nome.get(),
                senha=entry_senha_cad.get(),
                bloco=int(entry_bloco.get()),
                numeroAp=int(entry_ap.get()),
                email=entry_email.get(),
                data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ⬅ Aqui
            )
            bd.inserir_pessoa(pessoa)
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            cadastro_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")
    # Campos de cadastro
    tk.Label(cadastro_window, text="CPF").pack()
    entry_cpf = tk.Entry(cadastro_window)
    entry_cpf.pack()

    tk.Label(cadastro_window, text="Login").pack()
    entry_login_cad = tk.Entry(cadastro_window)
    entry_login_cad.pack()

    tk.Label(cadastro_window, text="Nome").pack()
    entry_nome = tk.Entry(cadastro_window)
    entry_nome.pack()

    tk.Label(cadastro_window, text="Senha").pack()
    entry_senha_cad = tk.Entry(cadastro_window, show="*")
    entry_senha_cad.pack()

    tk.Label(cadastro_window, text="Bloco").pack()
    entry_bloco = tk.Entry(cadastro_window)
    entry_bloco.pack()

    tk.Label(cadastro_window, text="Número do AP").pack()
    entry_ap = tk.Entry(cadastro_window)
    entry_ap.pack()

    tk.Label(cadastro_window, text="Email").pack()
    entry_email = tk.Entry(cadastro_window)
    entry_email.pack()

    tk.Button(cadastro_window, text="Cadastrar", command=cadastrar).pack(pady=10)

