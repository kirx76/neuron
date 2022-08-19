import random

import pygame

from GameObject import GameObject
from car_game.wall import Wall
from game.TextObject import TextObject

wall_width = 100
wall_height = 10
wall_top_offset = 50
wall_count = 1


class Car(GameObject):
    def __init__(self, w, h, color, game_width, game_height, identificator, surface, net, genome, speed=(0, 0)):
        GameObject.__init__(self, game_width / 2, game_height - h - 15, w, h, speed)
        self.color = color
        self.speed = speed

        self.game_width = game_width
        self.game_height = game_height
        self.surface = surface

        self.net = net
        self.genome = genome
        self.genome.fitness = 10

        self.current_wall_count = wall_count

        self.alive_time = 0
        self.time_out_of_bounds = 0
        self.score = 0
        self.identificator = identificator

        self.wall_offset = 0

        self.walls = []

        self.wall_speed = (0, 5)

        self.destroyed = False

    def self_draw(self, surface):
        self.show_score('Score: ' + str(self.score))
        pygame.draw.rect(surface, self.color, self.bounds)

    def draw_walls(self, surface):
        for wall in self.walls:
            wall.draw(surface)

    def draw(self, surface):
        self.self_draw(surface)
        self.draw_walls(surface)

    def self_update(self):
        if self.time_out_of_bounds > 10:
            self.genome.fitness -= 2
            self.genome.fitness += self.score
            self.destroyed = True
        self.update_intersections()
        self.alive_time += 1
        GameObject.update(self)
        self.update_car_movement()

    def update_car_movement(self):
        if self.left <= 0:
            self.time_out_of_bounds += 1
        if self.right >= self.game_width:
            self.time_out_of_bounds += 1
        closest_plank = self.get_closest_plank()
        if closest_plank is not None:
            power, way = self.net.activate((self.left, self.right, closest_plank.left, closest_plank.right,
                                            abs(self.left - self.game_width // 2),
                                            abs(self.right - self.game_width // 2),
                                            abs(self.left - closest_plank.left), abs(self.right - closest_plank.right)))
            if way > 0:
                dx = min(power * 10, self.game_width - self.right)
            else:
                dx = -min(power * 10, 0)
            if abs(dx) > 0:
                self.genome.fitness -= 0.1
            self.move(dx, 0)
        return

        collisions, rays, planks = self.draw_lines()
        collisions.insert(self.width, 0)
        collisions.insert(self.right, 0)
        collisions.insert(self.left, 0)
        collisions.insert(self.centerx, 0)
        power, way = self.net.activate(tuple(collisions))
        if way > 0:
            dx = min(power * 10, self.game_width - self.right)
        else:
            dx = -min(power * 10, 0)
        if self.left - dx < 5:
            dx = 0
        if self.right + dx > self.game_width - 5:
            dx = 0
        if abs(dx) > 0:
            self.genome.fitness -= 0.1
        self.move(dx, 0)
        # if self.left < 0:
        #     self.genome.fitness -= 1
        #     self.time_out_of_bounds += 1
        # if self.right > self.game_width:
        #     self.genome.fitness -= 1
        #     self.time_out_of_bounds += 1
        # cw, cd = self.get_closest_wall()
        # if cw is not None:
        #     power, way = self.net.activate(
        #         (self.centerx, self.left, self.right, self.width, cw.centerx, cw.left, cw.right, cw.width,
        #          abs(self.left - cw.left), abs(self.right - cw.right)))
        #     if way > 0:
        #         dx = min(power * 10, self.game_width - self.right)
        #     else:
        #         dx = -min(power * 10, 0)
        #     if self.left - dx < 5:
        #         dx = 0
        #     if self.right + dx > self.game_width - 5:
        #         dx = 0
        #     if abs(dx) > 0:
        #         self.genome.fitness -= 0.1
        #     self.move(dx, 0)

    def update_intersections(self):
        for wall in self.walls:
            for plank in wall.planks:
                if self.bounds.colliderect(plank.bounds):
                    self.genome.fitness -= 2
                    self.genome.fitness += self.score
                    self.destroyed = True

    def walls_update(self):
        for wall in self.walls:
            if wall.destroy:
                self.genome.fitness += 1
                self.score += 1
                self.walls.remove(wall)
            else:
                wall.update()
        if len(self.walls) < self.current_wall_count:
            self.create_random_wall()
            self.wall_offset += 1
        else:
            self.wall_offset = 0

        if self.score // 5 >= self.current_wall_count:
            self.wall_speed = self.wall_speed[0], self.wall_speed[1] + (((self.score // 5) * 0.5) // 5)

    def update(self):
        self.self_update()
        self.walls_update()

    def create_random_wall(self):
        self.add_wall(
            Wall(self.color, self.surface, self.game_width, self.game_height, self.wall_offset, self.wall_speed))

    def add_wall(self, wall):
        self.walls.append(wall)

    def get_closest_plank(self):
        closest_plank = None
        collisions, rays, planks = self.draw_lines()

        for plank in planks:
            closest_plank = plank
            break
        return closest_plank

    def create_rays(self):
        rays = []
        ray_left = pygame.draw.line(self.surface, (0, 0, 0), (self.left, self.top), (self.left, 0))
        ray_right = pygame.draw.line(self.surface, (0, 0, 0), (self.right, self.top), (self.right, 0))
        rays.append(ray_left)
        rays.append(ray_right)
        return rays
        # rays = []
        # # for i in range(self.game_width // 100):
        # #     ray = pygame.draw.line(self.surface, (255, 255, 255), (self.centerx, self.top), (i * 100, 0))
        # #     rays.append(ray)
        # ray_left = pygame.draw.line(self.surface, (255, 255, 255), (self.centerx, self.top), (0, 0))
        # ray_center = pygame.draw.line(self.surface, (255, 255, 255), (self.centerx, self.top), (self.game_width // 2, 0))
        # ray_right = pygame.draw.line(self.surface, (255, 255, 255), (self.centerx, self.top), (self.game_width, 0))
        # rays.append(ray_left)
        # rays.append(ray_center)
        # rays.append(ray_right)
        # return rays

    def draw_lines(self):
        rays = self.create_rays()
        collisions = [0] * len(rays)
        planks = []
        for i, ray in enumerate(rays):
            for wall in self.walls:
                for plank in wall.planks:
                    if ray.colliderect(plank.bounds):
                        rays[i] = pygame.draw.line(self.surface, self.color, (ray.x, self.top), (ray.x, plank.bottom))
                        collisions[i] = 1
                        planks.append(plank)
                        break
        return collisions, rays, planks

    def show_score(self,
                   text,
                   font_name='Arial',
                   font_size=20,
                   centralized=False):
        message = TextObject(20,
                             self.identificator * 15 + 10,
                             lambda: text, self.color,
                             font_name, font_size)
        message.draw(self.surface, centralized)
