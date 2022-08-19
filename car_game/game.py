import pygame


class CarGame:
    def __init__(self, width, height, frame_rate, cars, surface):
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.game_over = False
        self.cars = cars

        self.surface = surface
        self.clock = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption('Car Game')
        pygame.font.init()

    def run(self):
        while not self.game_over:
            self.surface.fill((0, 0, 0))

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)

    def update_cars(self):
        for car in self.cars:
            if car.destroyed:
                self.cars.remove(car)
            else:
                car.update()

    def update(self):
        self.update_cars()
        if len(self.cars) <= 0:
            self.game_over = True

    def draw(self):
        for car in self.cars:
            car.draw(self.surface)
