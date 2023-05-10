import time
import threading

semaforo = threading.Semaphore()    
vencedor_da_rodada = {"nome": None,
                      "palpite": None,
                      'diff_palpite_num_sorteado': 9999999999}

def main():

  contador_de_rodadas = 0

  while contador_de_rodadas < 10:

    jogadores = minha_funcao_que_pega_os_palpites_da_interface()

    executar_rodada(jogadores)
    
    contador_de_rodadas += 1
    

def minha_funcao_que_pega_os_palpites_da_interface():
  # TODO: implementar
  return [{"nome": "Alice",
           "palpite": 10,
           "pontuacao": 0},
          {"nome": "Beatriz",
           "palpite": 30,
           "pontuacao": 0},
          {"nome": "Carla",
           "palpite": 20,
           "pontuacao": 0}]

def executar_rodada(jogadores):

  global vencedor_da_rodada

  threads = []
  
  # numero_sorteado = random.randint(1, 100)
  numero_sorteado = 100

  for jogador in jogadores:
    threads.append(threading.Thread(target=jogar, args=(jogador, numero_sorteado)))

  for thread in threads:
    thread.start()

  for thread in threads:
    thread.join()
  
  print(f"\n\nO número sorteado foi {numero_sorteado}.")
  print(f"O(A) ganhador(a) da rodada foi: {vencedor_da_rodada['nome']}!")
  print(f"{vencedor_da_rodada['nome']} palpitou {vencedor_da_rodada['palpite']}.")
  print(f"A diferença entre o palpite e o número sorteado foi de {vencedor_da_rodada['palpite']}.\n\n\n\n")
  
  # TODO: incrementar pontuacao do vencedor da rodada
  # TODO: printar pontuacao incrementada
  

def jogar(jogador, numero_sorteado):

    global vencedor_da_rodada
    global semaforo

    # semaforo.acquire()
    
    diff_palpite_num_sorteado = abs(jogador['palpite'] - numero_sorteado)

    print(f"[{jogador['nome']} - {jogador['palpite']}] calculei a diferença = abs({jogador['palpite']} - {numero_sorteado}) = {diff_palpite_num_sorteado}")
    
    time.sleep(3)
    
    print(f"[{jogador['nome']} - {jogador['palpite']}] neste momento, há {len(semaforo._cond._waiters)} pessoas na fila")

    diff_atual_eh_menor = diff_palpite_num_sorteado < vencedor_da_rodada['diff_palpite_num_sorteado']

    print(f"[{jogador['nome']} - {jogador['palpite']}] comparei com o menor ate agr = {diff_palpite_num_sorteado} < {vencedor_da_rodada['diff_palpite_num_sorteado']}? {diff_atual_eh_menor}")
    
    if diff_atual_eh_menor:

        vencedor_da_rodada = {"nome": jogador['nome'],
                              "palpite": jogador['palpite'],
                              'diff_palpite_num_sorteado': diff_palpite_num_sorteado}

        print(f"[{jogador['nome']} - {jogador['palpite']}] escrevi meu nome como vencedor")

    # semaforo.release()
    
main()