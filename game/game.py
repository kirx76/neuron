import pygame


class NeatGame:
    def __init__(self, width, height, frame_rate, paddles):
        self.frame_rate = frame_rate
        self.width = width
        self.height = height
        self.paddles = paddles

        self.game_over = False
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        pygame.init()
        pygame.display.set_caption('Neat Game')
        pygame.font.init()

    def run(self):
        while not self.game_over:
            self.surface.fill((0, 0, 0))

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)

    def update(self):
        for p in self.paddles:
            if p.destroyed:
                self.paddles.remove(p)
            else:
                p.update()
        if len(self.paddles) <= 0:
            self.game_over = True

    def draw(self):
        for p in self.paddles:
            p.draw(self.surface)