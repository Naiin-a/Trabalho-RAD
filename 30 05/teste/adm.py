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
def mostrar_usuarios(root):
    if bd.conn:
        try:
            cursor = bd.conn.cursor()
            cursor.execute("SELECT nome, cpf, bloco, numero_ap, email, data_cadastro FROM Pessoa")
            usuarios = cursor.fetchall()



            for widget in root.winfo_children():
                widget.destroy()

            janela_usuarios = root  # Agora usaremos a janela principal como "página"

            janela_usuarios.title("Usuários Cadastrados")
            janela_usuarios.geometry("600x500")

            tk.Label(janela_usuarios, text="Lista de Usuários", font=("Helvetica", 14, "bold")).pack(pady=10)

            for usuario in usuarios:
                nome, cpf, bloco, numero_ap, email, data_cadastro = usuario
                frame = tk.Frame(janela_usuarios)
                frame.pack(fill="x", padx=10, pady=2)

                info = f"{nome} | CPF: {cpf} | Bloco: {bloco} | Ap: {numero_ap} | Email: {email}"
                tk.Label(frame, text=info, anchor="w").pack(side="left")

                tk.Button(frame, text="Editar", command=lambda c=cpf: editar_usuario(root, c)).pack(side="right")
                tk.Button(frame, text="Excluir", command=lambda c=cpf: excluir_usuario(root, c)).pack(side="right")

            tk.Button(janela_usuarios, text="Cadastrar novo ADM", command=abrir_cadastro_adm).pack(pady=15)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar usuários: {e}")

def editar_usuario(root, cpf):
    if bd.conn:
        cursor = bd.conn.cursor()
        cursor.execute("SELECT nome, email, bloco, senha, numero_ap, login FROM Pessoa WHERE cpf = ?", (cpf,))
        usuario = cursor.fetchone()

        if not usuario:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

        nome_atual, email_atual, bloco_atual, senha_atual, numero_ap_atual, login_atual = usuario

        janela_editar = tk.Toplevel()
        janela_editar.title("Editar Usuário")
        janela_editar.geometry("300x200")

        tk.Label(janela_editar, text="Novo Nome").pack()
        entry_nome = tk.Entry(janela_editar)
        entry_nome.insert(0, nome_atual)
        entry_nome.pack()

        tk.Label(janela_editar, text="Novo Email").pack()
        entry_email = tk.Entry(janela_editar)
        entry_email.insert(0, email_atual)
        entry_email.pack()

        tk.Label(janela_editar, text="Novo bloco").pack()
        entry_bloco = tk.Entry(janela_editar)
        entry_bloco.insert(0, bloco_atual)
        entry_bloco.pack()

        tk.Label(janela_editar, text="Nova Senha").pack()
        entry_senha = tk.Entry(janela_editar)
        entry_senha.insert(0, senha_atual)
        entry_senha.pack()

        tk.Label(janela_editar, text="Novo apartamento").pack()
        entry_numero_ap = tk.Entry(janela_editar)
        entry_numero_ap.insert(0, numero_ap_atual)
        entry_numero_ap.pack()

        tk.Label(janela_editar, text="Novo Login").pack()
        entry_login = tk.Entry(janela_editar)
        entry_login.insert(0, login_atual)
        entry_login.pack()

        def salvar():
            resposta = messagebox.askyesno("Confirmar", "Tem certeza que deseja salvar as mudanças porra?")
            if resposta:
                novo_nome = entry_nome.get()
                novo_email = entry_email.get()
                novo_bloco = entry_bloco.get()
                novo_senha = entry_senha.get()
                novo_numero_ap = entry_numero_ap.get()
                novo_login = entry_login.get()
                bd.atualizar_pessoa(cpf, novo_nome=novo_nome, novo_email=novo_email, novo_bloco=novo_bloco, novo_senha=novo_senha,
                                    novo_numero_ap=novo_numero_ap, novo_login=novo_login)
                messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
                janela_editar.destroy()
                mostrar_usuarios(root)  # Atualiza a lista na janela principal

        tk.Button(janela_editar, text="Salvar", command=salvar).pack(pady=10)

def excluir_usuario(root, cpf):
    resposta = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este usuário?")
    if resposta:
        bd.deletar_pessoa(cpf)
        messagebox.showinfo("Removido", "Usuário excluído com sucesso!")
        mostrar_usuarios(root)  # Atualiza a lista na janela principal

def abrir_cadastro_adm():
    cadastro_window = tk.Toplevel()
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
