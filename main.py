from tkinter import *
import threading
import time
import random

# ============================ Declaração de variáveis ============================

# Variáveis gerais
n = 0                                             # número de jogadores
jogadores = []                                    # array de jogadores (nome, palpite, pontuacao)
palpite_maximo = 100                              # valor máximo a ser sorteado
numero_sorteado = None                            # valor sorteado a cada rodada


# Variáveis de interface
janela_intro = None                               # janela de introdução do jogo
entry_num_jogadores = None                        # input do número de jogadores
entries_palpites = []                             # inputs dos palpites usuários
texto_vencedor = None                             # texto exibido na interface com o vencedor da rodada
texto_pontuacoes = None                           # texto exibido na interface com as pontuções


# Variáveis threads e semáforo
threads = []                                      # array com as threads para cada jogador
semaforo = threading.Semaphore()                  # semáforo
vencedor_da_rodada = {"nome": None,               # variável global protegida pelo semáforo
                      "palpite": None,
                      'diff_palpite_num_sorteado': palpite_maximo + 1}


# ============================  Declaração de funções ============================

# -------------  Funções auxiliares de strings -------------

# Gera a string da pontuação.
def gerar_str_pontuacao():
    pontuacao_jogadores = "Pontuação:\n"

    for jogador in jogadores:
        pontuacao_jogadores += jogador["nome"] + \
            ":  " + str(jogador["pontuacao"]) + "\n"

    return pontuacao_jogadores


# Gera a string do vencedor da rodada.
def gerar_str_vencedor_rodada():

    global vencedor_da_rodada
    global numero_sorteado

    str = f"O número sorteado foi {numero_sorteado}.\n"

    # Declara empate
    if (vencedor_da_rodada["nome"] == None):
        str += "Houve um empate, ninguém pontua nessa rodada.\n"

    # Declara vencedor
    else:
        str += f"{vencedor_da_rodada['nome']} ganhou com o palpite {vencedor_da_rodada['palpite']}.\n"

    return str


# Gera a string da comparação entre a diferença do jogador e a menor diferença da rodada.
def gerar_str_comparacao(diff_palpite_num_sorteado):
    return f"Comparando minha diferença ({diff_palpite_num_sorteado}) com a menor diferença até agora ({vencedor_da_rodada['diff_palpite_num_sorteado']})..."


# Printa cálculo da diferença entre o palpite do jogador e o número sorteado.
def printar_calculo_diff(jogador, diff_palpite_num_sorteado):
    print(f"\n[{jogador['nome']}] Calculando a diferença entre meu palpite ({jogador['palpite']}) e o número sorteado ({numero_sorteado}) = {diff_palpite_num_sorteado}.")


# Printa tamanho da fila do semáforo.
def printar_tam_fila(jogador):
    print(
        f"[Semáforo - {jogador['nome']}] Há {len(semaforo._cond._waiters)} pessoas na fila.")


# Printa que o jogador ganhou.
def printar_ganhou(jogador, diff_palpite_num_sorteado):
    print(f"[{jogador['nome']}] {gerar_str_comparacao(diff_palpite_num_sorteado)} Minha diferença é menor.")
    print(f"[{jogador['nome']}] Escrevendo meu nome como vencedor.")


# Printa que houve empate.
def printar_empate(jogador, diff_palpite_num_sorteado):
    print(f"[{jogador['nome']}] {gerar_str_comparacao(diff_palpite_num_sorteado)} Minha diferença é igual.")
    print(f"[{jogador['nome']}] Removi o nome do vencedor.")


# Printa que o jogador perdeu.
def printar_perdeu(jogador, diff_palpite_num_sorteado):
    print(f"[{jogador['nome']}] {gerar_str_comparacao(diff_palpite_num_sorteado)} Minha diferença é maior.")
    print(f"[{jogador['nome']}] Não alterei o nome do vencedor.")


# Printa o resultado da rodada.
def printar_resultado_rodada():
    
    # Declara empate
    if (vencedor_da_rodada["nome"] == None):
        print("\n\nHouve um empate, ninguém pontua nessa rodada.\n\n")

    # Declara vencedor
    else:
        print(
            f"\n\n{vencedor_da_rodada['nome']} ganhou com o palpite {vencedor_da_rodada['palpite']}.")
        print(
            f"A diferença entre o palpite e o número sorteado foi de {vencedor_da_rodada['diff_palpite_num_sorteado']}.\n\n")
    
    print(f"Jogadores:\n{jogadores}\n")
    
    print("\n================= FIM DA RODADA =================\n\n")


# Printa o número sorteado.
def printar_numero_sorteado():
    print(f"O número sorteado foi {numero_sorteado}.\n")


# Printa a quantidade de jogadores.
def printar_quantidade_de_jogadores():
    print(f"Iniciando jogo com {n} jogadores.\n")


# Printa que os palpites foram enviados.
def printar_palpites_enviados():
    print("Palpites enviados.\n")


# -------------  Funções auxiliares para a interface -------------

# Atualiza interface com o resultado da rodada.
def atualizar_interface():

    global texto_vencedor
    global texto_pontuacoes

    texto_vencedor.config(text=gerar_str_vencedor_rodada())
    texto_pontuacoes.config(text=gerar_str_pontuacao())


# Limpa os palpites digitados na interface.
def limpar_palpites_interface():

    for i in range(n):
        entries_palpites[i].delete(0, END)
        jogadores[i]["palpite"] = None


# Lê os palpites digitados na interface.
def ler_palpites_interface():

    for i in range(n):
        if entries_palpites[i] is not None:
            jogadores[i]["palpite"] = int(entries_palpites[i].get())


