import random

import pygame

from GameObject import GameObject


class Plank(GameObject):
    def __init__(self, x, y, w, h, color, surface, game_width, game_height, plank_speed):
        GameObject.__init__(self, x, y, w - random.randint(20, 30), h, plank_speed)
        self.color = color
        self.surface = surface
        self.game_width = game_width
        self.game_height = game_height
        self.destroy = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def destroy_plank(self):
        self.destroy = True

    def update(self):
        GameObject.update(self)
        if self.top >= self.surface.get_height():
            self.destroy_plank()


plank_width = 100
plank_height = 25
empty_count = 3


class Wall:
    def __init__(self, color, surface, game_width, game_height, offset, wall_speed):
        self.planks = []
        self.color = color
        self.surface = surface
        self.game_width = game_width
        self.game_height = game_height
        self.offset = offset
        self.speed = wall_speed

        self.destroy = False

        self.generate_plank_line()

    def generate_plank_line(self):
        plank_count = self.game_width // plank_width
        plank_array = []

        deleted = random.sample(range(0, plank_count), empty_count)

        for i in range(plank_count):
            if i not in deleted:
                x = i * plank_width
                y = 100 * self.offset
                plank_array.append(Plank(x, y, plank_width, plank_height, self.color, self.surface, self.game_width,
                                         self.game_height, self.speed))
        self.planks = plank_array

    def add_plank(self, plank):
        self.planks.append(plank)

    def draw(self, surface):
        for plank in self.planks:
            plank.draw(surface)

    def update(self):
        for plank in self.planks:
            plank.update()
            if plank.destroy:
                self.destroy = True
                break
