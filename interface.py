from tkinter import *
import threading
import time
import random

# Declaração de variáveis
n = 0  # numero de jogadores
entries = []    # input da interface
jogadores = []  # variaveis dos jogadores (nome, palpite, pontuacao)
vencedor_da_rodada = {"nome": None,
                      "palpite": None,
                      'diff_palpite_num_sorteado': 9999999999}
semaforo = threading.Semaphore()

# Declaração de funções


def ler_palpites():
    for i in range(n):
        if entries[i] is not None:
            jogadores[i]["palpite"] = int(entries[i].get())


def reiniciar_palpites():
    for i in range(n):
        entries[i].delete(0, END)
        jogadores[i]["palpite"] = None


def enviar_palpites():  # Ação do botão

    print("Palpites enviados")

    ler_palpites()
    executar_rodada()
    reiniciar_palpites()

    print(jogadores)


def computar_pontuacao_rodada():

  # TODO: incrementar pontuacao do vencedor da rodada
  # TODO: printar pontuacao incrementada
    vencedor_da_rodada


def executar_rodada():

    global vencedor_da_rodada

    threads = []

    numero_sorteado = random.randint(1, 100)

    for jogador in jogadores:
        threads.append(threading.Thread(
            target=jogar, args=(jogador, numero_sorteado)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"\n\nO número sorteado foi {numero_sorteado}.")
    print(f"O(A) ganhador(a) da rodada foi: {vencedor_da_rodada['nome']}!")
    print(
        f"{vencedor_da_rodada['nome']} palpitou {vencedor_da_rodada['palpite']}.")
    print(
        f"A diferença entre o palpite e o número sorteado foi de {vencedor_da_rodada['diferenca']}.\n\n\n\n")

    computar_pontuacao_rodada()


def jogar(jogador, numero_sorteado):

    global vencedor_da_rodada
    global semaforo

    semaforo.acquire()

    diff_palpite_num_sorteado = abs(jogador['palpite'] - numero_sorteado)

    print(f"[{jogador['nome']} - {jogador['palpite']}] calculei a diferença = abs({jogador['palpite']} - {numero_sorteado}) = {diff_palpite_num_sorteado}")

    time.sleep(3)

    print(f"[{jogador['nome']} - {jogador['palpite']}] neste momento, há {len(semaforo._cond._waiters)} pessoas na fila")

    diff_atual_eh_menor = diff_palpite_num_sorteado < vencedor_da_rodada[
        'diff_palpite_num_sorteado']

    print(f"[{jogador['nome']} - {jogador['palpite']}] comparei com o menor ate agr = {diff_palpite_num_sorteado} < {vencedor_da_rodada['diff_palpite_num_sorteado']}? {diff_atual_eh_menor}")

    if diff_atual_eh_menor:

        vencedor_da_rodada = {"nome": jogador['nome'],
                              "palpite": jogador['palpite'],
                              'diff_palpite_num_sorteado': diff_palpite_num_sorteado}

        print(
            f"[{jogador['nome']} - {jogador['palpite']}] escrevi meu nome como vencedor")

    semaforo.release()


# Interface
def interface_game():

    janela = Tk()
    janela.title("Jogo Advinhação")

    texto_orientacao = Label(
        janela, text=f"Olá, seja bem-vindo(a)!\n Aqui, {n} jogadores tentarão advinhar qual o número escolhido. \n Cuidado com seu palpite, quanto mais perto você chegar mais suas chances de ganhar aumentarão. ")
    texto_orientacao.grid(column=1, row=0)

    col = 0
    row = 1

    for i in range(n):
        # interface de palpites e pontuações dos jogadores
        space = Label(janela, text="")
        texto_jogador = Label(janela, text="Jogador "+str(i))
        entries[i] = Entry(janela)
        texto_pontuacao = Label(
            janela, text="Pontuação: " + str(jogadores[i]["pontuacao"]))

        space.grid(column=col, row=row)
        texto_jogador.grid(column=col, row=row+1)
        entries[i].grid(column=col, row=row+2)
        texto_pontuacao.grid(column=col, row=row+3)

        col += 1
        if col > 2:
            col = 0
            row += 4

    row += 4  # posição do proximo elemento de interface (botão)

    submit = Button(janela, text="Enviar Palpites", command=enviar_palpites)
    submit.grid(column=1, row=row, padx=10, pady=25)

    texto_vencedor = Label(janela, text="")
    texto_vencedor.grid(column=1, row=row+1)

    janela.mainloop()


def start_game():
    global entries
    global jogadores
    global n

    n = int(entry_num_jogadores.get())
    print("Iniciando jogo.", n, "jogadores.")

    janela_intro.destroy()

    entries = [None]*n                    # input da interface

    for i in range(n):
        jogadores.append({"nome": "Jogador "+str(i),      # variaveis dos jogadores (nome, palpite, pontuacao)
                          "palpite": None,
                          "pontuacao": 0})

    interface_game()


janela_intro = Tk()
janela_intro.title("Jogo Advinhação")

texto_orientacao = Label(
    janela_intro, text="Olá, seja bem-vindo(a)!\n Para começar, informe a quantidade de jogadores.")
texto_orientacao.grid(column=1, row=0)

entry_num_jogadores = Entry(janela_intro)
entry_num_jogadores.grid(column=1, row=1)

start = Button(janela_intro, text="Começar a jogar", command=start_game)
start.grid(column=1, row=2, padx=10, pady=25)

janela_intro.mainloop()
