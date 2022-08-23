import pygame

player_height = 50
max_trains_in_a_row = 2
train_spawn_timeout = (200 + player_height + 30) / 2


class Game:
    def __init__(self, width, height, frame_rate, surface, players):
        self.frame_rate = frame_rate
        self.width = width
        self.height = height
        self.game_over = False
        self.surface = surface
        self.clock = pygame.time.Clock()

        self.players = players

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
        # if self.game_over:
        #     pygame.quit()
        # sys.exit()

    def update_players(self):
        for player in self.players:
            if player.destroyed:
                self.players.remove(player)
            else:
                player.update()

    def destroy(self):
        self.game_over = True

    def draw_players(self):
        for player in self.players:
            player.draw(self.surface)

    def update(self):
        self.update_players()
        if len(self.players) <= 0:
            self.game_over = True

    def draw(self):
        self.draw_players()
