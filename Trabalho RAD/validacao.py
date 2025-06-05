# validacao.py (versão reescrita com validações para uso em interfaces GUI)
import re

def validar_nome(nome):
    nome = nome.strip()
    return nome.replace(" ", "").isalpha() and 8 <= len(nome) <= 20

def validar_texto(texto):
    texto = texto.strip()
    return 8 <= len(texto) <= 20

def validar_senha(senha):
    return 8 <= len(senha) <= 20

def validar_login(login):
    login = login.strip()
    return 8 <= len(login) <= 20 and login.replace("_", "").isalnum()

def validar_3dig(numero):
    try:
        numero = int(numero)
        return 1 <= numero <= 999
    except:
        return False

def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    return re.match(padrao, email) is not None

def validar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)  # Remove não dígitos
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if digito1 != int(cpf[9]):
        return False
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    return digito2 == int(cpf[10])