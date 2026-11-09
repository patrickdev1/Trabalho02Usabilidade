# Bairro Sem Barreiras

Jogo 2D em Python e **PyGame**, desenvolvido para a atividade A3 de Usabilidade, Desenvolvimento Web, Mobile e Jogos. Você é Alex, uma pessoa em cadeira de rodas que participa de um mutirão comunitário. Instale rampas, abra caminhos permanentes e entregue quatro cestas aos moradores.

## Executar no Windows

**Neste computador:** dê dois cliques em `JOGAR.bat`. O ambiente Python e o PyGame já foram preparados na pasta superior (`../.venv`). Mantenha essa pasta para usar o ambiente preparado.

**Em outro computador:** instale Python 3.12 (marque **Add Python to PATH**) e execute `JOGAR.bat`. Na primeira execução, o arquivo cria um ambiente `.venv` local e instala o PyGame; é necessária internet somente para instalar. Depois o jogo funciona offline. Nenhuma imagem, fonte externa ou conta é necessária.

Alternativa pelo PowerShell, dentro da pasta do jogo:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Para rodar usando o ambiente já preparado neste computador:

```powershell
..\.venv\Scripts\python.exe main.py
```

## Controles e regras

| Controle | Ação |
|---|---|
| Enter no menu | Mutirão com duração de 3 minutos |
| T no menu | Explorar sem limite de tempo |
| WASD / setas | Mover Alex |
| E / espaço | Interagir com o ponto mais próximo |
| P / Esc durante o jogo | Pausar / continuar |
| M | Desligar / ligar som |
| R no resultado | Reiniciar no mesmo modo |
| Esc no resultado | Voltar ao menu |

Os botões também funcionam com mouse. A janela pode ser redimensionada e preserva a proporção. Perder o foco pausa a partida. O feedback visual funciona mesmo sem dispositivo de áudio.

Você começa na BASE com **duas cestas e um kit de rampa**. A mochila comporta apenas essas quantidades. A BASE repõe os itens sem limite. Aproxime-se de uma passagem amarela (A ou B) e pressione E para instalar a rampa. As passagens verdes permanecem abertas. Árvores e passagens sem rampa bloqueiam o movimento. Aproxime-se das casas numeradas e pressione E para entregar uma cesta. Cada morador só recebe uma vez. Vença atendendo os quatro moradores e abrindo as duas passagens antes do tempo acabar. O modo livre tem os mesmos objetivos, sem derrota por tempo.

**Rota para a demonstração:** BASE → passagem A → Lia → Seu Davi → BASE (reabasteça com E) → passagem B → Dona Rosa → Ravi. A mensagem contextual indica quando E pode ser utilizado.

## Propósito e game design

- **Quem é impactado:** o público jogador, especialmente estudantes e pessoas que planejam ou usam espaços comunitários. Os personagens representam pessoas com necessidades diversas de mobilidade.
- **Problema:** barreiras urbanas que restringem circulação, autonomia e participação comunitária.
- **Contribuição das ações:** uma passagem inicialmente intransponível se torna utilizável após a intervenção. O acesso não depende apenas de uma mensagem: sem transformar o espaço, o jogador não consegue concluir as entregas.
- **Experiência desejada:** perceber a barreira, planejar recursos e experimentar a satisfação de tornar o bairro acessível. Não se pretende simular toda a experiência de uma pessoa com deficiência.
- **Reforço mecânico:** colisões materializam a exclusão; rampas alteram permanentemente o mapa; vizinhos usam as novas passagens; capacidade da mochila exige planejamento; diálogos relacionam a intervenção à autonomia.
- **Impacto pretendido, não medido:** sensibilização sobre acessibilidade. Não foram realizadas avaliações com usuários ou medições de impacto real. Os kits são uma abstração lúdica, não instruções de obra ou substituto de políticas públicas.

## Requisitos e implementação

| Requisito da atividade | Implementação |
|---|---|
| Python e PyGame obrigatórios | `main.py`, `requirements.txt` |
| Problema social e narrativa | Acessibilidade urbana; Alex e quatro moradores |
| Mecânica relevante | Movimento com colisão, rampas permanentes, coleta e entrega |
| Game loop input → update → draw | `Game.run`, limite de 60 FPS e movimento por delta time |
| Feedback perceptível | Mensagens, cores e números, contadores, som e vizinhos animados |
| Apresentação até 3 minutos | `APRESENTACAO.md` |
| Interatividade até 5 minutos | Partida de 3 minutos; rota de demonstração documentada |
| Uso honesto de IA | `USO_DE_IA.md` |
| Código no GitHub com acesso liberado | Repositório Git local preparado; publicação depende da conta do grupo |

## Arquitetura e testes

`World` contém estado e regras; `Resident` representa moradores; `Game` trata eventos, renderização e áudio. A atualização para ao pausar ou encerrar. O delta time é limitado a 50 ms para impedir saltos em travamentos; nessa situação o cronômetro mede tempo simulado. Colisão é resolvida por eixo; diagonais têm velocidade normalizada. Arte e áudio são gerados por código.

```powershell
..\.venv\Scripts\python.exe -m unittest -v
```

Se instalou o ambiente dentro desta pasta, use `.\.venv\Scripts\python.exe` no comando. Os testes usam os drivers SDL de teste, sem abrir janela. Cobrem uma partida inteira com movimento real por caminhos válidos, bloqueios, limites, falta de recursos, derrota por tempo, modo livre, entregas repetidas, velocidade diagonal, renderização das telas, pausa e reinício.

Checklist manual: iniciar com Enter; tentar atravessar A sem rampa; instalar com E; observar passagem e vizinho; entregar duas cestas; reabastecer; abrir B; finalizar; reiniciar; testar pausa, modo livre, som e redimensionamento.

## Publicar no GitHub

A publicação externa não foi feita: é preciso escolher a conta e o repositório de destino. Não envie `.venv` ou credenciais. Crie no GitHub um repositório **público**, vazio, chamado `bairro-sem-barreiras`. Dentro desta pasta execute, substituindo `SEU-USUARIO`:

```powershell
git remote add origin https://github.com/SEU-USUARIO/bairro-sem-barreiras.git
git push -u origin main
```

Autentique-se na sua conta quando solicitado. Verifique o link em janela anônima para confirmar que o professor consegue abrir o código. Se alterar arquivos antes de publicar, faça `git add .` e `git commit -m "Atualiza entrega A3"`. Preencha os integrantes em `APRESENTACAO.md`.

## Referência técnica

Documentação oficial consultada: https://www.pygame.org/docs/ (eventos, desenho, teclado e relógio). Biblioteca: PyGame 2.6.1. Não há assets de terceiros incorporados.
