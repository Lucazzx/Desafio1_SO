import requests
from tkinter import *

#funções testes
def f_teste():

    numero_aleatorio = 10
    numero_max = 100

    texto_teste_a = int(entry_a.get())
    texto_teste_b = int(entry_b.get())
    texto_teste_c = int(entry_c.get())

    texto_pontuacao_a["text"] = f''' Pontuação: {texto_teste_a} '''
    texto_pontuacao_b["text"] = f''' Pontuação: {texto_teste_b} '''
    texto_pontuacao_c["text"] = f''' Pontuação: {texto_teste_c} '''

    entry_a.delete(0, END)
    entry_b.delete(0, END)
    entry_c.delete(0, END)

    #texto_vencedor["text"] = " "
    if texto_teste_a == numero_aleatorio or texto_teste_a >= numero_max:
        texto_vencedor["text"] = "Jogador 1 ganhou!"
    elif texto_teste_b == numero_aleatorio or texto_teste_b >= numero_max:
        texto_vencedor["text"] = "Jogador 2 ganhou!"
    elif texto_teste_c == numero_aleatorio or texto_teste_c >= numero_max:
        texto_vencedor["text"] = "Jogador 3 ganhou!"
    else:
        texto_vencedor["text"] = "Nenhum jogador ganhou."


#interface
janela = Tk()
janela.title("Jogo Advinhação")


texto_orientacao = Label(janela, text="Olá, seja bem vindo.\n Aqui, três jogadores tentarão advinhar qual o número escolhido. \n Cuidado com seu palpite, quanto mais perto você chegar mais suas chances de ganhar aumentarão. ")
texto_orientacao.grid(column=1, row=0)

texto_jogador_a = Label(janela, text="Jogador 1")
texto_jogador_a.grid(column=0, row=1)
texto_pontuacao_a = Label(janela, text="")
texto_pontuacao_a.grid(column=0, row=3)

texto_jogador_b = Label(janela, text="Jogador 2")
texto_jogador_b.grid(column=2, row=1)
texto_pontuacao_b = Label(janela, text="")
texto_pontuacao_b.grid(column=2, row=3)

texto_jogador_c = Label(janela, text="Jogador 3")
texto_jogador_c.grid(column=1, row=2)
texto_pontuacao_c = Label(janela, text="")
texto_pontuacao_c.grid(column=1, row=4)

entry_a =Entry(janela)
entry_a.grid(column=0, row=2)
entry_b =Entry(janela)
entry_b.grid(column=2, row=2)
entry_c =Entry(janela)
entry_c.grid(column=1, row=3)

butao_a = Button(janela, text="Enviar Palpites", command = f_teste)
butao_a.grid(column=1, row=5, padx=10, pady=25)

texto_vencedor = Label(janela, text="")
texto_vencedor.grid(column=1, row=6)


janela.mainloop()