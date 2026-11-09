import math
import random

import pygame


PAPER = '#f7e9bd'
INK = '#423d36'
MOSS = '#4c6944'
CREAM = '#fff5d5'
WOOD = '#85563e'


class Visuals:
    def __init__(self, game):
        self.g = game
        self.time = 0
        self.particles = []
        self.walk = 0
        self.facing = 1
        self.moving = False
        self.trees = [(18,46,1),(99,38,2),(26,218,3),(92,231,4),(159,35,5),
                      (221,35,6),(287,40,7),(370,35,8),(283,224,9),(376,224,10),(159,152,11)]
        self.ground = self.make_ground()

    def box(self, s, color, rect):
        pygame.draw.rect(s, color, tuple(int(v) for v in rect))

    def panel(self, rect, paper=True):
        x, y, w, h = rect
        s = self.g.canvas
        self.box(s, '#332f2b', (x+5,y+6,w,h))
        self.box(s, '#543e32', rect)
        self.box(s, '#b78b57', (x+3,y+3,w-6,h-6))
        self.box(s, PAPER if paper else '#6f4936', (x+7,y+7,w-14,h-14))
        for px in (x+12,x+w-15):
            for py in (y+12,y+h-15):
                self.box(s, '#d6af71', (px,py,3,3))

    def label(self, text, x, y, size=18, color=INK, bold=False):
        return self.g.text(text,x,y,size,color,bold)

    def wrap(self, text, x, y, width, size=18, color=INK):
        return self.g.wrap(text,x,y,width,size,color)

    def shadow(self,s,x,y,w=18,h=6):
        pygame.draw.ellipse(s,'#687c4c',(int(x-w/2),int(y-h/2),w,h))

    def tree(self,s,x,y,seed=0):
        r = random.Random(seed)
        self.shadow(s,x+4,y+1,31,10)
        self.box(s,'#654d38',(x-3,y-17,6,20))
        self.box(s,'#a17848',(x,y-16,2,16))
        pygame.draw.polygon(s,'#365c43',[(x-18,y-18),(x-18,y-33),(x-12,y-33),(x-12,y-42),(x+6,y-45),(x+14,y-37),(x+19,y-37),(x+20,y-21),(x+12,y-12),(x-8,y-12)])
        pygame.draw.polygon(s,'#4b8151',[(x-17,y-29),(x-12,y-40),(x+4,y-44),(x+14,y-35),(x+13,y-24),(x+3,y-16),(x-10,y-21)])
        pygame.draw.polygon(s,'#78a45a',[(x-13,y-33),(x-8,y-40),(x+3,y-41),(x+8,y-35),(x+1,y-29),(x-7,y-27)])
        for _ in range(9):
            px,py=x+r.randrange(-12,13),y+r.randrange(-36,-17)
            self.box(s,r.choice(['#679653','#90b263','#376b48']),(px,py,3,2))
        if seed%3==0:
            for dx,dy in [(-8,-29),(8,-23),(2,-37)]:
                self.box(s,'#d8a35c',(x+dx,y+dy,3,3))

    def pot(self,s,x,y,flower=False):
        self.box(s,'#7f4f37',(x-3,y-1,7,5))
        self.box(s,'#c17b4b',(x-4,y-2,9,3))
        self.box(s,'#365f42',(x-1,y-8,3,6))
        self.box(s,'#6b904c',(x-5,y-7,5,3))
        self.box(s,'#81a453',(x+2,y-10,4,4))
        if flower:
            self.box(s,'#e9ad85',(x-3,y-11,4,4))
            self.box(s,'#f4d46d',(x+3,y-13,3,3))

    def bench(self,s,x,y):
        self.shadow(s,x,y+6,29,8)
        for xx in (x-10,x+9): self.box(s,'#4d5144',(xx,y-4,2,13))
        for yy in (-6,-2,3):
            self.box(s,'#815236',(x-13,y+yy,28,3))
            self.box(s,'#c18b51',(x-13,y+yy,28,1))

    def lamp(self,s,x,y):
        self.shadow(s,x+2,y+1,11,4)
        self.box(s,'#434f46',(x-1,y-30,3,32))
        self.box(s,'#434f46',(x-5,y-34,11,8))
        self.box(s,'#f8db8f',(x-3,y-33,7,5))
        self.box(s,'#434f46',(x-4,y-36,9,2))

    def house(self,s,x,y,style):
        walls=['#e3bf88','#e9d3a0','#a9c8b0','#dfac8b']
        roofs=['#a85c45','#896348','#608480','#ae6048']
        self.box(s,'#6e7851',(x-19,y-4,48,10))
        self.box(s,'#674e3d',(x-23,y-38,46,39))
        self.box(s,walls[style],(x-21,y-36,42,35))
        self.box(s,'#c39768',(x-21,y-5,42,5))
        for dx in (-16,9):
            self.box(s,'#6e5a48',(x+dx,y-23,10,12))
            self.box(s,'#71939a',(x+dx+1,y-22,8,9))
            self.box(s,'#b9d5c4',(x+dx+2,y-21,2,7))
            self.box(s,'#f3e2b8',(x+dx-1,y-12,12,2))
            self.box(s,'#634936',(x+dx+4,y-23,1,11))
        self.box(s,'#54463c',(x-5,y-17,10,17))
        self.box(s,'#9b7047',(x-4,y-16,8,15))
        self.box(s,'#e6c783',(x+1,y-9,2,2))
        pygame.draw.polygon(s,'#573f36',[(x-28,y-32),(x-19,y-53),(x+17,y-53),(x+28,y-32)])
        pygame.draw.polygon(s,roofs[style],[(x-26,y-34),(x-18,y-51),(x+16,y-51),(x+25,y-34)])
        for row in range(4):
            yy=y-49+row*4
            half=17+row*2
            pygame.draw.line(s,'#d89967' if style!=2 else '#8fafa1',(x-half,yy),(x+half,yy))
            for col in range(-half+3,half,7):
                self.box(s,'#694b3e' if style!=2 else '#466760',(x+col+(row%2)*2,yy+1,1,3))
        self.box(s,'#edc389',(x-21,y-33,43,2))
        self.box(s,'#795644',(x+12,y-58,6,11))
        self.box(s,'#af7a54',(x+11,y-59,8,3))
        self.pot(s,x-21,y+1,True)
        self.pot(s,x+22,y+1,style%2==0)
        self.box(s,'#bda887',(x-8,y,17,3))

    def stall(self,s,x,y):
        self.shadow(s,x,y+2,50,10)
        for xx in (x-22,x+21): self.box(s,'#705039',(xx,y-28,3,29))
        self.box(s,'#89603d',(x-24,y-12,49,12))
        for xx in range(x-22,x+24,8): self.box(s,'#b58b52',(xx,y-11,6,10))
        self.box(s,'#e6c78c',(x-25,y-14,51,3))
        for dx in (-15,0,14): self.basket(s,x+dx,y-17)
        pygame.draw.polygon(s,'#3e725d',[(x-28,y-29),(x-20,y-43),(x+20,y-43),(x+28,y-29)])
        for dx in range(-20,25,12):
            pygame.draw.polygon(s,'#ecd49a',[(x+dx,y-42),(x+dx+5,y-42),(x+dx+8,y-29),(x+dx,y-29)])
        self.box(s,'#365b4d',(x-28,y-29,56,6))
        for dx in range(-28,28,12): self.box(s,'#e8ce95',(x+dx,y-29,6,6))

    def basket(self,s,x,y):
        self.box(s,'#695039',(x-6,y-4,13,9))
        self.box(s,'#c1914e',(x-5,y-3,11,7))
        self.box(s,'#f0ce87',(x-6,y-3,13,2))
        for dx in (-3,1,4): self.box(s,'#9b6b3d',(x+dx,y,1,4))
        self.box(s,'#6b8e48',(x-4,y-6,4,3))
        self.box(s,'#d76e46',(x+1,y-6,4,3))

    def make_ground(self):
        s=pygame.Surface((384,240))
        s.fill('#92a66a')
        rng=random.Random(101)
        for _ in range(1900):
            x,y=rng.randrange(384),rng.randrange(240)
            self.box(s,rng.choice(['#889e62','#a3b478','#99ae70']),(x,y,2,1))
        routes=[[(60,60),(60,204)],[(60,84),(228,84)],[(60,132),(108,132),(108,84)],
                [(180,60),(180,84),(204,84),(204,204),(180,204)],
                [(204,180),(348,180)],[(348,180),(348,60),(324,60)],[(324,180),(348,180)]]
        for route in routes:
            pygame.draw.lines(s,'#78845b',False,route,23)
            pygame.draw.lines(s,'#b7ae87',False,route,21)
            pygame.draw.lines(s,'#d8c99b',False,route,17)
        for _ in range(750):
            x,y=rng.randrange(384),rng.randrange(240)
            if s.get_at((x,y))[:3]==(216,201,155):
                self.box(s,rng.choice(['#c3b78d','#e4d7aa']),(x,y,2,1))
        for x in (120,240):
            for y in range(0,240,8):
                self.box(s,'#6b704d',(x,y,24,8))
                self.box(s,'#a99a70',(x+2,y,19,7))
                self.box(s,'#c2b184',(x+2,y,19,2))
                self.box(s,'#8b815d',(x+10+(y//8%2)*5,y+2,1,5))
            for y in range(0,240,24):
                if (x==120 and y==72) or (x==240 and y==168): continue
                self.box(s,'#416547',(x+4,y+2,15,17))
                self.box(s,'#63814b',(x+3,y+1,16,12))
                self.box(s,'#86a15e',(x+5,y+1,11,4))
        for x,y in [(26,92),(86,65),(286,120)]: self.bench(s,x,y)
        for x,y in [(98,170),(221,119),(366,153)]: self.lamp(s,x,y)
        for x,y in [(40,186),(80,186),(291,70),(294,204),(363,79)]: self.pot(s,x,y,True)
        for _ in range(60):
            x,y=rng.randrange(384),rng.randrange(240)
            if s.get_at((x,y))[:3] in [(146,166,106),(136,158,98)]:
                self.box(s,'#e6d596',(x,y,2,2))
                self.box(s,'#6c8b4e',(x,y+2,1,2))
        pygame.draw.ellipse(s,'#72825a',(35,27,53,26))
        pygame.draw.ellipse(s,'#d3c6a0',(34,24,50,26))
        pygame.draw.ellipse(s,'#789e9b',(38,27,42,19))
        pygame.draw.ellipse(s,'#b3cbb5',(43,30,30,10),1)
        self.box(s,'#cabd96',(57,26,5,12))
        pygame.draw.ellipse(s,'#eee0af',(51,23,17,6))
        pygame.draw.line(s,'#70644c',(277,81),(305,90))
        for i,col in enumerate(['#e9c88b','#b6745d','#e6dcbb']):
            self.box(s,col,(280+i*8,84+i*2,6,9))
        for x,y in [(19,146),(19,156),(19,166)]:
            self.box(s,'#74583d',(x,y,14,7))
            self.box(s,'#bb8b50',(x+1,y+1,12,5))
            self.box(s,'#e1bc78',(x+1,y+1,12,1))
        return s

    def person(self,s,x,y,kind=0,phase=0,wheel=False,facing=1):
        x,y=int(x),int(y)
        self.shadow(s,x,y+3,18 if wheel else 13,5)
        bob=int(math.sin(phase)*1)
        y+=bob
        shirts=['#d4974f','#8c80a0','#ce8663','#66978b','#b56b64']
        skin=['#c99568','#edbc8d','#9e6e4c','#dca87b','#bf8960'][kind%5]
        hair=['#473b32','#524239','#d7d0ae','#3f3936','#d8cbb0'][kind%5]
        if wheel:
            self.box(s,'#3b4243',(x-7,y-9,14,11))
            self.box(s,'#567f87',(x-6,y-9,12,8))
            for dx in (-8,6):
                self.box(s,'#343b3b',(x+dx,y-7,3,13))
                self.box(s,'#bac3b1',(x+dx+1,y-5,1,9))
                self.box(s,'#5d716a',(x+dx+1,y-4+int(phase*3)%5,1,2))
            self.box(s,'#37566a',(x-4,y-4,8,6))
            self.box(s,'#443c36',(x-5,y+1,4,3))
            self.box(s,'#443c36',(x+1,y+1,4,3))
        else:
            stride=int(math.sin(phase)*2)
            self.box(s,'#495966',(x-4,y-3,3,7+stride))
            self.box(s,'#495966',(x+1,y-3,3,7-stride))
            self.box(s,'#493f35',(x-5,y+3+stride,4,2))
            self.box(s,'#493f35',(x+1,y+3-stride,4,2))
        self.box(s,shirts[kind%5],(x-5,y-13,10,10))
        self.box(s,'#ecd5a3',(x-1,y-12,2,7))
        self.box(s,skin,(x-7,y-11,2,7))
        self.box(s,skin,(x+5,y-11,2,7))
        self.box(s,hair,(x-5,y-24,10,10))
        self.box(s,skin,(x-4,y-21,8,8))
        self.box(s,hair,(x-5,y-24,10,4))
        self.box(s,hair,(x-5,y-21,2,4))
        if facing>=0:
            self.box(s,'#3e3933',(x-1,y-18,1,1))
            self.box(s,'#3e3933',(x+3,y-18,1,1))
        else:
            self.box(s,'#3e3933',(x-3,y-18,1,1))
            self.box(s,'#3e3933',(x+1,y-18,1,1))
        if kind==2:
            self.box(s,'#654e38',(x+8,y-6,1,12))
        if kind==3 and not wheel:
            self.box(s,'#48534a',(x+9,y-4,2,8))
            pygame.draw.ellipse(s,'#bc9468',(x+9,y-9,11,10))
            self.box(s,'#424d43',(x+11,y+1,2,4))
            self.box(s,'#424d43',(x+18,y+1,2,4))

    def tick(self,dt,moved):
        self.time+=min(dt,.05)
        self.moving=moved.length_squared()>.01
        if self.moving:
            self.walk+=moved.length()*.11
            if abs(moved.x)>.1: self.facing=1 if moved.x>0 else -1
        for p in self.particles:
            p[0]+=p[2]*dt; p[1]+=p[3]*dt; p[3]+=22*dt; p[4]-=dt
        self.particles=[p for p in self.particles if p[4]>0]

    def burst(self,good):
        x,y=self.g.world.pos/2
        rng=random.Random(int(self.time*100))
        for _ in range(18 if good else 5):
            self.particles.append([x,y-8,rng.uniform(-26,26),rng.uniform(-45,-12),rng.uniform(.5,1.2),rng.choice(['#f6d77d','#f4edc5','#9ac27a']) if good else '#d08667'])

    def world_surface(self,preview=False):
        w=self.g.world
        s=self.ground.copy()
        for tile,opened in w.gates.items():
            x,y=tile[0]*24,tile[1]*24
            self.box(s,'#766951',(x,y,24,24))
            if opened:
                self.box(s,'#c6b48b',(x,y+1,24,22))
                for xx in range(2,24,4): self.box(s,'#a39373',(x+xx,y+3,1,18))
                self.box(s,'#e0cf9e',(x,y+1,24,2))
                self.box(s,'#e0cf9e',(x,y+21,24,2))
                pygame.draw.lines(s,'#4f7b67',False,[(x+8,y+15),(x+11,y+18),(x+17,y+10)],2)
            else:
                for xx in range(0,24,6):
                    self.box(s,'#ddd0a2',(x+xx,y+2,5,21))
                    self.box(s,'#a18e6b',(x+xx+4,y+2,2,21))
                self.box(s,'#c18b48',(x+1,y+1,22,3))
                self.box(s,'#c18b48',(x+1,y+21,22,3))
        drawables=[]
        for x,y,seed in self.trees:
            drawables.append((y,lambda x=x,y=y,seed=seed:self.tree(s,x,y,seed)))
        for i,r in enumerate(w.residents):
            x,y=r.tile[0]*24+12,r.tile[1]*24+12
            drawables.append((y-12,lambda x=x,y=y,i=i:self.house(s,x,y,i)))
            drawables.append((y+18,lambda x=x,y=y,i=i:self.person(s,x,y+18,i+1,math.sin(self.time+i)*.4)))
        drawables.append((118,lambda:self.stall(s,60,118)))
        for i,(tile,opened) in enumerate(w.gates.items()):
            if opened or preview:
                x=tile[0]*24+12+math.sin(self.time*.6+i)*25
                y=tile[1]*24+12
                drawables.append((y,lambda x=x,y=y,i=i:self.person(s,x,y,i+2,self.time*6)))
        px,py=w.pos/2
        drawables.append((py,lambda:self.person(s,px,py,0,self.walk if self.moving else 0,True,self.facing)))
        for _,draw in sorted(drawables,key=lambda item:item[0]): draw()
        for p in self.particles:
            self.box(s,p[5],(p[0],p[1],2,2))
        for i in range(4):
            phase=(self.time*1.7+i*.7)%2
            self.box(s,'#e3e9c4',(56+math.sin(i*3+phase)*8,26-phase*5,1,2))
        for i in range(12):
            x=(i*47+self.time*5)%384; y=(i*31+self.time*2)%240
            self.box(s,'#d9cf86',(x,y,2,1))
        return s

    def marker(self,text,x,y,done=False):
        s=self.g.canvas
        yy=int(y+math.sin(self.time*2.5+x)*2)
        color='#c5d797' if done else '#fff0bb'
        pygame.draw.polygon(s,'#554b3c',[(x-7,yy+19),(x,yy+27),(x+7,yy+19)])
        self.box(s,'#554b3c',(x-13,yy-3,26,25))
        self.box(s,color,(x-11,yy-1,22,21))
        self.label(text,x-7,yy-3,18,INK,True)

    def map(self):
        g=self.g
        self.box(g.canvas,'#443e32',(24,148,784,496))
        self.box(g.canvas,'#c5ae79',(28,152,776,488))
        g.canvas.blit(pygame.transform.scale(self.world_surface(),(768,480)),(32,156))
        for i,r in enumerate(g.world.residents):
            x,y=32+r.tile[0]*48+24,156+r.tile[1]*48+24
            if not r.done: self.marker(str(i+1),x+33,y-43)
        for i,(tile,opened) in enumerate(g.world.gates.items()):
            if not opened:
                self.marker('AB'[i],32+tile[0]*48+24,156+tile[1]*48-36)
        target=g.world.target()
        if target and g.scene=='game':
            px,py=g.world.pos
            self.box(g.canvas,'#433f34',(int(px)+19,int(py)+169,28,25))
            self.box(g.canvas,CREAM,(int(px)+21,int(py)+171,24,21))
            self.label('E',int(px)+26,int(py)+168,18,INK,True)

    def hud(self):
        g=self.g; w=g.world
        self.label('BAIRRO SEM BARREIRAS',32,19,27,CREAM,True)
        self.label('Sábado de mutirão',34,54,17,'#c6cfab')
        self.panel((32,91,768,48))
        for x,title in [(50,'PRAÇA DO ENCONTRO'),(335,'VILA DAS FLORES'),(588,'JARDIM DO SOL')]:
            self.label(title,x,104,15,MOSS,True)
        self.panel((828,26,260,89),False)
        seconds=math.ceil(w.remaining)
        self.label('SEM PRESSA' if w.practice else f'{seconds//60:02}:{seconds%60:02}',850,35,33,CREAM,True)
        self.label('exploração livre' if w.practice else 'até o fim do mutirão',850,79,16,'#e0c596')
        self.panel((828,139,260,497))
        self.label('CADERNO DO MUTIRÃO',848,159,17,MOSS,True)
        self.box(g.canvas,'#ccb88a',(848,191,218,2))
        self.label('Na mochila',848,207,21,INK,True)
        for i in range(2):
            icon=pygame.Surface((24,24),pygame.SRCALPHA)
            self.basket(icon,12,12)
            if i>=w.food: icon.set_alpha(50)
            g.canvas.blit(pygame.transform.scale(icon,(48,48)),(846+i*45,240))
        self.label(f'{w.food}/2 cestas',950,251,18,INK)
        self.label(f'Rampas: {w.kits} kit',848,295,20,INK,True)
        self.label('E na base para repor',848,325,16,'#766b55')
        self.box(g.canvas,'#ccb88a',(848,359,218,2))
        self.label('Quem vamos visitar?',848,376,19,INK,True)
        for i,r in enumerate(w.residents):
            yy=413+i*34
            self.box(g.canvas,'#b3a078',(850,yy+4,17,17))
            self.box(g.canvas,'#ebe0b6',(852,yy+6,13,13))
            if r.done:
                pygame.draw.lines(g.canvas,MOSS,False,[(852,yy+11),(857,yy+16),(867,yy+5)],3)
            self.label(f'{i+1}. {r.name}',880,yy,18,MOSS if r.done else INK,r.done)
        self.label(f'{sum(w.gates.values())}/2 passagens acessíveis',848,572,17,MOSS,True)
        self.panel((32,659,1056,76))
        target=w.target()
        hint='WASD / setas: mover     E: conversar / agir     P: pausa     M: som'
        if target:
            hint={'station':'[E] Pegar cestas e kit de rampa na barraca', 'ramp':'[E] Instalar rampa nesta passagem', 'resident':'[E] Entregar cesta e conversar'}[target[0]]
        self.label(hint,50,671,18,MOSS,True)
        self.wrap(w.message if w.message_time else 'Um bairro acessível é um bairro em que todo mundo pode participar.',50,701,1010,17,INK)

    def button(self,label,rect,action,primary=False):
        x,y,w,h=rect
        sw,sh=self.g.screen.get_size(); scale=min(sw/1120,sh/760)
        mx,my=pygame.mouse.get_pos()
        mouse=((mx-(sw-1120*scale)/2)/scale,(my-(sh-760*scale)/2)/scale)
        hovered=pygame.Rect(rect).collidepoint(mouse)
        self.box(self.g.canvas,'#302e27',(x+3,y+5,w,h))
        self.box(self.g.canvas,'#3f4f36' if primary else '#614a35',rect)
        self.box(self.g.canvas,'#a8ba76' if hovered and primary else '#8da465' if primary else '#e2c591' if hovered else '#cdb27d',(x+3,y+3,w-6,h-6))
        self.box(self.g.canvas,'#c6d38f' if primary else '#e9d5a5',(x+3,y+3,w-6,3))
        self.label(label,x+20,y+12,21,'#273e32' if primary else INK,True)
        self.g.buttons.append((pygame.Rect(rect),action))

    def menu(self):
        g=self.g
        scene=pygame.transform.scale(self.world_surface(True),(1216,760))
        g.canvas.blit(scene,(-40,0))
        veil=pygame.Surface((1120,760),pygame.SRCALPHA)
        veil.fill((26,44,35,65)); g.canvas.blit(veil,(0,0))
        self.panel((53,56,528,634))
        self.label('UMA HISTÓRIA DO NOSSO BAIRRO',84,87,16,MOSS,True)
        self.label('Bairro Sem',80,128,58,INK,True)
        self.label('Barreiras',80,190,66,MOSS,True)
        self.box(g.canvas,'#cfb67f',(86,280,457,2))
        self.wrap('Hoje é dia de mutirão. Junte-se a Alex, abra caminhos e leve cuidado aos vizinhos.',86,307,444,22,INK)
        self.button('Começar o mutirão   [Enter]',(86,423,456,58),'start',True)
        self.button('Passear sem pressa   [T]',(86,498,456,58),'practice')
        self.label('WASD / setas para mover  ·  E para agir',86,586,19,INK)
        self.label('4 vizinhos. 2 passagens. Um bairro para todos.',86,624,17,MOSS)
        portrait=pygame.Surface((80,90),pygame.SRCALPHA)
        self.person(portrait,40,65,0,0,True)
        g.canvas.blit(pygame.transform.scale(portrait,(320,360)),(696,290))
        self.panel((716,586,300,82),False)
        self.label('ALEX',743,596,25,CREAM,True)
        self.label('Todo caminho começa junto.',740,633,17,'#ead3a2')
        self.label('Um pequeno gesto transforma o lugar onde a gente vive.',281,723,18,CREAM)

    def overlay(self,result=False):
        g=self.g; w=g.world
        shade=pygame.Surface((1120,760),pygame.SRCALPHA)
        shade.fill((28,39,30,195)); g.canvas.blit(shade,(0,0))
        self.panel((230,140,660,480))
        if not result:
            self.label('A praça pode esperar.',267,181,36,MOSS,True)
            self.wrap('Respire um pouco. Seu progresso está guardado nesta partida e o relógio está parado.',270,256,565,23)
            self.button('Voltar ao bairro   [P / Esc]',(270,405,570,57),'resume',True)
            self.button('Voltar ao início   [Q]',(270,487,570,57),'menu')
        else:
            won=w.status=='won'
            self.label('O bairro é de todos!' if won else 'Amanhã tem mais.',267,179,38,MOSS,True)
            self.label(f'{sum(r.done for r in w.residents)} vizinhos atendidos  /  {sum(w.gates.values())} passagens abertas',270,245,22,INK,True)
            self.wrap('As cestas chegaram, as conversas aconteceram e os caminhos ficaram. Um bairro melhor se faz junto.' if won else 'O dia passou rápido. Que tal buscar os suprimentos antes de seguir para o Jardim? Você também pode passear sem pressa.',270,303,565,23)
            self.button('Mais um mutirão   [R]',(270,443,570,57),'retry',True)
            self.button('Voltar ao início   [Esc]',(270,523,570,57),'menu')
