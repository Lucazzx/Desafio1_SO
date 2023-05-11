from tkinter import *
import threading
import time
import random

# -------------------------------- Declaração de variáveis --------------------------------

# Variáveis gerais
n = 0  # numero de jogadores
threads = []
jogadores = []  # variaveis dos jogadores (nome, palpite, pontuacao)
palpite_maximo = 100
numero_sorteado = None


# Variáveis de interface
entry_num_jogadores = None
janela_intro = None
entries = []    # inputs dos usuários
texto_vencedor = None
texto_pontuacoes = None


# Variáveis do semáforo
vencedor_da_rodada = {"nome": None,
                      "palpite": None,
                      'diff_palpite_num_sorteado': 101}
semaforo = threading.Semaphore()


# --------------------------------  Declaração de funções -------------------------------- 

# Ler palpites
def ler_palpites():

    for i in range(n):
        if entries[i] is not None:
            jogadores[i]["palpite"] = int(entries[i].get())


# Reiniciar rodada
def reiniciar_rodada():

    global vencedor_da_rodada
    global threads
    
    threads = []

    vencedor_da_rodada = {"nome": None,
                      "palpite": None,
                      'diff_palpite_num_sorteado': 101}
    
    for i in range(n):
        entries[i].delete(0, END)
        jogadores[i]["palpite"] = None


# Enviar palpites
def enviar_palpites(): 
    
    print("Palpites enviados.\n")

    ler_palpites()
    executar_rodada()
    reiniciar_rodada()

# Computar pontuação
def computar_pontuacao_rodada():

    global vencedor_da_rodada
    
    for jogador in jogadores:
        if jogador["nome"] == vencedor_da_rodada["nome"]:
            jogador["pontuacao"] += 1
            break


# Escrever pontuação
def gerar_str_pontuacao():

    pontuacao_jogadores = "Pontuação:\n"

    for jogador in jogadores:
        pontuacao_jogadores += jogador["nome"] + \
            ":  " + str(jogador["pontuacao"]) + "\n"

    return pontuacao_jogadores


# Gerar string do vencedor da rodada
def gerar_str_vencedor_rodada():
   
    global vencedor_da_rodada
    global numero_sorteado
    
    str = f"O número sorteado foi {numero_sorteado}.\n"

    # Declara empate
    if(vencedor_da_rodada["nome"] == None): 
        str += f"Houve um empate, ninguém pontua nessa rodada.\n"
    
    # Declara vencedor
    else:
        str += f"{vencedor_da_rodada['nome']} ganhou com o palpite {vencedor_da_rodada['palpite']}.\n"

    return str


# Instanciar threads
def instanciar_threads():
    
    global threads
    
    for jogador in jogadores:
        threads.append(threading.Thread(
            target=jogar, args=(jogador, 0)))


# Iniciar threads
def iniciar_threads():
    
    for thread in threads:
        thread.start()


# Finalizar threads
def finalizar_threads():
    
    for thread in threads:
        thread.join()


# Atualizar interface com o resultado da rodada
def atualizar_interface():
    
    global texto_vencedor
    global texto_pontuacoes
    
    texto_vencedor.config(text=gerar_str_vencedor_rodada())
    texto_pontuacoes.config(text=gerar_str_pontuacao())


# Printr logs do resultado da rodada
def printar_resultado_rodada():

    print(f"\n\nO(A) ganhador(a) da rodada foi: {vencedor_da_rodada['nome']}!")
    print(f"{vencedor_da_rodada['nome']} palpitou {vencedor_da_rodada['palpite']}.")
    print(f"A diferença entre o palpite e o número sorteado foi de {vencedor_da_rodada['diff_palpite_num_sorteado']}.\n\n")
    print(f"Jogadores:\n{jogadores}\n")


# Executar rodada. 
def executar_rodada():

    global numero_sorteado

    numero_sorteado = random.randint(1, palpite_maximo)

    print(f"O número sorteado foi {numero_sorteado}.\n")

    instanciar_threads()
    iniciar_threads()
    finalizar_threads()
    computar_pontuacao_rodada()
    atualizar_interface()
    printar_resultado_rodada()


