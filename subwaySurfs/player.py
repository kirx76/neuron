import random

import pygame.draw

from GameObject import GameObject
from subwaySurfs.game import player_height, train_spawn_timeout
from subwaySurfs.train import Train

player_color = (255, 0, 0)


class Player(GameObject):
    def __init__(self, surface, game_width, game_height, net, genome, current_id, color=player_color, speed=(0, 0)):
        GameObject.__init__(self, (game_width / 2) - player_height / 2, game_height - player_height * 2, player_height,
                            player_height)
        self.surface = surface
        self.color = color
        self.net = net
        self.genome = genome
        self.genome.fitness = 0
        self.current_id = current_id
        self.destroyed = False
        self.game_width = game_width
        self.game_height = game_height
        self.speed = speed
        self.pos = 0

        self.trains = []
        self.spawn_timeout = train_spawn_timeout
        self.create_random_train()

    # TRAINS SECTION START
    def update_trains(self):
        for train in self.trains:
            if train.destroyed:
                self.trains.remove(train)
            else:
                train.update()

    def update_trains_collision(self):
        for train in self.trains:
            if self.bounds.colliderect(train.bounds):
                self.destroy()

    def draw_trains(self):
        for train in self.trains:
            train.draw(self.surface)

    def generate_trains(self):
        self.create_train()

    def create_random_train(self):
        train = Train(self.surface, self.game_width, self.game_height, random.randint(1, 3) * self.game_width // 3,
                      self.color)
        self.add_train(train)

    def add_train(self, train):
        self.trains.append(train)

    def create_train(self):
        self.spawn_timeout -= 1
        if self.spawn_timeout > 0:
            return
        array = []
        left = self.get_left_top_train()
        center = self.get_center_top_train()
        right = self.get_right_top_train()

        if left and left.bounds.y >= player_height + 150 + 30 and len(array) <= 2:
            array.append(1)
        else:
            array.append(0)
        if center and center.bounds.y >= player_height + 150 + 30 and len(array) <= 2:
            array.append(1)
        else:
            array.append(0)
        if right and right.bounds.y >= player_height + 150 + 30 and len(array) <= 2:
            array.append(1)
        else:
            array.append(0)

        random.shuffle(array)
        if len(array) == 3:
            array[0] = 0
            random.shuffle(array)

        array_sum = sum(array)
        if array_sum < 1:
            array[0] = 1
            random.shuffle(array)
        print(array)

        for index, i in enumerate(array):
            if i == 1:
                train = Train(self.surface, self.game_width, self.game_height, index * self.game_width // 3, self.color)
                self.add_train(train)
        self.spawn_timeout = train_spawn_timeout

    def get_left_trains(self):
        left_trains = []
        for train in self.trains:
            if train.bounds.x < 200:
                left_trains.append(train)
        return left_trains

    def get_left_top_train(self):
        left_trains = self.get_left_trains()
        left_top_train = None
        for left_train in left_trains:
            if left_train.bounds.y < left_top_train.bounds.y if left_top_train else self.game_height:
                left_top_train = left_train
        return left_top_train

    def get_center_trains(self):
        center_trains = []
        for train in self.trains:
            if 200 <= train.bounds.x <= 399:
                center_trains.append(train)
        return center_trains

    def get_center_top_train(self):
        center_trains = self.get_center_trains()
        center_top_train = None
        for center_train in center_trains:
            if center_train.bounds.y < center_top_train.bounds.y if center_top_train else self.game_height:
                center_top_train = center_train
        return center_top_train

    def get_right_trains(self):
        right_trains = []
        for train in self.trains:
            if train.bounds.x >= 400:
                right_trains.append(train)
        return right_trains

    def get_right_top_train(self):
        right_trains = self.get_right_trains()
        right_top_train = None
        for right_train in right_trains:
            if right_train.bounds.y < right_top_train.bounds.y if right_top_train else self.game_height:
                right_top_train = right_train
        return right_top_train

    def get_left_lowest_train(self):
        left_trains = self.get_left_trains()
        lowest_left_train = None
        lowest_left_train_distance = self.game_height
        for train in left_trains:
            if train.bottom < lowest_left_train_distance:
                lowest_left_train = train
                lowest_left_train_distance = train.bottom
        return lowest_left_train, lowest_left_train_distance

    def get_center_lowest_train(self):
        center_trains = self.get_center_trains()
        lowest_center_train = None
        lowest_center_train_distance = self.game_height
        for train in center_trains:
            if train.bottom < lowest_center_train_distance:
                lowest_center_train = train
                lowest_center_train_distance = train.bottom
        return lowest_center_train, lowest_center_train_distance

    def get_right_lowest_train(self):
        right_trains = self.get_right_trains()
        lowest_right_train = None
        lowest_right_train_distance = self.game_height
        for train in right_trains:
            if train.bottom < lowest_right_train_distance:
                lowest_right_train = train
                lowest_right_train_distance = train.bottom
        return lowest_right_train, lowest_right_train_distance

    # TRAINS SECTION END

    def destroy(self):
        self.destroyed = True

    def draw(self, surface):
        self.draw_trains()
        pygame.draw.rect(surface, self.color, self.bounds)

    def get_closest_train(self):
        lt, ltd = self.get_left_lowest_train()
        ct, ctd = self.get_center_lowest_train()
        rt, rtd = self.get_right_lowest_train()
        if self.pos < 0 and lt is not None:
            self.get_distance_to(lt.bounds, self.surface)
            return lt, ltd
        if self.pos == 0 and ct is not None:
            self.get_distance_to(ct, self.surface)
            return ct, ctd
        if self.pos > 0 and rt is not None:
            self.get_distance_to(rt, self.surface)
            return rt, rtd
        return None, self.game_height

    def self_update(self):
        ct, ctd = self.get_closest_train()

        pos = self.net.activate(
            (self.pos, ctd, ct.centery if ct is not None else 0, ct.centerx if ct is not None else -1))

        print(pos)
        if pos[0] < -0.25:
            self.pos = -1
        elif -0.25 <= pos[0] <= 0.25:
            self.pos = 0
        elif pos[0] > 0.25:
            self.pos = 1

        if self.pos < -0.25:
            self.bounds.x = (self.game_width // 3) / 2 - (player_height / 2)
            self.genome.fitness -= 0.1
        elif -0.25 <= self.pos <= 0.25:
            self.bounds.x = (self.game_width // 2) - (player_height / 2)
            self.genome.fitness -= 0.1
        elif self.pos > 0.25:
            self.bounds.x = self.game_width - 100 - player_height / 2
            self.genome.fitness -= 0.1

    def update(self):
        self.update_trains_collision()
        self.self_update()
        self.update_trains()
        self.generate_trains()
