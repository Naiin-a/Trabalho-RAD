import tkinter as tk
from tkinter import messagebox
from bd import BancoDeDados
from cadastro import Cadastro_adm
from datetime import datetime



# Iniciar banco de dados
bd = BancoDeDados()
bd.conectar()
bd.criar_tabelas()

# Janela principal


def mostrar_usuarios():
    if bd.conn:
        try:
            cursor = bd.conn.cursor()
            cursor.execute("SELECT nome, cpf, bloco, numeroAp, email, data_cadastro FROM Pessoa")
            usuarios = cursor.fetchall()

            if not usuarios:
                messagebox.showinfo("Informação", "Nenhum usuário cadastrado.")
                return

            janela_usuarios = tk.Toplevel()
            janela_usuarios.title("Usuários Cadastrados")
            janela_usuarios.geometry("600x500")

            tk.Label(janela_usuarios, text="Lista de Usuários", font=("Helvetica", 14, "bold")).pack(pady=10)

            for usuario in usuarios:
                nome, cpf, bloco, numeroAp, email, data_cadastro = usuario
                info = f"Nome: {nome} | CPF: {cpf} | Bloco: {bloco} | Ap: {numeroAp} | Email: {email} | Cadastrado em: {data_cadastro}"
                tk.Label(janela_usuarios, text=info, anchor="w", justify="left").pack(fill="x", padx=10, pady=2)

            def abrir_cadastro_adm():
                cadastro_window = tk.Toplevel(janela_usuarios)
                cadastro_window.title("Cadastro de ADM")
                cadastro_window.geometry("350x400")

                def cadastrar():
                    try:
                        pessoa = Cadastro_adm(
                            cpf=entry_cpf.get(),
                            login=entry_login_cad.get(),
                            nome=entry_nome.get(),
                            senha=entry_senha_cad.get(),
                            data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        )
                        bd.inserir_adm(pessoa)
                        messagebox.showinfo("Sucesso", "Administrador cadastrado com sucesso!")
                        cadastro_window.destroy()
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

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

                tk.Button(cadastro_window, text="Cadastrar", command=cadastrar).pack(pady=10)

            tk.Button(janela_usuarios, text="Cadastrar novo ADM", command=abrir_cadastro_adm).pack(pady=15)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuários: {e}")


