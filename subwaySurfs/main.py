import os

import pygame

from subwaySurfs.game import Game

game_width = 600
game_height = 800
frame_rate = 60


def game():
    surface = pygame.display.set_mode((game_width, game_height))
    g = Game(game_width, game_height, frame_rate, surface)
    g.run()


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'n_config.txt')

    game()
