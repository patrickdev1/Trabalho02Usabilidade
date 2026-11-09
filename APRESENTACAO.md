# Apresentação A3 — Bairro Sem Barreiras

Integrantes (grupo de 2 a 4): **preencher os nomes reais antes de entregar**.

## Pitch — aproximadamente 2 minutos e 30 segundos

**0:00–0:30 — Problema e público**

Nosso jogo aborda a acessibilidade urbana. Uma passagem com degrau pode impedir alguém de chegar a um serviço ou participar da comunidade. O público são estudantes e moradores que podem refletir sobre a organização dos espaços. O impacto pretendido é a conscientização; ainda não realizamos uma pesquisa para comprovar esse impacto.

**0:30–1:05 — Narrativa e objetivo**

Em Bairro Sem Barreiras, controlamos Alex, uma pessoa em cadeira de rodas que organiza um mutirão. A missão é entregar quatro cestas e abrir duas passagens. Alex atua como protagonista da transformação do bairro. Os moradores relatam como os acessos ajudam quem usa cadeira de rodas, bengala ou carrinho de bebê.

**1:05–1:45 — Por que a mecânica comunica a mensagem**

As barreiras realmente impedem a passagem. O jogador precisa instalar rampas para alcançar os moradores. Uma rampa continua aberta e outros personagens passam a utilizá-la. A mochila tem duas cestas e um kit, então precisamos planejar retornos à base. Não é só ler um texto sobre inclusão: é necessário modificar o espaço para vencer.

**1:45–2:10 — Implementação**

Usamos Python e PyGame, com um loop de entrada, atualização e desenho a 60 quadros por segundo. Há movimento proporcional ao tempo, colisões, estados de menu, partida, pausa e resultado. Mensagens, contadores, animações e som mostram o resultado de cada ação. O modo sem cronômetro permite explorar no próprio ritmo.

**2:10–2:30 — Transparência e conclusão**

Utilizamos IA para auxiliar a concepção, a implementação, a documentação e os testes. O registro descreve esse apoio e não atribui ao grupo validações que ainda não foram feitas. Nossa mensagem é que a acessibilidade depende de transformar o ambiente para que todos tenham autonomia.

## Demonstração — até 5 minutos

1. Apresente o menu e inicie o mutirão com Enter (20 segundos).
2. Vá à passagem A, mostre o bloqueio e instale a rampa com E (30 segundos).
3. Entregue as cestas à Lia e ao Seu Davi; observe os textos e o inventário (40 segundos).
4. Retorne à BASE e reabasteça com E (30 segundos).
5. Abra B, atenda Dona Rosa e Ravi e mostre o resultado (60 segundos).
6. Mostre o modo livre e explique a divisão `input → update → draw` em `Game.run` (40 segundos).

Os tempos são um roteiro estimado. Ensaiem antes da apresentação. Distribuam a fala conforme o número real de integrantes; cada integrante deve compreender e conseguir explicar o código. Não inventem contribuições individuais.
