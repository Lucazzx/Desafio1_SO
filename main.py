# Importando os módulos necessários
import random
import threading
import time

# Definindo o número aleatório a ser adivinhado
numero = random.randint(1, 100)

# Definindo a variável que guarda o palpite da rodada
palpite_da_rodada = None

# Definindo o semáforo que controla o acesso à variável
semaforo = threading.Semaphore()

# Definindo a função que cada thread executa
def jogar(nome):
    global palpite_da_rodada # Usando a variável global
    palpite = None # Inicializando o palpite da thread
    diferenca = None # Inicializando a diferença da thread
    while True: # Repetindo até acertar ou desistir
        # Sorteando a ordem de leitura do teclado
        time.sleep(random.random())
        # Lendo o palpite da thread
        palpite = int(input(f"{nome}, digite um número entre 1 e 100: "))
        # Calculando a diferença entre o palpite e o número
        diferenca = abs(palpite - numero)
        # Tentando escrever na variável global
        semaforo.acquire() # Bloqueando o semáforo
        if palpite_da_rodada is None: # Se ninguém escreveu ainda
            palpite_da_rodada = (nome, palpite, diferenca) # Escrevendo os dados da thread
        else: # Se alguém já escreveu
            if diferenca < palpite_da_rodada[2]: # Se a diferença da thread é menor que a da rodada
                palpite_da_rodada = (nome, palpite, diferenca) # Substituindo os dados da rodada pelos da thread
        semaforo.release() # Liberando o semáforo
        # Esperando todas as threads escreverem na variável global
        time.sleep(1)
        # Verificando se a thread acertou o número ou não
        if palpite_da_rodada[0] == nome: # Se a thread foi a última a escrever na rodada
            if palpite_da_rodada[1] == numero: # Se a thread acertou o número
                print(f"{nome} acertou! O número era {numero}. Parabéns!")
                break # Saindo do loop
            else: # Se a thread errou o número
                print(f"{nome} errou por {palpite_da_rodada[2]} unidades. Tente novamente.")
                palpite_da_rodada = None # Reiniciando a variável global para a próxima rodada
        else: # Se a thread não foi a última a escrever na rodada
            print(f"{nome} não foi rápido o suficiente. Tente novamente.")
            palpite_da_rodada = None # Reiniciando a variável global para a próxima rodada

# Criando as quatro threads com os nomes dos jogadores
jogador1 = threading.Thread(target=jogar, args=("Alice",))
jogador2 = threading.Thread(target=jogar, args=("Bruno",))
jogador3 = threading.Thread(target=jogar, args=("Carla",))


# Iniciando as quatro threads
jogador1.start()
jogador2.start()
jogador3.start()


# Esperando as quatro threads terminarem
jogador1.join()
jogador2.join()
jogador3.join()


# Finalizando o programa
print("Fim do jogo.")
