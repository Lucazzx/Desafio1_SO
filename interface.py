from tkinter import *
import threading
import time
import random

# Declaração de variáveis
intro_game = True
n = 3  # numero de jogadores

entry = []    # input da interface
palpites = [] # variaveis dos palpites
threads = []  # variaveis de threads
vencedor = None     

sem = threading.Semaphore() # semaforo

# Declaração de funções
def ler_palpite(): # lê todos os palpites
    while(True):
        for i in range(n):
            if entry[i] is not None:
                # sem.acquire()
                palpites[i] = (entry[i].get())
                # sem.release()
    
def enviar_palpites(): # Ação do botão

    print("Palpites enviados")

    # Execução de threads
    for i in range(n):
        threads[i] = threading.Thread(target = ler_palpite)
        threads[i].start()

    # Reinicia palpites
    for i in range(n):
        entry[i].delete(0, END)

    print(palpites)


# Interface
def interface_game():

    janela = Tk()
    janela.title("Jogo Advinhação")
    
    texto_orientacao = Label(janela, text=f"Olá, seja bem vindo.\n Aqui, {n} jogadores tentarão advinhar qual o número escolhido. \n Cuidado com seu palpite, quanto mais perto você chegar mais suas chances de ganhar aumentarão. ")
    texto_orientacao.grid(column=1, row=0)

    col =  0
    row = 1 

    for i in range(n):

        texto_jogador = Label(janela, text="Jogador "+str(i))
        entry[i] =Entry(janela)
        texto_pontuacao = Label(janela, text="Pontuação:")

        texto_jogador.grid(column=col, row=row)
        entry[i].grid(column=col, row=row+1)
        texto_pontuacao.grid(column=col, row=row+2)

        col += 1
        if col > 2:
            col = 0
            row += 4 

    row += 3 # posição do proximo elemento de interface (botão)

    submit = Button(janela, text="Enviar Palpites", command = enviar_palpites)
    submit.grid(column=1, row=row, padx=10, pady=25)

    # texto_vencedor = Label(janela, text="")
    # texto_vencedor.grid(column=1, row=6)

    janela.mainloop()

def start_game():
    global entry
    global palpites
    global threads
    global n
    
    n = int(entry_num_jogadores.get())
    print("Iniciando jogo", n, "jogadores")
    
    janela_intro.destroy()
    
    entry = [None]*n     # input da interface
    palpites = [None]*n  # variaveis dos palpites
    threads = [None]*n   # variaveis de threads

    interface_game()


janela_intro = Tk()
janela_intro.title("Jogo Advinhação")

texto_orientacao = Label(janela_intro, text= "Olá, seja bem vindo.\n Para começar, informe a quantidade de jogadores.")
texto_orientacao.grid(column=1, row=0)

entry_num_jogadores = Entry(janela_intro)
entry_num_jogadores.grid(column=1, row=1)

start = Button(janela_intro, text="Começar a jogar", command = start_game)
start.grid(column=1, row=2, padx=10, pady=25)

janela_intro.mainloop()

