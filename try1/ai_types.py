
import random

import libtcodpy as libtcod

from fysom import Fysom

class BasicAI:
    def __init__(self, world):
        self.map = world.map
        self.pathing = self.map.path_map
        self.path = []
        self.fsm = Fysom({
            'initial': 'spawning',
            'events': [
                { 'name': 'stop',
                  'src': ['spawning', 'exploring'],
                  'dst': 'idle' },
                { 'name': 'explore',
                  'src': ['idle'],
                  'dst': 'exploring' },
            ]
        })

    def get_path_to(self, nx, ny):
        entity = self.owner
        path = []
        libtcod.path_compute(self.pathing, entity.x, entity.y, nx, ny)

        for i in range(libtcod.path_size(self.pathing)):
            (x, y) = libtcod.path_get(self.pathing, i)
            path.append((x, y))

        path.reverse()
        return path

    def get_path_to_random(self):
        (nx, ny) = self.map.get_random_position()
        self.path = self.get_path_to(nx, ny)

    def update(self):
        entity = self.owner
        if self.fsm.isstate('spawning'):
            self.fsm.stop()
        elif self.fsm.isstate('idle'):
            if random.random() < 0.3:
                self.fsm.explore()
        elif self.fsm.isstate('exploring'):
            if len(self.path) < 1:
                if random.random() < 0.01:
                    return self.fsm.stop()
                self.get_path_to_random()

            if len(self.path) > 0:
                (x, y) = self.path.pop()
                if entity.can_move_abs(x, y, self.map):
                    entity.move_abs(x, y, self.map)
                else:
                    return self.get_path_to_random()
            else:
                self.get_path_to_random()
