import tkinter as tk
from tkinter import messagebox
from bd import BancoDeDados
from cadastro import Cadastro
from datetime import  datetime
from interface_usuario import mostrar_dados_usuario
from adm import mostrar_usuarios



bd = BancoDeDados()
bd.conectar()
bd.criar_tabelas()

# Janela principal
root = tk.Tk()
root.title("Sistema de Login")
root.geometry("300x300")

def fazer_login():
    login = entry_login.get()
    senha = entry_senha.get()
    if bd.conn:
        cursor = bd.conn.cursor()

        # Verifica login como ADM
        cursor.execute("SELECT nome, cpf FROM Adm WHERE login = ? AND senha = ?", (login, senha))
        dados= cursor.fetchone()
        if dados:
            messagebox.showinfo("Sucesso", "Login de administrador bem-sucedido!")
            mostrar_usuarios()
            return

        # Verifica login como usuário normal
        cursor.execute("SELECT nome, cpf FROM Pessoa WHERE login = ? AND senha = ?", (login, senha))
        dados_pessoa = cursor.fetchone()
        if dados_pessoa:
            messagebox.showinfo("Sucesso", "Login de usuário bem-sucedido!")
            mostrar_dados_usuario()
            return

        messagebox.showerror("Erro", "Login ou senha inválidos.")

def abrir_cadastro():
    cadastro_window = tk.Toplevel(root)
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


tk.Label(root, text="Login").pack()
entry_login = tk.Entry(root)
entry_login.pack()

tk.Label(root, text="Senha").pack()
entry_senha = tk.Entry(root, show="*")
entry_senha.pack()

tk.Button(root, text="Entrar", command=fazer_login).pack(pady=10)
tk.Button(root, text="Cadastrar", command=abrir_cadastro).pack()

root.mainloop()
