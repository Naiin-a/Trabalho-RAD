import tkinter as tk
from tkinter import messagebox
from bd import BancoDeDados
from cadastro import Cadastro
from datetime import datetime
from validacao import validar_nome, validar_email, validar_senha, validar_login, validar_cpf, validar_3dig

bd = BancoDeDados()
bd.conectar()
bd.criar_tabelas()

cpf_adm_logado_global = None


def set_root(referencia_root):
    global root
    root = referencia_root

def mostrar_tela_login():
    root.title("Sistema de Login")
    root.configure(bg="gray")
    root.geometry("300x300")

    for widget in root.winfo_children():
        widget.destroy()

    global entry_login, entry_senha
    tk.Label(root, text="Login", bg="gray").pack()
    entry_login = tk.Entry(root)
    entry_login.pack()
    tk.Label(root, text="Senha", bg="gray").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()
    tk.Button(root, text="Entrar", command=fazer_login).pack(pady=10)
    tk.Button(root, text="Cadastrar", command=abrir_cadastro).pack()

def fazer_login():
    global cpf_adm_logado_global
    login = entry_login.get()
    senha = entry_senha.get()
    cpf_adm_logado_global = None

    if not bd.conn and not bd.conectar():
        messagebox.showerror("Erro", "Falha ao conectar ao banco de dados.")
        return

    resultado_login = bd.validar_login(login, senha)

    if resultado_login:
        tipo_usuario = resultado_login[0]
        if tipo_usuario == "adm":
            cpf_adm = resultado_login[1]
            nome_adm = resultado_login[2]
            cpf_adm_logado_global = cpf_adm
            messagebox.showinfo("Sucesso", f"Login de administrador bem-sucedido! Bem-vindo, {nome_adm}")
            from adm import mostrar_usuarios
            mostrar_usuarios(root, cpf_adm_logado_global)
        elif tipo_usuario == "pessoa":
            dados_pessoa_completo = resultado_login[1:]
            messagebox.showinfo("Sucesso", "Login de usuário bem-sucedido!")
            mostrar_dados_usuario(dados_pessoa_completo)
        else:
            messagebox.showerror("Erro", "Tipo de usuário desconhecido.")
    else:
        messagebox.showerror("Erro", "Login ou senha inválidos.")

def abrir_cadastro():
    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastro de Usuário")
    cadastro_window.geometry("350x450")
    cadastro_window.transient(root)
    cadastro_window.grab_set()

    def cadastrar_pessoa():
        try:
            cpf_str = entry_cpf.get()
            login = entry_login_cad.get()
            nome = entry_nome.get()
            senha = entry_senha_cad.get()
            bloco_str = entry_bloco.get()
            numero_ap_str = entry_numero_ap.get()
            email = entry_email.get()

            if not all([cpf_str, login, nome, senha, email,bloco_str,numero_ap_str]):
                messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos obrigatórios.",
                                       parent=cadastro_window)
                return
            if not validar_cpf(cpf_str):
                messagebox.showerror("Erro", "CPF inválido.", parent=cadastro_window)
                return
            if not validar_nome(nome):
                messagebox.showerror("Erro", "Nome inválido. Use apenas letras e espaços (8-20 caracteres).",
                                     parent=cadastro_window)
                return
            if not validar_login(login):
                messagebox.showerror("Erro", "Login inválido. Deve ter entre 8 e 20 caracteres alfanuméricos.",
                                     parent=cadastro_window)
                return
            if not validar_senha(senha):
                messagebox.showerror("Erro", "Senha deve ter entre 8 e 20 caracteres.", parent=cadastro_window)
                return
            if not validar_email(email):
                messagebox.showerror("Erro", "E-mail inválido.", parent=cadastro_window)
                return
            if not validar_3dig(bloco_str):
                messagebox.showerror("Erro", "Numero de bloco muito grande.", parent=cadastro_window)
            if not  validar_3dig(numero_ap_str):
                messagebox.showerror("Erro", "Numero de apartamento muito grande.", parent=cadastro_window)
            try:
                cpf = str(cpf_str)
                bloco = int(bloco_str) if bloco_str else None
                numero_ap = int(numero_ap_str) if numero_ap_str else None
            except ValueError:
                messagebox.showerror("Erro de Formato", "CPF, Bloco e AP devem ser números.", parent=cadastro_window)
                return

            pessoa = Cadastro(
                cpf=cpf, login=login, nome=nome, senha=senha,
                bloco=bloco, numero_ap=numero_ap, email=email,
                data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            bd.inserir_pessoa(pessoa, cpf_adm=None)
            messagebox.showinfo("Sucesso", "Cadastro realizado! Faça login.", parent=cadastro_window)
            cadastro_window.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}", parent=cadastro_window)

    tk.Label(cadastro_window, text="CPF*").pack(); entry_cpf = tk.Entry(cadastro_window); entry_cpf.pack()
    tk.Label(cadastro_window, text="Login*").pack(); entry_login_cad = tk.Entry(cadastro_window); entry_login_cad.pack()
    tk.Label(cadastro_window, text="Nome*").pack(); entry_nome = tk.Entry(cadastro_window); entry_nome.pack()
    tk.Label(cadastro_window, text="Senha*").pack(); entry_senha_cad = tk.Entry(cadastro_window, show="*"); entry_senha_cad.pack()
    tk.Label(cadastro_window, text="Bloco").pack(); entry_bloco = tk.Entry(cadastro_window); entry_bloco.pack()
    tk.Label(cadastro_window, text="Número do AP").pack(); entry_numero_ap = tk.Entry(cadastro_window); entry_numero_ap.pack()
    tk.Label(cadastro_window, text="Email*").pack(); entry_email = tk.Entry(cadastro_window); entry_email.pack()
    tk.Label(cadastro_window, text="* Campos obrigatórios").pack(pady=5)
    tk.Button(cadastro_window, text="Cadastrar", command=cadastrar_pessoa).pack(pady=10)

