import random

import pygame

from GameObject import GameObject
from game.TextObject import TextObject
from game.ball import Ball
from game.config import default_ball_size, max_score


def get_random_speed():
    return random.randint(5, 8)


class NeatPaddle(GameObject):
    def __init__(self, h, color, offset, balls_count, width, height, net, genome, genome_id):
        GameObject.__init__(self, width / 2, height - 15, width / 10, h)
        self.color = color
        self.offset = offset
        self.moving_left = False
        self.moving_right = False
        self.net = net
        self.genome = genome
        self.genome_id = genome_id
        self.genome.fitness = 10

        self.game_width = width
        self.game_height = height

        self.surface = pygame.display.set_mode((self.width, self.height))

        self.balls = []
        self.max_balls = balls_count

        self.score = 0

        self.destroyed = False

        self.create_balls()

        self.alive_time = 0

    def increase_score(self):
        self.genome.fitness += 0.1
        self.score += 1

    def decrease_score(self):
        self.genome.fitness -= 0.1
        self.score -= 1

    def create_default_ball(self):
        self.genome.fitness += 0.1
        self.add_ball(Ball(random.randint(0 + default_ball_size, self.game_width - default_ball_size),
                           random.randint(0 + default_ball_size, 50 - default_ball_size), default_ball_size,
                           self.color, (0, get_random_speed()), self))

    def add_ball(self, ball):
        self.balls.append(ball)

    def destroy_ball(self, ball):
        self.balls.remove(ball)

    def increase_max_balls(self):
        self.max_balls += 1

    def decrease_max_balls(self):
        self.max_balls -= 1

    def create_balls(self):
        if len(self.balls) < self.max_balls:
            self.create_default_ball()

    def show_score(self,
                   text,
                   font_name='Arial',
                   font_size=20,
                   centralized=False):
        message = TextObject(20,
                             self.genome_id * 15 + 10,
                             lambda: text, self.color,
                             font_name, font_size)
        message.draw(self.surface, centralized)

    def draw(self, surface):
        self.show_score('Score: ' + str(self.score))
        for b in self.balls:
            b.draw(surface)
        pygame.draw.rect(surface, self.color, self.bounds)

    def get_lowest_ball(self):
        lowest_ball = None
        lowest_distance = 0
        for ball in self.balls:
            distance = ball.bottom
            if distance > lowest_distance:
                lowest_ball = ball
                lowest_distance = distance
        return lowest_ball, lowest_distance

    def get_closest_ball(self):
        closest_ball = None
        closest_distance = self.game_width
        for ball in self.balls:
            distance = self.get_distance_to(ball, self.surface)
            if distance < closest_distance:
                closest_ball = ball
                closest_distance = distance
        return closest_ball, closest_distance

    def colliderect(self, ball):
        return self.bounds.colliderect(ball.bounds)

    def detect_intersect_with_ball(self, ball):
        if self.colliderect(ball):
            return True
        return False

    def draw_line_to_closest_ball(self, closest_ball):
        pygame.draw.line(self.surface, self.color, self.center, closest_ball.center)

    def update_by_balls(self):
        if len(self.balls) <= 0:
            self.genome.fitness -= 1
            self.destroyed = True
            return
        self.create_balls()
        for b in self.balls:
            if self.detect_intersect_with_ball(b):
                self.increase_max_balls()
                self.increase_score()
                self.genome.fitness += 0.1
                self.create_balls()
                self.destroy_ball(b)
            b.update()

    def update_movement(self, power, way):
        if way > 0:
            dx = power * self.offset
        else:
            dx = -(power * self.offset)
        self.genome.fitness -= 0.5
        self.move(dx, 0)
        if self.left <= 10:
            self.genome.fitness -= 1
            self.destroyed = True
        if self.right >= self.game_width - 10:
            self.genome.fitness -= 1
            self.destroyed = True

    def update(self):
        if self.alive_time > 1500:
            self.genome.fitness -= 1
            self.destroyed = True
            return
        if self.score >= max_score:
            self.genome.fitness += 1
            self.destroyed = True
            return

        self.update_by_balls()
        cb, cd = self.get_lowest_ball()
        print(cb, cd)

        if cb is not None:
            self.draw_line_to_closest_ball(cb)
            power, way = self.net.activate((self.centerx, self.width, cb.centerx, cb.width, cb.speed[0], cd))
            self.update_movement(power, way)
        self.alive_time += 1
