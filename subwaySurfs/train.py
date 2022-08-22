import random

import pygame

from GameObject import GameObject

train_width = 190
train_color = (255, 255, 0)
train_speed = (0, 2)


def get_random_train_height():
    return 150
    return random.randint(100, 200)


class Train(GameObject):
    def __init__(self, surface, game_width, game_height, train_pos_x, color=train_color, width=train_width,
                 height=get_random_train_height(), speed=train_speed):
        GameObject.__init__(self, train_pos_x, 0, width, height)
        self.surface = surface
        self.color = color
        self.destroyed = False
        self.game_width = game_width
        self.game_height = game_height
        self.speed = speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.bounds)

    def update(self):
        GameObject.update(self)
        if self.bounds.y >= self.game_height - 50:
            self.destroyed = True
