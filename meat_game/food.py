import random

import pygame.draw

from GameObject import GameObject

food_size = 10
food_color = (0, 255, 0)
food_weight = 1


def get_random_vector(min_value, prop):
    return random.randint(min_value, prop)


class Food(GameObject):
    def __init__(self, game_width, game_height, color=food_color, food_value=food_weight):
        GameObject.__init__(self, get_random_vector(food_value, game_width - food_size),
                            get_random_vector(food_size, game_height - food_size),
                            food_size * 2, food_size * 2, (0, 0))
        self.radius = food_size
        self.diameter = food_size * 2
        self.color = color
        self.destroyed = False
        self.food_value = food_value

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)

    def destroy(self):
        self.destroyed = True

    def update(self):
        GameObject.update(self)