# Interface do jogo em execução. Possui palpites e pontuações dos jogadores.
def interface_jogo():

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

        space = Label(janela, text="")
        texto_jogador = Label(janela, text=jogadores[i]["nome"])
        entries_palpites[i] = Entry(janela)

        space.grid(column=col, row=row)
        texto_jogador.grid(column=col, row=row+1)
        entries_palpites[i].grid(column=col, row=row+2)

        col += 1
        if col > 2:
            col = 0
            row += 4

    row += 4  # posição do proximo elemento de interface (botão)

    submit = Button(janela, text="Enviar Palpites", command=inicializar_rodada)
    submit.grid(column=1, row=row, padx=10, pady=25)

    texto_vencedor = Label(janela, text="")
    texto_vencedor.grid(column=1, row=row+1)

    texto_pontuacoes = Label(janela, text=gerar_str_pontuacao())
    texto_pontuacoes.grid(column=2, row=row+1)

    janela.mainloop()


# Ação do botão. Inicializa variáveis e interface do jogo.
def inicializar_jogo():

    global entries_palpites
    global jogadores
    global n

    n = int(entry_num_jogadores.get())

    printar_quantidade_de_jogadores()

    janela_intro.destroy()

    entries_palpites = [None]*n

    for i in range(n):
        jogadores.append({"nome": "Jogador "+str(i+1),
                          "palpite": None,
                          "pontuacao": 0})

    interface_jogo()


# Interface de introdução. Informa quantidade de jogadores.
def introducao_jogo():

    global janela_intro
    global entry_num_jogadores

    janela_intro = Tk()
    janela_intro.title("Jogo Advinhação")

    texto_orientacao = Label(
        janela_intro, text="Olá, seja bem-vindo(a)!\n Para começar, informe a quantidade de jogadores.")
    texto_orientacao.grid(column=1, row=0)

    entry_num_jogadores = Entry(janela_intro)
    entry_num_jogadores.grid(column=1, row=1)

    start = Button(janela_intro, text="Começar a jogar",
                   command=inicializar_jogo)
    start.grid(column=1, row=2, padx=10, pady=25)

    janela_intro.mainloop()


# -------------  Funções relacionadas às threads -------------

# Instancia as threads.
def instanciar_threads():

    global threads

    for jogador in jogadores:
        threads.append(threading.Thread(
            target=inicializar_jogada, args=(jogador, )))


# Inicializa a execução das threads.
def inicializar_threads():

    for thread in threads:
        thread.start()


# Finaliza a execução threads.
def finalizar_threads():

    for thread in threads:
        thread.join()


# -------------  Funções executadas a cada rodada  -------------

# Prepara a próxima rodada. Limpa as variáveis e a interface para a rodada seguinte.
def proxima_rodada():

    global vencedor_da_rodada
    global numero_sorteado
    global threads

    threads = []

    numero_sorteado = None

    vencedor_da_rodada = {"nome": None,
                          "palpite": None,
                          'diff_palpite_num_sorteado': palpite_maximo + 1}

    limpar_palpites_interface()


# Incrementa a pontuação do vencedor da rodada.
def incrementa_pontuacao_vencedor_rodada():

    global vencedor_da_rodada

    for jogador in jogadores:
        if jogador["nome"] == vencedor_da_rodada["nome"]:
            jogador["pontuacao"] += 1
            break


# Executa a rodada. Sorteia o número, gerencia as threads, coordena pontuações e exibe o resultado da rodada.
def executar_rodada():

    global numero_sorteado

    # Sorteia o número
    numero_sorteado = random.randint(1, palpite_maximo)
    printar_numero_sorteado()

    # Gerencia as threads
    instanciar_threads()
    inicializar_threads()
    finalizar_threads()

    # Atualiza pontuação do vencedor da rodada
    incrementa_pontuacao_vencedor_rodada()

    # Exibe os resultados na interface e no terminal
    atualizar_interface()
    printar_resultado_rodada()


# Ação do botão. Dispara o trigger para executar a rodada.
def inicializar_rodada():

    printar_palpites_enviados()
    ler_palpites_interface()

    executar_rodada()
    proxima_rodada()


# -------------  Funções executadas por cada jogador/thread  -------------

# Compara os palpites e escreve o vencedor.
def comparar_diff_e_escrever_vencedor(jogador, diff_palpite_num_sorteado):

    global vencedor_da_rodada

    if (diff_palpite_num_sorteado < vencedor_da_rodada['diff_palpite_num_sorteado']):
        printar_ganhou(jogador, diff_palpite_num_sorteado)
        vencedor_da_rodada = {"nome": jogador['nome'],
                              "palpite": jogador['palpite'],
                              'diff_palpite_num_sorteado': diff_palpite_num_sorteado}

    elif (diff_palpite_num_sorteado == vencedor_da_rodada['diff_palpite_num_sorteado']):
        printar_empate(jogador, diff_palpite_num_sorteado)
        vencedor_da_rodada = {"nome": None,
                              "palpite": None,
                              'diff_palpite_num_sorteado': diff_palpite_num_sorteado}

    else:
        printar_perdeu(jogador, diff_palpite_num_sorteado)

    printar_tam_fila(jogador)


# Executa a jogada de cada um dos jogadores. Compara os palpites e escreve o vencedor.
def executar_jogada(jogador):

    global numero_sorteado

    diff_palpite_num_sorteado = abs(jogador['palpite'] - numero_sorteado)
    printar_calculo_diff(jogador, diff_palpite_num_sorteado)

    time.sleep(3)
    comparar_diff_e_escrever_vencedor(jogador, diff_palpite_num_sorteado)


# Inicializa a jogada de cada um dos jogadores. Ativa e desativa o semáforo.
def inicializar_jogada(jogador):

    global semaforo

    semaforo.acquire()
    executar_jogada(jogador)
    semaforo.release()


# ============================ Run ============================

introducao_jogo()
