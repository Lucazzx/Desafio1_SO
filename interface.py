from tkinter import *
import threading
import time
import random

# Declaração de variáveis
n = 0  # numero de jogadores

entry = []    # input da interface
jogadores = [] # variaveis dos jogadores (nome, palpite, pontuacao)
vencedor = None     

# Declaração de funções
def ler_palpites():
    # preenche palpite dos jogadores
    for i in range(n):
        if entry[i] is not None:
            jogadores[i]["palpite"] = int(entry[i].get())

def enviar_palpites(): # Ação do botão

    print("Palpites enviados")

    ler_palpites()

    # Reinicia palpites
    for i in range(n):
        entry[i].delete(0, END)

    print(jogadores)


# Interface
def interface_game():

    janela = Tk()
    janela.title("Jogo Advinhação")
    
    texto_orientacao = Label(janela, text=f"Olá, seja bem-vindo(a)!\n Aqui, {n} jogadores tentarão advinhar qual o número escolhido. \n Cuidado com seu palpite, quanto mais perto você chegar mais suas chances de ganhar aumentarão. ")
    texto_orientacao.grid(column=1, row=0)

    col =  0
    row = 1 

    for i in range(n):
        # interface de palpites e pontuações dos jogadores
        space = Label(janela, text="")
        texto_jogador = Label(janela, text="Jogador "+str(i))
        entry[i] =Entry(janela)
        texto_pontuacao = Label(janela, text="Pontuação: " + str(jogadores[i]["pontuacao"]))

        space.grid(column=col, row=row)
        texto_jogador.grid(column=col, row=row+1)
        entry[i].grid(column=col, row=row+2)
        texto_pontuacao.grid(column=col, row=row+3)

        col += 1
        if col > 2:
            col = 0
            row += 4 

    row += 4 # posição do proximo elemento de interface (botão)

    submit = Button(janela, text="Enviar Palpites", command = enviar_palpites)
    submit.grid(column=1, row=row, padx=10, pady=25)

    texto_vencedor = Label(janela, text="")
    texto_vencedor.grid(column=1, row=row+1)

    janela.mainloop()

def start_game():
    global entry
    global jogadores
    global threads
    global n
    
    n = int(entry_num_jogadores.get())
    print("Iniciando jogo.", n, "jogadores.")
    
    janela_intro.destroy()
    
    entry = [None]*n                    # input da interface
    threads = [None]*n                  # variaveis de threads

    # TODO nome dos jogadores
    for i in range(n):
        jogadores.append({"nome":"Jogador "+str(i),      # variaveis dos jogadores (nome, palpite, pontuacao)
                            "palpite":None, 
                            "pontuacao":0}) 
    
    interface_game()


janela_intro = Tk()
janela_intro.title("Jogo Advinhação")

texto_orientacao = Label(janela_intro, text= "Olá, seja bem-vindo(a)!\n Para começar, informe a quantidade de jogadores.")
texto_orientacao.grid(column=1, row=0)

entry_num_jogadores = Entry(janela_intro)
entry_num_jogadores.grid(column=1, row=1)

start = Button(janela_intro, text="Começar a jogar", command = start_game)
start.grid(column=1, row=2, padx=10, pady=25)

janela_intro.mainloop()

