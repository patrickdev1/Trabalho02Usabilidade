import math
import os
from array import array
from dataclasses import dataclass

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import pygame
from visuals import Visuals

WIDTH, HEIGHT = 1120, 760
TILE = 48
BG = '#354e40'
INK = '#edf5ee'
MUTED = '#a9bec6'


@dataclass
class Resident:
    name: str
    tile: tuple
    story: str
    done: bool = False


class World:
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
        self.buildings = [pygame.Rect(r.tile[0]*TILE-18, r.tile[1]*TILE-76, 84, 76)
                          for r in self.residents]
        self.buildings.append(pygame.Rect(72, 182, 96, 54))
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
        return (any(box.colliderect(pygame.Rect(x*TILE, y*TILE, TILE, TILE)) for x,y in obstacles)
                or any(box.colliderect(building) for building in self.buildings))

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
        pygame.display.set_caption('Bairro Sem Barreiras')
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.fonts = {}
        self.world = World()
        self.scene = 'menu'
        self.running = True
        self.muted = False
        self.buttons = []
        self.visuals = Visuals(self)
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
            pass

    def text(self, value, x, y, size=20, color=INK, bold=False):
        key = size, bold
        if key not in self.fonts:
            self.fonts[key] = pygame.font.SysFont('consolas', size, bold=bold)
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

    def start(self, practice=False):
        self.world = World(practice)
        self.scene = 'game'
        self.visuals.particles.clear()
        self.visuals.walk = 0

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
                        success = self.world.interact()
                        self.visuals.burst(success)
                        if success and self.sound and not self.muted:
                            self.sound.play()
                elif self.scene == 'pause':
                    if event.key in (pygame.K_p, pygame.K_ESCAPE, pygame.K_RETURN): self.scene = 'game'
                    elif event.key == pygame.K_q: self.scene = 'menu'
                elif self.scene == 'result':
                    if event.key == pygame.K_r: self.start(self.world.practice)
                    elif event.key == pygame.K_ESCAPE: self.scene = 'menu'

    def update(self, dt):
        previous = self.world.pos.copy()
        if self.scene == 'game':
            keys = pygame.key.get_pressed()
            self.world.update(dt, (int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT]),
                                   int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])))
            if self.world.status != 'playing': self.scene = 'result'
        if self.scene in ('game', 'menu'):
            self.visuals.tick(dt, self.world.pos - previous)

    def draw(self):
        self.buttons = []
        self.canvas.fill(BG)
        if self.scene == 'menu': self.visuals.menu()
        else:
            self.visuals.map()
            self.visuals.hud()
            if self.scene in ('pause','result'): self.visuals.overlay(self.scene == 'result')
        if self.muted: self.text('SOM DESLIGADO',890,734,13,MUTED)
        sw,sh = self.screen.get_size()
        scale = min(sw/WIDTH,sh/HEIGHT)
        size = max(1,int(WIDTH*scale)),max(1,int(HEIGHT*scale))
        self.screen.fill(BG)
        self.screen.blit(pygame.transform.scale(self.canvas,size),((sw-size[0])//2,(sh-size[1])//2))
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.input()
            self.update(dt)
            self.draw()
        pygame.quit()


if __name__ == '__main__':
    Game().run()
