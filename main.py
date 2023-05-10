# Importando os módulos necessários
import random
import threading
import time

# Definindo o número aleatório a ser adivinhado
# numero = random.randint(1, 100)
numero = 100

# Definindo a variável que guarda o palpite da rodada
vencedor_parcial = (None, None, 9999999999999999)

# Definindo o semáforo que controla o acesso à variável
semaforo = threading.Semaphore()

# Definindo a função que cada thread executa
def jogar(nome, palpite):
    global vencedor_parcial # Usando a variável global

    # Tentando escrever na variável global
    semaforo.acquire() # Bloqueando o semáforo
    
    diferenca = abs(palpite - numero) # Calculando a diferença entre o palpite e o número
    
    print(f"[{nome} - {palpite}] calculei a diferença = abs({palpite} - {numero}) = {diferenca}")
    time.sleep(3)
    print(f"[{nome} - {palpite}] neste momento, há {len(semaforo._cond._waiters)} pessoas na fila")


    x = diferenca < vencedor_parcial[2]

    print(f"[{nome} - {palpite}] comparei com o menor ate agr = {diferenca} < {vencedor_parcial[2]}? {x}")
    
    if x: # Se a diferença da thread é menor que a da rodada

        vencedor_parcial = (nome, palpite, diferenca) # Substituindo os dados da rodada pelos da thread

        print(f"[{nome} - {palpite}] escrevi meu nome como vencedor")

    semaforo.release() # Liberando o semáforo

# Criando as threads com os nomes dos jogadores
jogador1 = threading.Thread(target=jogar, args=("Alice", 10)) # maior 100
jogador2 = threading.Thread(target=jogar, args=("Bruno", 30)) # menor 50
jogador3 = threading.Thread(target=jogar, args=("Carla", 20)) # médio 80


# Iniciando as threads
jogador1.start()
jogador2.start()
jogador3.start()


# Esperando as threads terminarem
jogador1.join()
jogador2.join()
jogador3.join()


print(f"O número sorteado foi {numero}.")
print(f"O(A) ganhador(a) foi: {vencedor_parcial[0]}!")
print(f"{vencedor_parcial[0]} palpitou {vencedor_parcial[1]}.")
print(f"A diferença foi de {vencedor_parcial[2]}.")


# Finalizando o programa
# Verificando se a thread acertou o número ou não
# if vencedor_parcial[0] == nome: # Se a thread foi a última a escrever na rodada
#     if vencedor_parcial[1] == numero: # Se a thread acertou o número
#         print(f"{nome} acertou! O número era {numero}. Parabéns!")
#         break # Saindo do loop
#     else: # Se a thread errou o número
#         print(f"{nome} errou por {vencedor_parcial[2]} unidades. Tente novamente.")
#         vencedor_parcial = None # Reiniciando a variável global para a próxima rodada
# else: # Se a thread não foi a última a escrever na rodada
#     print(f"{nome} não foi rápido o suficiente. Tente novamente.")
#     vencedor_parcial = None # Reiniciando a variável global para a próxima rodada
# print("Fim do jogo.")

