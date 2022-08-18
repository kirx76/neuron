import pygame
from pygame.rect import Rect

from game.GameObject import GameObject
from game.config import height


class Ball(GameObject):
    def __init__(self, x, y, r, color, speed, paddle):
        GameObject.__init__(self,
                            x - r,
                            y - r,
                            r * 2,
                            r * 2,
                            speed)
        self.radius = r
        self.diameter = r * 2
        self.color = color
        self.paddle = paddle

    def draw(self, surface):
        pygame.draw.circle(surface,
                           self.color,
                           self.center,
                           self.radius)

    def destroy(self):
        self.paddle.destroy_ball(self)

    def update(self):
        GameObject.update(self)
        if self.top >= height:
            self.paddle.genome.fitness -= 0.5
            self.paddle.decrease_score()
            self.paddle.decrease_max_balls()
            self.destroy()
