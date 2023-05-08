from tkinter import *
import threading
import time
import random


# Declaração de variáveis
n = 3  # numero de jogadores
entry = [None]*n    # input da interface
palpites = [None]*n # variaveis dos palpites
threads = [None]*n  # variaveis de threads
vencedor = None     

sem = threading.Semaphore() # semaforo

# Declaração de funções
def ler_palpite(): # lê todos os palpites
    while(True):
        for i in range(n):
            if entry[i] is not None:
                sem.acquire()
                palpites[i] = (entry[i].get())
                sem.release()


def enviar_palpites(): # Ação do botão

    print("Palpites enviados")

    # Execução de threads
    for i in range(n):
        threads[i] = threading.Thread(target = ler_palpite)
        threads[i].start()
        time.sleep(1)

    print(palpites)

    # Reinicia palpites
    for i in range(n):
        entry[i].delete(0, END)


# Interface
janela = Tk()
janela.title("Jogo Advinhação")

texto_orientacao = Label(janela, text="Olá, seja bem vindo.\n Aqui, três jogadores tentarão advinhar qual o número escolhido. \n Cuidado com seu palpite, quanto mais perto você chegar mais suas chances de ganhar aumentarão. ")
texto_orientacao.grid(column=1, row=0)


for i in range(n):

    texto_jogador = Label(janela, text="Jogador "+str(i))
    entry[i] =Entry(janela)
    texto_pontuacao = Label(janela, text="Pontuação:")

    texto_jogador.grid(column=i, row=1)
    entry[i].grid(column=i, row=2)
    texto_pontuacao.grid(column=i, row=3)


submit = Button(janela, text="Enviar Palpites", command = enviar_palpites)
submit.grid(column=1, row=5, padx=10, pady=25)

# texto_vencedor = Label(janela, text="")
# texto_vencedor.grid(column=1, row=6)


janela.mainloop()