def mostrar_dados_usuario(dados):
    cpf, nome, bloco, numero_ap, email = dados
    for widget in root.winfo_children():
        widget.destroy()

    root.title(f"Área do Membro - {nome}")
    root.geometry("750x380")
    root.configure(bg="#f0f8ff")

    # --- Frame Esquerdo (Informações do Usuário) ---
    left_frame = tk.Frame(root, bg="#f0f8ff", padx=15, pady=10)
    left_frame.pack(side="left", fill="y", expand=False, padx=(10, 5), pady=10)  # fill="y" para ocupar altura

    tk.Label(left_frame, text="Informações do Usuário", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=10)
    info_display_frame = tk.Frame(left_frame, bg="#f0f8ff")
    info_display_frame.pack(pady=10, padx=5, fill="x", anchor="n")

    for info_text in [
        f"Nome: {nome}",
        f"CPF: {cpf}",
        f"Bloco: {bloco if bloco is not None else 'N/A'}",
        f"Apartamento: {numero_ap if numero_ap is not None else 'N/A'}",
        f"Email: {email}"
    ]:
        tk.Label(info_display_frame, text=info_text, anchor="w", justify="left", bg="#f0f8ff",
                 font=("Helvetica", 10)).pack(fill="x", pady=3)

    # Frame para botões de ação (todos juntos e empilhados)
    action_frame = tk.Frame(left_frame, bg="#f0f8ff")
    # pack normal, sem anchor ou expand, para ficar abaixo das infos
    action_frame.pack(pady=20, fill="x")

    # Botão Editar Dados
    tk.Button(action_frame, text="Editar Meus Dados", command=lambda u_cpf=cpf: editar_dados_usuario(u_cpf)).pack(
        pady=5, fill="x")

    # Botão Excluir Conta
    tk.Button(action_frame, text="Excluir Minha Conta", command=lambda u_cpf=cpf: excluir_conta(u_cpf), fg="red").pack(
        pady=5, fill="x")

    # Botão Logout (agora neste frame também)
    tk.Button(action_frame, text="Logout", command=reiniciar_para_login).pack(pady=5, fill="x")

    # --- Frame Direito (Carteirinha) ---
    right_frame = tk.Frame(root, bg="#f0f8ff", padx=10, pady=10)
    right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

    tk.Label(right_frame, text="Carteirinha do Clube", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=10)

    carteirinha_container = tk.Frame(right_frame, bg="#f0f8ff")
    carteirinha_container.pack(fill="both", expand=True)

    desenhar_carteirinha_no_frame(carteirinha_container, dados)

