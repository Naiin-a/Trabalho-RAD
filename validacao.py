def input_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Entrada obrigatória. Tente novamente.")

def input_inteiro(mensagem):
    while True:
        try:
            valor = int(input(mensagem).strip())
            return valor
        except ValueError:
            print("Digite um número inteiro válido.")