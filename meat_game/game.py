import pygame

from meat_game.food import Food

initial_food_on_screen = 10


class MeatGame:
    def __init__(self, width, height, frame_rate, surface):
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.game_over = False
        self.surface = surface
        self.clock = pygame.time.Clock()
        self.food = []

        pygame.init()
        pygame.display.set_caption('Meat Game')
        pygame.font.init()

    def run(self):
        while not self.game_over:
            self.surface.fill((0, 0, 0))

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)

    def update(self):
        self.food_spawner()
        for food in self.food:
            if food.destroyed:
                self.food.remove(food)
            else:
                food.update()

    def draw(self):
        for food in self.food:
            food.draw(self.surface)

    def food_spawner(self):
        while len(self.food) < initial_food_on_screen:
            self.spawn_food()

    def spawn_food(self):
        self.food.append(Food(self.width, self.height))