def print_calculo_diff(jogador, diff_palpite_num_sorteado):
    print(f"\n[{jogador['nome']}] Calculei a diferença entre meu palpite ({jogador['palpite']}) e o número sorteado ({numero_sorteado}) = {diff_palpite_num_sorteado}.")


def print_tam_fila(jogador):
    print(f"[{jogador['nome']}] Há {len(semaforo._cond._waiters)} pessoas na fila.")


def gerar_str_comparacao(diff_palpite_num_sorteado):
    return f"Comparando minha diferença ({diff_palpite_num_sorteado}) com a menor diferença até agora ({vencedor_da_rodada['diff_palpite_num_sorteado']})..."


def print_ganhou(jogador, diff_palpite_num_sorteado):
    print(f"[{jogador['nome']}] {gerar_str_comparacao(diff_palpite_num_sorteado)} Minha diferença é menor.")
    print(f"[{jogador['nome']}] Escrevi meu nome como vencedor.")


def print_empate(jogador, diff_palpite_num_sorteado):
    print(f"[{jogador['nome']}] {gerar_str_comparacao(diff_palpite_num_sorteado)} Minha diferença é igual.")
    print(f"[{jogador['nome']}] Removi o nome do vencedor.")

    
def print_perdeu(jogador, diff_palpite_num_sorteado):
    print(f"[{jogador['nome']}] {gerar_str_comparacao(diff_palpite_num_sorteado)} Minha diferença é maior.")
    print(f"[{jogador['nome']}] Não alterei o nome do vencedor.")


def compara_diff_e_escreve_vencedor(jogador, diff_palpite_num_sorteado):

    global vencedor_da_rodada
    
    if (diff_palpite_num_sorteado < vencedor_da_rodada['diff_palpite_num_sorteado']):
        print_ganhou(jogador, diff_palpite_num_sorteado)
        vencedor_da_rodada = {"nome": jogador['nome'],
                              "palpite": jogador['palpite'],
                              'diff_palpite_num_sorteado': diff_palpite_num_sorteado}

    elif(diff_palpite_num_sorteado == vencedor_da_rodada['diff_palpite_num_sorteado']):
        print_empate(jogador, diff_palpite_num_sorteado)
        vencedor_da_rodada = {"nome": None,
                              "palpite": None,
                              'diff_palpite_num_sorteado': diff_palpite_num_sorteado}
    
    else:
        print_perdeu(jogador, diff_palpite_num_sorteado)



def foo(jogador):

    global numero_sorteado

    diff_palpite_num_sorteado = abs(jogador['palpite'] - numero_sorteado)
    
    print_calculo_diff(jogador, diff_palpite_num_sorteado)

    # time.sleep(1)

    compara_diff_e_escreve_vencedor(jogador, diff_palpite_num_sorteado)

    print_tam_fila(jogador)


def jogar(jogador, n):  # TODO: tirar n

    global semaforo

    semaforo.acquire()

    foo(jogador)

    semaforo.release()


# Inicia o jogo
def start_game():
    
    global entries
    global jogadores
    global n

    n = int(entry_num_jogadores.get())
    print(f"Iniciando jogo com {n} jogadores.\n")

    janela_intro.destroy()

    entries = [None]*n                    # input da interface

    for i in range(n):
        jogadores.append({"nome": "Jogador "+str(i+1),      # variaveis dos jogadores (nome, palpite, pontuacao)
                          "palpite": None,
                          "pontuacao": 0})

    inicializar_interface_game()

# -------------------------------- Interface --------------------------------

# Interface do jogo em execução
def inicializar_interface_game():
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

    texto_pontuacoes = Label(janela, text=gerar_str_pontuacao())
    texto_pontuacoes.grid(column=2, row=row+1)

    janela.mainloop()


# Interface de introdução. Informa quantidade de jogadores
def inicializar_intro_game():

    global janela_intro
    global entry_num_jogadores

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


inicializar_intro_game()