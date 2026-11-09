import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import unittest
from collections import deque
import pygame
from main import World, Game, TILE


class RulesTest(unittest.TestCase):
    def walk(self, world, target):
        start = (int(world.pos.x // TILE), int(world.pos.y // TILE))
        queue = deque([(start, [start])])
        visited = {start}
        path = None
        while queue:
            cell, route = queue.popleft()
            if cell == target:
                path = route
                break
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                p = cell[0]+dx, cell[1]+dy
                if p not in visited and not world.blocked(pygame.Vector2(p)*TILE+(24,24)):
                    visited.add(p)
                    queue.append((p, route+[p]))
        self.assertIsNotNone(path, f'Sem caminho para {target}')
        for cell in path[1:]:
            goal = pygame.Vector2(cell)*TILE+(24,24)
            for _ in range(100):
                delta = goal-world.pos
                if delta.length() < .1: break
                world.update(min(1/60, delta.length()/190), delta)
            self.assertLess(world.pos.distance_to(goal), .1)

    def test_complete_playthrough_with_real_movement(self):
        w = World()
        self.walk(w,(4,3)); self.assertTrue(w.interact())
        self.walk(w,(7,2)); self.assertTrue(w.interact())
        self.walk(w,(7,8)); self.assertTrue(w.interact())
        self.walk(w,(9,7)); self.assertFalse(w.interact())
        self.walk(w,(2,5)); self.assertTrue(w.interact())
        self.walk(w,(9,7)); self.assertTrue(w.interact())
        self.walk(w,(13,7)); self.assertTrue(w.interact())
        self.walk(w,(13,2)); self.assertTrue(w.interact())
        self.assertEqual(w.status, 'won')
        self.assertGreater(w.remaining, 0)

    def test_barrier_and_boundary_collisions(self):
        w = World()
        w.pos = pygame.Vector2(4.5*TILE,3.5*TILE)
        for _ in range(120): w.update(1/60,(1,0))
        self.assertLessEqual(w.pos.x,5*TILE-12)
        self.assertTrue(w.interact())
        for _ in range(30): w.update(1/60,(1,0))
        self.assertGreater(w.pos.x,6*TILE)
        self.assertTrue(w.blocked(pygame.Vector2(-1,100)))

    def test_timeout_and_practice(self):
        w = World(); w.remaining = .01; w.update(.02)
        self.assertEqual(w.status,'lost')
        self.assertFalse(w.interact())
        w = World(True); w.remaining = .01; w.update(.02)
        self.assertEqual(w.status,'playing')

    def test_no_remote_delivery_or_duplicate(self):
        w = World(); w.pos = pygame.Vector2(24,24)
        self.assertFalse(w.interact())
        w.pos = pygame.Vector2(w.residents[0].tile)*TILE+(24,24)
        self.assertTrue(w.interact()); self.assertFalse(w.interact())
        self.assertEqual(w.food,1)

    def test_diagonal_speed(self):
        a,b = World(),World()
        origin = a.pos.copy()
        a.update(.02,(1,0)); b.update(.02,(1,1))
        self.assertAlmostEqual(a.pos.distance_to(origin),b.pos.distance_to(origin))

    def test_screens_pause_restart_and_keyboard(self):
        game = Game()
        for scene in ('menu','game','pause','result'):
            game.scene = scene; game.draw()
        game.start(); game.scene = 'pause'
        remaining = game.world.remaining
        game.update(.05)
        self.assertEqual(game.world.remaining, remaining)
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN,key=pygame.K_p))
        game.input(); self.assertEqual(game.scene,'game')
        game.world.food = 0; game.action('retry')
        self.assertEqual(game.world.food,2)
        pygame.quit()

    def test_scaled_menu_click_and_visual_effects(self):
        game = Game()
        game.screen = pygame.display.set_mode((840,570))
        game.draw()
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN,button=1,pos=(150,345)))
        game.input()
        self.assertEqual(game.scene,'game')
        game.visuals.burst(True)
        self.assertEqual(len(game.visuals.particles),18)
        game.visuals.tick(.02,pygame.Vector2(3,0))
        self.assertTrue(game.visuals.moving)
        self.assertGreater(game.visuals.walk,0)
        for state in ('playing','won','lost'):
            game.world.status=state
            game.scene='game' if state=='playing' else 'result'
            game.draw()
        game.action('retry')
        self.assertFalse(game.visuals.particles)
        pygame.quit()


if __name__ == '__main__': unittest.main()