def desenhar_carteirinha_no_frame(parent_frame, dados_usuario):

    cpf, nome, bloco, numero_ap, email = dados_usuario  # Email não é usado no design atual

    # Limpa widgets anteriores DENTRO do frame da carteirinha
    for widget in parent_frame.winfo_children():
        widget.destroy()


    parent_frame.configure(bg="#f0f8ff")  # Fundo da área da carteirinha

    # Frame principal da carteirinha - simula o cartão físico
    card_width = 400
    card_height = 225
    card_frame = tk.Frame(parent_frame, bg="#f8f8f0", bd=2, relief="solid", width=card_width, height=card_height)
    # Centraliza o card_frame dentro do parent_frame
    card_frame.pack(pady=15, padx=10, expand=True)
    card_frame.pack_propagate(False)

    # ---
    photo_width = 100
    photo_height = 125
    photo_placeholder_frame = tk.Frame(card_frame, bg="#a0d2db", width=photo_width, height=photo_height)
    photo_placeholder_frame.place(x=20,
                                  y=(card_height - photo_height) // 2 + 10)
    photo_placeholder_frame.pack_propagate(False)
    tk.Label(photo_placeholder_frame, text="FOTO", font=("Helvetica", 9, "bold"), bg="#a0d2db", fg="#ffffff").pack(
        expand=True)


    info_container_x = photo_width + 30
    info_container_width = card_width - info_container_x - 15
    info_container = tk.Frame(card_frame, bg="#f8f8f0")
    info_container.place(x=info_container_x, y=10, width=info_container_width, height=card_height - 20)


    club_info_frame = tk.Frame(info_container, bg="#f8f8f0")
    club_info_frame.pack(anchor="ne", pady=3, padx=3)
    logo_canvas = tk.Canvas(club_info_frame, width=20, height=20, bg="#f8f8f0", highlightthickness=0)
    logo_canvas.create_oval(2, 2, 18, 18, fill="#006a71", outline="#006a71")
    logo_canvas.pack(side="left", padx=2)
    tk.Label(club_info_frame, text="Clube da Vizinhança", font=("Helvetica", 8, "bold"), bg="#f8f8f0", fg="#006a71").pack(
        side="left")


    member_info_frame = tk.Frame(info_container, bg="#f8f8f0")
    member_info_frame.pack(anchor="w", pady=(15, 5), padx=8)


    nome_label = tk.Label(member_info_frame, text=nome.upper() if nome else 'NOME INDISPONÍVEL',
                          font=("Helvetica", 12, "bold"), bg="#f8f8f0", fg="#006a71", anchor="w", justify="left",
                          wraplength=info_container_width - 20)  # Ajusta ao container
    nome_label.pack(fill='x')


    tk.Label(member_info_frame, text=f"CPF: {cpf if cpf else 'N/A'}",
             font=("Helvetica", 8), bg="#f8f8f0", fg="#333333", anchor="w", justify="left").pack(fill='x', pady=(6, 1))
    bloco_str = f"Bloco: {bloco}" if bloco else "Bloco: N/A"
    ap_str = f"Apto: {numero_ap}" if numero_ap else "Apto: N/A"
    tk.Label(member_info_frame, text=f"{bloco_str} / {ap_str}",
             font=("Helvetica", 8), bg="#f8f8f0", fg="#333333", anchor="w", justify="left").pack(fill='x', pady=1)


    bottom_border_height = 18
    bottom_border = tk.Frame(card_frame, bg="#006a71", height=bottom_border_height)
    bottom_border.place(x=0, y=card_height - bottom_border_height, relwidth=1.0)



def editar_dados_usuario(cpf):
    if not bd.conn and not bd.conectar():
        messagebox.showerror("Erro", "Sem conexão com banco.")
        return

    cursor = bd.conn.cursor()
    cursor.execute("SELECT nome, email, bloco, numero_ap, login FROM Pessoa WHERE cpf = ?", (str(cpf),))
    dados = cursor.fetchone()
    if not dados:
        messagebox.showerror("Erro", "Usuário não encontrado.")
        reiniciar_para_login()
        return

    nome_atual, email_atual, bloco_atual, numero_ap_atual, login_atual = dados

    editar_window = tk.Toplevel(root)
    editar_window.title("Editar Meus Dados")
    editar_window.geometry("350x450")
    editar_window.transient(root)
    editar_window.grab_set()

    tk.Label(editar_window, text="Nome*").pack()
    entry_nome_edit = tk.Entry(editar_window); entry_nome_edit.insert(0, nome_atual); entry_nome_edit.pack()
    tk.Label(editar_window, text="Email*").pack()
    entry_email_edit = tk.Entry(editar_window); entry_email_edit.insert(0, email_atual); entry_email_edit.pack()
    tk.Label(editar_window, text="Bloco").pack()
    entry_bloco_edit = tk.Entry(editar_window); entry_bloco_edit.insert(0, str(bloco_atual) if bloco_atual else ""); entry_bloco_edit.pack()
    tk.Label(editar_window, text="Número do AP").pack()
    entry_numero_ap_edit = tk.Entry(editar_window); entry_numero_ap_edit.insert(0, str(numero_ap_atual) if numero_ap_atual else ""); entry_numero_ap_edit.pack()
    tk.Label(editar_window, text="Nova Senha (deixe em branco para não alterar)").pack()
    entry_senha_edit = tk.Entry(editar_window, show="*"); entry_senha_edit.pack()
    tk.Label(editar_window, text="Confirmar Nova Senha").pack()
    entry_confirma_senha_edit = tk.Entry(editar_window, show="*"); entry_confirma_senha_edit.pack()
    tk.Label(editar_window, text="* Campos obrigatórios").pack(pady=5)

    def salvar_edicao():
        novo_nome = entry_nome_edit.get().strip()
        novo_email = entry_email_edit.get().strip()
        novo_bloco_str = entry_bloco_edit.get().strip()
        novo_numero_ap_str = entry_numero_ap_edit.get().strip()
        nova_senha = entry_senha_edit.get().strip()
        confirma_senha = entry_confirma_senha_edit.get().strip()

        if not validar_nome(novo_nome):
            messagebox.showerror("Erro", "Nome inválido. Use apenas letras e espaços (8-20 caracteres).",
                                 parent=editar_window)
            return
        if not validar_email(novo_email):
            messagebox.showerror("Erro", "E-mail inválido.", parent=editar_window)
            return
        if nova_senha and not validar_senha(nova_senha):
            messagebox.showerror("Erro", "Nova senha deve ter entre 8 e 20 caracteres.", parent=editar_window)
            return
        if nova_senha != "" and nova_senha != confirma_senha:
            messagebox.showerror("Erro", "As novas senhas não coincidem.", parent=editar_window)
            return
        if novo_bloco_str and not validar_3dig(novo_bloco_str):
            messagebox.showerror("Erro", "Bloco deve ser um número entre 1 e 999.", parent=editar_window)
            return
        if novo_numero_ap_str and not validar_3dig(novo_numero_ap_str):
            messagebox.showerror("Erro", "Número do AP deve ser um número entre 1 e 999.", parent=editar_window)
            return

        try:
            novo_bloco = int(novo_bloco_str) if novo_bloco_str else None
            novo_numero_ap = int(novo_numero_ap_str) if novo_numero_ap_str else None

            bd.atualizar_pessoa(
                cpf=str(cpf),
                cpf_adm=None,
                novo_nome=novo_nome,
                novo_email=novo_email,
                novo_bloco=novo_bloco,
                novo_numero_ap=novo_numero_ap,
                novo_senha=nova_senha if nova_senha else None
            )

            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!", parent=editar_window)
            editar_window.destroy()
            mostrar_dados_usuario((str(cpf), novo_nome, novo_bloco, novo_numero_ap, novo_email))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}", parent=editar_window)

    tk.Button(editar_window, text="Salvar Alterações", command=salvar_edicao).pack(pady=10)

def excluir_conta(cpf):
    if not messagebox.askyesno("Excluir Conta", "Tem certeza que deseja excluir sua conta?\nEsta ação é irreversível.", icon='warning'):
        return
    if not bd.conn and not bd.conectar():
        messagebox.showerror("Erro", "Sem conexão com banco.")
        return
    try:
        success = bd.deletar_pessoa(cpf=str(cpf), cpf_adm=None)
        if success:
            messagebox.showinfo("Sucesso", "Conta excluída com sucesso!")
            reiniciar_para_login()
        else:
            messagebox.showerror("Erro", "Não foi possível excluir a conta.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao excluir conta: {e}")

def reiniciar_para_login():
    global cpf_adm_logado_global
    cpf_adm_logado_global = None

    if root:
        for widget in root.winfo_children():
            widget.destroy()
        mostrar_tela_login()
    else:
        print("[ERRO] root está None! A janela principal deve ser criada pelo main() em interface.py")



def main():
    global root
    root = tk.Tk()
    mostrar_tela_login()
    root.mainloop()
    if bd.conn:
        bd.fechar_conexao()

if __name__ == "__main__":
    main()
