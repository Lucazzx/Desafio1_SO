import random
import threading
import time

semaforo = threading.Semaphore(2)

#Inicializa variáveis do jogo
n = 3   # numero de jogadores
players = [None]*n
vencedor = None
max = 100
numero = random.randint(1, max) # Definindo o número aleatório a ser adivinhado

def jogar(nome):
    diferenca = None # Inicializando a diferença da thread
    global vencedor

    palpite = random.randint(0, max)
    print(f"{nome}, palpite:", palpite)

    diferenca = abs(palpite - numero)
    
    jogada = (nome, palpite, diferenca)

    if vencedor is None: # Se ninguém escreveu ainda   
        vencedor = jogada
        
    else: # Se alguém já escreveu
        if diferenca < vencedor[2]: # Se a diferença da thread é menor que a do vencedor
            vencedor = jogada # Substituindo os dados da rodada pelos da thread
    
    # semaforo.release() # Liberando o semáforo


print()

for i in range(n):
    players[i] = threading.Thread(target=jogar, args=("P"+str(i),)) 
    players[i].start()

#jogador1.join()
print("\nO número sorteado é",numero)
print("Vencedor:",vencedor[0])

print("\nFim do jogo.\n")
