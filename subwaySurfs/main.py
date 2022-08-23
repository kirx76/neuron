import os
import random

import neat
import pygame

from subwaySurfs.game import Game
from subwaySurfs.player import Player

game_width = 600
game_height = 800
frame_rate = 60


def get_random_color():
    return (random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))


def eval_genomes(genomes, config):
    surface = pygame.display.set_mode((game_width, game_height))
    players = []
    current_id = 1
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        player = Player(surface, game_width, game_height, net, genome, current_id, get_random_color())
        players.append(player)
        current_id += 1

    while len(players) > 0:
        g = Game(game_width, game_height, frame_rate, surface, players)
        g.run()


def game(config_file):
    n_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  config_file)

    p = neat.Population(n_config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 250)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'n_config.txt')

    game(config_path)
