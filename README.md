# Desafio 01 - MATA58

Projeto desenvolvido como parte da ementa da disciplina MATA58 - Sistemas Operacionais, sob orientação do professor Robespierre Dantas da Rocha Pita.

## Equipe

* Beatriz Cerqueira Brandão de Jesus;
* Lucas Morais Barreto;
* Lucas Sousa da Silva.

## Descrição

Um jogo de sorte para 2 ou mais jogadores, cujo objetivo é tentar adivinhar (ou chegar mais próximo de) um número sorteado aleatoriamente.

No jogo, há uma variável global que armazena o menor valor obtido até então pelo cálculo da diferença entre o valor sorteado e o palpite de cada jogador. Essa variável inicia com um valor logicamente nulo.

Cada jogador faz seu palpite. Em seguida, é criada uma **thread** para cada jogador. A execução de todas as threads é iniciada simultaneamente.

Cada thread é responsável por calcular a diferença entre o valor sorteado e seu respectivo palpite e, caso a diferença seja a menor até então, substitui o valor da variável global, indicando que o jogador correspondente àquela thread é o vencedor da rodada até o momento.

Para controlar o acesso a essa variável global que armazena a menor diferença, evitando problemas de paralelismo e concorrência entre as threads, é aplicado o conceito de **semáforo**.

A cada rodada, o jogador que obtiver a menor diferença entre o valor sorteado e seu respectivo palpite ganha um ponto, ou seja, ganha um ponto o jogador que ao final da rodada possuir a sua diferença armazenada na variável que armazena a menor diferença. Em caso de empate, nenhum jogador pontua.

Ganha o jogador que tiver mais pontos ao final do jogo.

## Vídeo
https://youtu.be/GjyP6RepfmA)

## Manual de uso

1. Execute o jogo. Será exibida a tela de seleção do número de jogadores.

2. Informe quantos jogadores vão jogar e clique em "Começar a Jogar". Uma nova tela será aberta para iniciar o jogo.

3. Cada jogador deverá digitar um palpite para tentar acertar ou chegar mais próximo do número que será sorteado pelo sistema. Os números variam entre 1 e 100.

4. Quando todos tiverem digitado seus palpites, clique em "Enviar Palpites".

5. O sistema irá revelar quem e qual palpite ganhou, além de mostrar o número escolhido e atualizar a pontuação.

6. Divirta-se!


## Instruções de instalação/compilação/execução

### Requerimentos

1. Git;
1. Python.

### Instruções


1. Clonar o repositório:

    ```
    git clone https://github.com/Lucazzx/Desafio1_SO.git
    ```

1. Instalar o `pip`:

    Instruções para instalação: https://pip.pypa.io/en/stable/installation/.


1. Instalar o `tkinter`:

    ```
    pip install tkinter
    ```

1. Executar o jogo:

    Você pode rodar o jogo diretamente através do código-fonte em Python ou através de um arquivo executável.

    #### Através do código-fonte

    ```
    python main.py
    ```

    Ou clique em "Run" na IDE de sua preferência.

    #### Através do arquivo executável

    Se você quiser gerar o executável, siga todos os passos abaixo. 

    Caso deseje apenas executar os arquivos executáveis já disponibilizados, pule para o passo 3.

    1. Instale o `PyInstaller`:

        ```
        pip install pyinstaller
        ```

    1. Gere o arquivo executável:

        ```
        pyinstaller --onefile main.py
        ```

        O arquivo executável será criado na pasta `dist`.

    1. Execute o arquivo gerado:

        ```
        dist/main
        ```
