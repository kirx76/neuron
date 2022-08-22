import random

import pygame

from subwaySurfs.train import Train

player_height = 50
max_trains_in_a_row = 2
train_spawn_timeout = (200 + player_height + 30) / 2


class Game:
    def __init__(self, width, height, frame_rate, surface):
        self.frame_rate = frame_rate
        self.width = width
        self.height = height
        self.game_over = False
        self.surface = surface
        self.clock = pygame.time.Clock()

        self.trains = []

        self.create_random_train()
        self.spawn_timeout = train_spawn_timeout

        pygame.init()
        pygame.display.set_caption('Subway Surfers')
        pygame.font.init()

    def run(self):
        while not self.game_over:
            self.surface.fill((0, 0, 0))

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)

    def update_trains(self):
        for train in self.trains:
            if train.destroyed:
                self.trains.remove(train)
            else:
                train.update()

    def draw_trains(self):
        for train in self.trains:
            train.draw(self.surface)

    def get_left_top_train(self):
        left_trains = []
        for train in self.trains:
            if train.bounds.x < 200:
                left_trains.append(train)
        left_top_train = None
        for left_train in left_trains:
            if left_train.bounds.y < left_top_train.bounds.y if left_top_train else self.height:
                left_top_train = left_train
        return left_top_train
        # if left_top_train and left_top_train.bounds.y > player_height + 30:
        #     self.create_train()

    def get_center_top_train(self):
        center_trains = []
        for train in self.trains:
            if 200 <= train.bounds.x <= 399:
                center_trains.append(train)

        center_top_train = None
        for center_train in center_trains:
            if center_train.bounds.y < center_top_train.bounds.y if center_top_train else self.height:
                center_top_train = center_train
        return center_top_train
        # if center_top_train and center_top_train.bounds.y > player_height + 30:
        #     self.create_train()

    def get_right_top_train(self):
        right_trains = []
        for train in self.trains:
            if train.bounds.x >= 400:
                right_trains.append(train)

        right_top_train = None
        for right_train in right_trains:
            if right_train.bounds.y < right_top_train.bounds.y if right_top_train else self.height:
                right_top_train = right_train
        return right_top_train
        # if right_top_train and right_top_train.bounds.y > player_height + 30:
        #     self.create_train()

    def generate_trains(self):
        self.create_train()
        return
        if self.spawn_timeout <= 0:
            self.create_train()
            self.spawn_timeout = train_spawn_timeout
        self.spawn_timeout -= 1

    def update(self):
        self.update_trains()
        self.generate_trains()

    def draw(self):
        self.draw_trains()

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

        print(array)

        for index, i in enumerate(array):
            if i == 1:
                train = Train(self.surface, self.width, self.height, index * self.width // 3)
                self.add_train(train)
        self.spawn_timeout = train_spawn_timeout

    def create_random_train(self):
        train = Train(self.surface, self.width, self.height, random.randint(1, 3) * self.width // 3)
        self.add_train(train)

    def add_train(self, train):
        self.trains.append(train)
