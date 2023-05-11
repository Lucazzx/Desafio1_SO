from tkinter import *
import threading
import time
import random

# Declaração de variáveis
n = 0  # numero de jogadores
jogadores = []  # variaveis dos jogadores (nome, palpite, pontuacao)
palpite_maximo = 100
numero_sorteado = None

# Variáveis de interface
entries = []    # inputs dos usuários
texto_vencedor = None
texto_pontuacoes = None

# Variáveis do semáforo
vencedor_da_rodada = {"nome": None,
                      "palpite": None,
                      'diff_palpite_num_sorteado': 101}
semaforo = threading.Semaphore()

# Declaração de funções


def ler_palpites():
    for i in range(n):
        if entries[i] is not None:
            jogadores[i]["palpite"] = int(entries[i].get())


def reiniciar_rodada():
    global vencedor_da_rodada
    vencedor_da_rodada = {"nome": None,
                      "palpite": None,
                      'diff_palpite_num_sorteado': 101}
    
    for i in range(n):
        entries[i].delete(0, END)
        jogadores[i]["palpite"] = None
    


def enviar_palpites():  # Ação do botão

    print("Palpites enviados")

    ler_palpites()
    executar_rodada()
    reiniciar_rodada()

    print(jogadores)


def computar_pontuacao_rodada():

    for jogador in jogadores:
        if jogador["nome"] == vencedor_da_rodada["nome"]:
            jogador["pontuacao"] += 1
            break


def escrever_pontuacao():
    pontuacao_jogadores = "Pontuação:\n"

    for jogador in jogadores:
        pontuacao_jogadores += jogador["nome"] + \
            ":  " + str(jogador["pontuacao"]) + "\n"

    return pontuacao_jogadores


def executar_rodada():

    global vencedor_da_rodada
    global numero_sorteado
    global texto_vencedor
    global texto_pontuacoes

    threads = []

    numero_sorteado = random.randint(1, 100)

    for jogador in jogadores:
        threads.append(threading.Thread(
            target=jogar, args=(jogador, 0)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    computar_pontuacao_rodada()

    if(vencedor_da_rodada["nome"] == None): # empate
        texto_vencedor.config(
            text=f"O número sorteado foi {numero_sorteado}.\nHouve um empate, ninguém pontua nessa rodada.\n")
    
    else:
        texto_vencedor.config(
            text=f"O número sorteado foi {numero_sorteado}.\n{vencedor_da_rodada['nome']} ganhou com o palpite {vencedor_da_rodada['palpite']}.\n")

    texto_pontuacoes.config(text=escrever_pontuacao())

    print(f"\n\nO número sorteado foi {numero_sorteado}.")
    print(f"O(A) ganhador(a) da rodada foi: {vencedor_da_rodada['nome']}!")
    print(
        f"{vencedor_da_rodada['nome']} palpitou {vencedor_da_rodada['palpite']}.")
    print(
        f"A diferença entre o palpite e o número sorteado foi de {vencedor_da_rodada['palpite']}.\n\n\n\n")


def jogar(jogador, n):  # TODO: tirar n

    global vencedor_da_rodada
    global numero_sorteado
    global semaforo

    semaforo.acquire()

    diff_palpite_num_sorteado = abs(jogador['palpite'] - numero_sorteado)

    print(f"[{jogador['nome']} - {jogador['palpite']}] calculei a diferença = abs({jogador['palpite']} - {numero_sorteado}) = {diff_palpite_num_sorteado}")

    time.sleep(1)

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

    elif(diff_palpite_num_sorteado == vencedor_da_rodada['diff_palpite_num_sorteado']):
        vencedor_da_rodada = {"nome": None,
                              "palpite": None,
                              'diff_palpite_num_sorteado': diff_palpite_num_sorteado}
        print("Empate!!")

    semaforo.release()


# Interface
def interface_game():
    global texto_vencedor
    global texto_pontuacoes

    janela = Tk()
    janela.title("Jogo de Advinhação")

    texto_orientacao = Label(
        janela, text=f"Olá, seja bem-vindo(a)!\n Aqui, {n} jogadores tentarão advinhar qual o número escolhido entre 0 e {palpite_maximo}. \n Cuidado com seu palpite, quanto mais perto você chegar mais suas chances de ganhar aumentarão. ")
    texto_orientacao.grid(column=1, row=0)

    col = 0
    row = 1

    for i in range(n):
        # interface de palpites e pontuações dos jogadores
        space = Label(janela, text="")
        texto_jogador = Label(janela, text=jogadores[i]["nome"])
        entries[i] = Entry(janela)

        space.grid(column=col, row=row)
        texto_jogador.grid(column=col, row=row+1)
        entries[i].grid(column=col, row=row+2)

        col += 1
        if col > 2:
            col = 0
            row += 4

    row += 4  # posição do proximo elemento de interface (botão)

    submit = Button(janela, text="Enviar Palpites", command=enviar_palpites)
    submit.grid(column=1, row=row, padx=10, pady=25)

    texto_vencedor = Label(janela, text="")
    texto_vencedor.grid(column=1, row=row+1)

    texto_pontuacoes = Label(janela, text=escrever_pontuacao())
    texto_pontuacoes.grid(column=2, row=row+1)

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
        jogadores.append({"nome": "Jogador "+str(i+1),      # variaveis dos jogadores (nome, palpite, pontuacao)
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
