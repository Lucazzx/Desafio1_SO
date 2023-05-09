import tkinter as tk
from threading import Thread, Semaphore, Lock
import random
import time

class Jogar:

    def __init__(self, janela):

        self.janela = janela
        self.janela.title("Jogo Advinhação")

        self.semaforo = Semaphore(1)
        self.threads_finalizadas = 0
        self.bloquear = Lock()

        self.texto_orientacao = tk.Label(janela,
                                         text="Olá, seja bem vindo.\n Aqui, três jogadores tentarão advinhar qual o número escolhido. \n Cuidado com seu palpite, quanto mais perto você chegar mais suas chances de ganhar aumentarão. ")
        self.texto_orientacao.grid(column=1, row=0)

        self.texto_jogador_a = tk.Label(janela, text="Jogador 1")
        self.texto_jogador_a.grid(column=0, row=1)

        self.texto_jogador_b = tk.Label(janela, text="Jogador 2")
        self.texto_jogador_b.grid(column=1, row=2)

        self.texto_jogador_c = tk.Label(janela, text="Jogador 3")
        self.texto_jogador_c.grid(column=2, row=1)

        self.entry_a = tk.Entry(self.janela)
        self.entry_a.grid(column=0, row=2)
        self.entry_b = tk.Entry(self.janela)
        self.entry_b.grid(column=1, row=3)
        self.entry_c = tk.Entry(self.janela)
        self.entry_c.grid(column=2, row=2)

        self.botao_enviar = tk.Button(self.janela, text="Enviar Palpites", command=self.enviar_palpites)
        self.botao_enviar.grid(column=1, row=5, padx=10, pady=25)

        self.botao_limpar = tk.Button(self.janela, text="Limpar Pontuações", command=self.limpar)
        self.botao_limpar.grid(row=5, column=2)

        self.texto_vencedor = tk.Label(self.janela, text="")
        self.texto_vencedor.grid(row=4, column=1)

        self.texto_pontuacao_geral = tk.Label(self.janela, text="Pontuação:\nJogador 1: 0\nJogador 2: 0\nJogador 3: 0")
        self.texto_pontuacao_geral.grid(row=5, column=0, rowspan=4)

        self.pontuacoes = [0, 0, 0]

    def enviar_palpites(self):
        self.finished_threads = 0
        self.numero_escolhido = random.randint(1, 100)

        texto_a = int(self.entry_a.get())
        texto_b = int(self.entry_b.get())
        texto_c = int(self.entry_c.get())

        thread1 = Thread(target=self.threads_jogadores, args=(1, texto_a))
        thread2 = Thread(target=self.threads_jogadores, args=(2, texto_b))
        thread3 = Thread(target=self.threads_jogadores, args=(3, texto_c))

        thread1.start()
        thread2.start()
        thread3.start()

    def threads_jogadores(self, id_jogador, palpite):

        time.sleep(random.random())

        with self.semaforo:
            diferenca = abs(self.numero_escolhido - palpite)


            if not hasattr(self, 'palpite_mais_perto'):
                self.palpite_mais_perto = (id_jogador, palpite, diferenca)
            elif diferenca < self.palpite_mais_perto[2]:
                self.palpite_mais_perto = (id_jogador, palpite, diferenca)


            with self.bloquear:
                self.finished_threads += 1

                if self.finished_threads == 3:
                    self.pontuacoes[self.palpite_mais_perto[0]-1] += 1
                    self.texto_pontuacao_geral.config(text=f"Pontuação:\nJogador 1: {self.pontuacoes[0]}\nJogador 2: {self.pontuacoes[1]}\nJogador 3: {self.pontuacoes[2]}")
                    self.texto_vencedor.config(text=f"Jogador {self.palpite_mais_perto[0]} ganhou com o palpite {self.palpite_mais_perto[1]} (Número Escolhido: {self.numero_escolhido})!")
                    del self.palpite_mais_perto
                    del diferenca

            self.entry_a.delete(0, tk.END)
            self.entry_b.delete(0, tk.END)
            self.entry_c.delete(0, tk.END)



    def limpar(self):

        self.entry_a.delete(0, tk.END)
        self.entry_b.delete(0, tk.END)
        self.entry_c.delete(0, tk.END)
        self.texto_vencedor.config(text="")
        self.pontuacoes = [0, 0, 0]
        self.texto_pontuacao_geral.config(
            text=f"Pontuação:\nJogador 1: {self.pontuacoes[0]}\nJogador 2: {self.pontuacoes[1]}\nJogador 3: {self.pontuacoes[2]}")


root = tk.Tk()
app = Jogar(root)
root.mainloop()

