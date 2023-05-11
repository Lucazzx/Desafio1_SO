# MATA 58 - Sistemas Operacionais - T2

Este é o repositório da equipe formada por Beatriz Cerqueira Brandão de Jesus, Lucas Morais Barreto e Lucas Sousa da Silva, responsável pelo desenvolvimento do jogo do T2 da disciplina MATA 58 - Sistemas Operacionais.

## Instruções de instalação/compilação/execução do jogo:

### Windows:
Para jogar no Windows, basta baixar o arquivo `jogo_win.exe` em qualquer pasta do sistema e executá-lo.

### Linux: 
Para jogar no Linux, basta baixar o arquivo `jogo_lnx.` em qualquer pasta do sistema e executá-lo.

### IDE:

Para jogar na IDE de sua preferência, após dar pull ou copiar o código, é necessário ter o Pip e o Tkinter instalados. Para isso, siga os passos abaixo:

1. Abra o terminal da IDE e digite os seguintes comandos:
2. Pip: `python -m ensurepip --default-pip`
3. Tkinter: `pip install tkinter`

Agora, ao clicar em "Run" na IDE, as interfaces carregarão e será possível jogar ali mesmo.

Se ainda assim você quiser gerar o executável após alguma mudança, siga os passos abaixo:

4. PyInstaller: `pip install pyinstaller`
5. Navegue até o diretório no qual o arquivo foi salvo. Use `cd nomedapasta` para ir e `cd ..` para voltar pastas.
6. Ao chegar na pasta desejada, digite o comando: `pyinstaller --onefile nomedoarquivo.py`
Assim, o arquivo executável será criado na pasta `dist`, no diretório em que o arquivo está.

## Manual de Uso:

Ao executar o jogo, será exibida a tela de seleção do número de jogadores. Informe quantos jogadores vão jogar e clique em "Começar a Jogar". Na próxima tela, cada jogador deverá tentar acertar ou chegar mais próximo do número escolhido pelo sistema. Em seguida, cada um deverá digitar um palpite e clicar em "Enviar Palpites". O sistema irá revelar quem e qual palpite ganhou, além de mostrar também o número escolhido e atualizar a pontuação.
