"""Bairro Sem Barreiras — jogo social em Python/PyGame, sem assets externos."""
import math
import os
import sys
from array import array
from dataclasses import dataclass

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import pygame

WIDTH, HEIGHT = 1120, 760
TILE, OX, OY = 48, 32, 174
BG = '#101f29'
INK = '#edf5ee'
MUTED = '#a9bec6'
GREEN = '#b8ef78'
TEAL = '#63d9c0'
GOLD = '#ffce78'


@dataclass
class Resident:
    name: str
    tile: tuple
    story: str
    done: bool = False


class World:
    """Regras independentes da janela, para permitir testes reproduzíveis."""
    def __init__(self, practice=False):
        self.practice = practice
        self.remaining = 180.0
        self.pos = pygame.Vector2(2.5 * TILE, 5.5 * TILE)
        self.station = (2, 5)
        self.gates = {(5, 3): False, (10, 7): False}
        self.walls = {(x, y) for x in (5, 10) for y in range(10)
                      if (x, y) not in self.gates}
        self.kits, self.food = 1, 2
        self.residents = [
            Resident('Lia', (7, 2), 'Lia: agora consigo ir à biblioteca com autonomia!'),
            Resident('Seu Davi', (7, 8), 'Davi: uma passagem acessível também ajuda quem usa bengala.'),
            Resident('Ravi', (13, 2), 'Ravi: posso levar o carrinho do meu bebê até a praça.'),
            Resident('Dona Rosa', (13, 7), 'Rosa: obrigada! O bairro precisa de acesso todos os dias.'),
        ]
        self.status = 'playing'
        self.message = 'Primeiro passo: aproxime-se da passagem A e pressione E.'
        self.message_time = 8
        self.elapsed = 0.0

    def near(self, tile):
        return self.pos.distance_to(pygame.Vector2(tile) * TILE + (24, 24)) < 65

    def blocked(self, pos):
        box = pygame.Rect(round(pos.x - 12), round(pos.y - 12), 24, 24)
        if box.left < 0 or box.top < 0 or box.right > 768 or box.bottom > 480:
            return True
        obstacles = self.walls | {p for p, opened in self.gates.items() if not opened}
        return any(box.colliderect(pygame.Rect(x * TILE, y * TILE, TILE, TILE))
                   for x, y in obstacles)

    def say(self, message):
        self.message, self.message_time = message, 7

    def target(self):
        if self.near(self.station):
            return ('station', self.station)
        for tile, opened in self.gates.items():
            if not opened and self.near(tile):
                return ('ramp', tile)
        for resident in self.residents:
            if not resident.done and self.near(resident.tile):
                return ('resident', resident)
        return None

    def interact(self):
        if self.status != 'playing':
            return False
        target = self.target()
        if not target:
            self.say('Chegue perto da base, de uma passagem ou de um morador marcado.')
            return False
        kind, obj = target
        if kind == 'station':
            self.kits, self.food = 1, 2
            self.say('Mochila abastecida: 2 cestas e 1 kit de rampa. Vamos juntos!')
        elif kind == 'ramp':
            if not self.kits:
                self.say('Sem kit de rampa. Volte à BASE e pressione E para reabastecer.')
                return False
            self.kits -= 1
            self.gates[obj] = True
            self.say('Passagem aberta para todos! A mudança permanece no bairro.')
        else:
            if not self.food:
                self.say('Sem cestas. Volte à BASE e pressione E para buscar mais duas.')
                return False
            self.food -= 1
            obj.done = True
            self.say(obj.story)
        if all(r.done for r in self.residents) and all(self.gates.values()):
            self.status = 'won'
        return True

    def update(self, dt, direction=(0, 0)):
        if self.status != 'playing':
            return
        dt = max(0, min(dt, .05))
        self.elapsed += dt
        self.message_time = max(0, self.message_time - dt)
        if not self.practice:
            self.remaining = max(0, self.remaining - dt)
            if self.remaining <= 0:
                self.status = 'lost'
                return
        velocity = pygame.Vector2(direction)
        if velocity.length_squared():
            velocity = velocity.normalize() * 190 * dt
        for axis in ('x', 'y'):
            candidate = self.pos.copy()
            setattr(candidate, axis, getattr(candidate, axis) + getattr(velocity, axis))
            if not self.blocked(candidate):
                self.pos = candidate


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Bairro Sem Barreiras | A3')
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.fonts = {}
        self.world = World()
        self.scene = 'menu'
        self.running = True
        self.muted = False
        self.buttons = []
        self.sound = None
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1)
            rate, _, channels = pygame.mixer.get_init()
            samples = array('h')
            for i in range(int(rate * .14)):
                value = int(4000 * math.sin(2 * math.pi * 660 * i / rate) * (1-i/(rate*.14)))
                samples.extend([value] * channels)
            self.sound = pygame.mixer.Sound(buffer=samples)
        except pygame.error:
            pass  # Todos os feedbacks também são visuais.

    def text(self, value, x, y, size=20, color=INK, bold=False):
        key = size, bold
        if key not in self.fonts:
            self.fonts[key] = pygame.font.SysFont('segoeui,arial', size, bold=bold)
        surface = self.fonts[key].render(str(value), True, color)
        self.canvas.blit(surface, (x, y))
        return surface.get_width()

    def wrap(self, value, x, y, width, size=20, color=MUTED):
        self.text('', 0, 0, size)
        font = self.fonts[(size, False)]
        line = ''
        for word in value.split():
            trial = (line + ' ' + word).strip()
            if font.size(trial)[0] > width and line:
                self.text(line, x, y, size, color)
                y += size + 8
                line = word
            else:
                line = trial
        self.text(line, x, y, size, color)
        return y + size + 8

    def rect(self, rect, color, radius=14, width=0):
        pygame.draw.rect(self.canvas, color, rect, width, border_radius=radius)

    def button(self, label, rect, action, primary=False):
        r = pygame.Rect(rect)
        self.rect(r, GREEN if primary else '#29424d', 12)
        self.text(label, r.x + 20, r.y + 13, 21, BG if primary else INK, True)
        self.buttons.append((r, action))

    def start(self, practice=False):
        self.world = World(practice)
        self.scene = 'game'

    def action(self, action):
        if action == 'start': self.start()
        elif action == 'practice': self.start(True)
        elif action == 'resume': self.scene = 'game'
        elif action == 'menu': self.scene = 'menu'
        elif action == 'retry': self.start(self.world.practice)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.WINDOWFOCUSLOST and self.scene == 'game':
                self.scene = 'pause'
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                sw, sh = self.screen.get_size()
                scale = min(sw / WIDTH, sh / HEIGHT)
                px = (event.pos[0] - (sw - WIDTH * scale) / 2) / scale
                py = (event.pos[1] - (sh - HEIGHT * scale) / 2) / scale
                for rect, action in self.buttons:
                    if rect.collidepoint(px, py):
                        self.action(action)
                        break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m: self.muted = not self.muted
                if self.scene == 'menu':
                    if event.key == pygame.K_RETURN: self.start()
                    elif event.key == pygame.K_t: self.start(True)
                elif self.scene == 'game':
                    if event.key in (pygame.K_p, pygame.K_ESCAPE): self.scene = 'pause'
                    elif event.key in (pygame.K_e, pygame.K_SPACE):
                        if self.world.interact() and self.sound and not self.muted:
                            self.sound.play()
                elif self.scene == 'pause':
                    if event.key in (pygame.K_p, pygame.K_ESCAPE, pygame.K_RETURN): self.scene = 'game'
                    elif event.key == pygame.K_q: self.scene = 'menu'
                elif self.scene == 'result':
                    if event.key == pygame.K_r: self.start(self.world.practice)
                    elif event.key == pygame.K_ESCAPE: self.scene = 'menu'

    def update(self, dt):
        if self.scene == 'game':
            keys = pygame.key.get_pressed()
            self.world.update(dt, (int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT]),
                                   int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])))
            if self.world.status != 'playing': self.scene = 'result'

    def wheelchair(self, x, y):
        pygame.draw.circle(self.canvas, BG, (x, y + 7), 13, 4)
        pygame.draw.circle(self.canvas, INK, (x, y - 14), 7)
        pygame.draw.lines(self.canvas, INK, False, [(x, y-5), (x, y+6), (x+12, y+6), (x+17, y+16)], 5)
        pygame.draw.circle(self.canvas, TEAL, (x-3, y+7), 7, 2)

    def map(self):
        w = self.world
        self.rect((OX-4, OY-4, 776, 488), '#3c5660', 12)
        for x in range(16):
            for y in range(10):
                r = pygame.Rect(OX+x*TILE, OY+y*TILE, TILE, TILE)
                pygame.draw.rect(self.canvas, '#dce5d7' if (x+y)%2 else '#d5dfd0', r)
                if (x,y) in w.walls:
                    pygame.draw.rect(self.canvas, '#547464', r)
                    pygame.draw.circle(self.canvas, '#6e9175', r.center, 17)
                    pygame.draw.circle(self.canvas, '#80a281', (r.centerx-4,r.centery-4), 9)
        for index, (tile, opened) in enumerate(w.gates.items()):
            x,y = OX+tile[0]*TILE, OY+tile[1]*TILE
            self.rect((x+2,y+2,44,44), TEAL if opened else GOLD, 5)
            for offset in (12,23,34):
                pygame.draw.line(self.canvas, '#315358' if opened else '#855e34', (x+7,y+offset), (x+40,y+offset if not opened else y+offset-5), 3)
            self.text(('A','B')[index], x+16,y-24,18,BG,True)
        sx, sy = OX+2*TILE, OY+5*TILE
        self.rect((sx-9,sy-7,66,62), '#214f60', 8)
        self.text('BASE',sx-2,sy+57,18,BG,True)
        pygame.draw.line(self.canvas, TEAL, (sx+18,sy+4),(sx+30,sy+4),3)
        pygame.draw.line(self.canvas, TEAL, (sx+24,sy-2),(sx+24,sy+10),3)
        for i,r in enumerate(w.residents):
            x,y = OX+r.tile[0]*TILE+24, OY+r.tile[1]*TILE+24
            self.rect((x-21,y-21,42,42), '#397e73' if r.done else '#b47954',8)
            pygame.draw.polygon(self.canvas, '#244a56', [(x-24,y-18),(x,y-34),(x+24,y-18)])
            self.text('OK' if r.done else str(i+1),x-10,y-12,19,INK,True)
            self.text(r.name,x-29,y+24,16,BG,True)
        # Vizinhos passam a usar as rotas abertas: consequência visível da intervenção.
        for index, (tile, opened) in enumerate(w.gates.items()):
            if opened:
                x = OX + tile[0]*TILE + 24 + math.sin(w.elapsed*.9+index)*67
                y = OY + tile[1]*TILE+24
                pygame.draw.circle(self.canvas, '#9760a0',(int(x),y-6),6)
                pygame.draw.line(self.canvas,'#9760a0',(int(x),y),(int(x),y+13),5)
        self.wheelchair(int(OX+w.pos.x),int(OY+w.pos.y))

    def hud(self):
        w = self.world
        self.text('BAIRRO SEM BARREIRAS',32,25,31,INK,True)
        self.text('O acesso muda quando o bairro muda.',34,69,19,MUTED)
        done = sum(r.done for r in w.residents)
        self.rect((826,25,262,73),'#203640')
        seconds = math.ceil(w.remaining)
        self.text('LIVRE' if w.practice else f'{seconds//60:02}:{seconds%60:02}',846,31,30,GREEN,True)
        self.text('sem cronômetro' if w.practice else 'tempo de mutirão',846,69,16,MUTED)
        self.text('01  PRAÇA / BASE',36,133,17,TEAL,True)
        self.text('02  VILA',330,133,17,TEAL,True)
        self.text('03  JARDIM',584,133,17,TEAL,True)
        self.rect((824,122,264,536),'#1b303b')
        self.text('SEU MUTIRÃO',844,143,18,TEAL,True)
        self.text(f'{done}/4',844,177,45,INK,True)
        self.text('moradores atendidos',844,231,18,MUTED)
        self.rect((844,266,222,7),'#37515a',3)
        if done: self.rect((844,266,222*done//4,7),GREEN,3)
        self.text(f'Cestas: {w.food}/2',844,294,21,INK,True)
        self.text(f'Kit de rampa: {w.kits}/1',844,330,21,INK,True)
        self.text(f'Passagens: {sum(w.gates.values())}/2',844,366,21,TEAL,True)
        self.wrap('Na BASE, E repõe sua mochila. Planeje as idas e voltas.',844,411,219,18)
        for i,r in enumerate(w.residents):
            self.text(f'{"OK" if r.done else str(i+1)+"."}  {r.name}',844,505+i*31,18,GREEN if r.done else MUTED)
        target = w.target()
        hint = 'WASD / setas: mover   •   E: interagir   •   P: pausa   •   M: som'
        if target:
            hint = {'station':'[E] Abastecer: 2 cestas + 1 kit de rampa', 'ramp':'[E] Instalar rampa e abrir passagem', 'resident':'[E] Entregar cesta e ouvir morador'}[target[0]]
        self.text(hint,34,670,19,GREEN)
        self.wrap(w.message if w.message_time else 'Meta: abrir as duas passagens e entregar cestas aos quatro moradores.',34,706,1045,18,INK)

    def menu(self):
        self.text('UM JOGO SOBRE AUTONOMIA E COMUNIDADE',58,48,18,TEAL,True)
        self.text('Bairro Sem',55,103,64,INK,True)
        self.text('Barreiras',55,174,72,GREEN,True)
        self.wrap('Você é Alex, uma pessoa em cadeira de rodas que organiza o mutirão do bairro. As cestas estão prontas. Mas nem todos os caminhos estão.',60,284,550,23,INK)
        self.wrap('Abra duas passagens com rampas e entregue cestas a quatro moradores. O problema está nas barreiras do espaço: transformar o bairro beneficia toda a comunidade.',60,405,550,21,MUTED)
        self.button('Iniciar mutirão  [Enter]',(60,550,348,57),'start',True)
        self.button('Explorar sem tempo  [T]',(60,624,348,57),'practice')
        self.rect((690,105,365,560),'#203640',26)
        self.wheelchair(865,174)
        self.text('COMO JOGAR',726,226,23,TEAL,True)
        for y, title, body in [(282,'01  Mova-se','WASD ou setas direcionais.'),(369,'02  Transforme','Perto da passagem, E instala a rampa.'),(471,'03  Conecte','E entrega cestas. Reabasteça na BASE.')]:
            self.text(title,720,y,23,INK,True)
            self.wrap(body,720,y+35,295,20)
        self.text('3 minutos  •  pausa com P',720,604,19,GOLD)
        self.text('Arte e áudio gerados por código  /  Python + PyGame',60,715,16,MUTED)

    def overlay(self, result=False):
        shade = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        shade.fill((5,15,24,215))
        self.canvas.blit(shade,(0,0))
        self.rect((230,145,660,470),'#203640',24)
        if not result:
            self.text('Uma pausa no caminho',268,189,36,INK,True)
            self.wrap('O tempo está parado. Volte quando quiser. As rampas e entregas continuam aqui.',270,260,565,23)
            self.button('Continuar  [P / Esc]',(270,400,570,58),'resume',True)
            self.button('Voltar ao início  [Q]',(270,480,570,58),'menu')
        else:
            won = self.world.status == 'won'
            self.text('O bairro é de todos.' if won else 'O mutirão continua.',268,185,39,GREEN if won else GOLD,True)
            done = sum(r.done for r in self.world.residents)
            self.text(f'{done}/4 entregas  •  {sum(self.world.gates.values())}/2 passagens abertas',270,248,23,INK,True)
            self.wrap('A acessibilidade não é um favor: é autonomia. As rotas que você abriu agora servem a todas as pessoas.' if won else 'O tempo acabou, mas as barreiras não são culpa de quem precisa passar. Tente planejar o reabastecimento ou explore sem cronômetro.',270,302,560,23)
            self.button('Jogar novamente  [R]',(270,444,570,57),'retry',True)
            self.button('Menu  [Esc]',(270,518,570,57),'menu')

    def draw(self):
        self.buttons = []
        self.canvas.fill(BG)
        if self.scene == 'menu': self.menu()
        else:
            self.map()
            self.hud()
            if self.scene in ('pause','result'): self.overlay(self.scene == 'result')
        if self.muted: self.text('SOM DESLIGADO',890,734,13,MUTED)
        sw,sh = self.screen.get_size()
        scale = min(sw/WIDTH,sh/HEIGHT)
        size = max(1,int(WIDTH*scale)),max(1,int(HEIGHT*scale))
        self.screen.fill(BG)
        self.screen.blit(pygame.transform.smoothscale(self.canvas,size),((sw-size[0])//2,(sh-size[1])//2))
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.input()   # 1. INPUT: eventos e comandos
            self.update(dt)  # 2. UPDATE: movimento, colisões, tempo e objetivos
            self.draw()    # 3. DRAW: cenário, personagem e feedback
        pygame.quit()


if __name__ == '__main__':
    Game().run()
