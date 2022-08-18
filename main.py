import os
import random

import neat

from game.config import initial_balls_on_screen, width, height, frame_rate
from game.game import NeatGame
from game.paddle import NeatPaddle


def get_random_color():
    return (random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))


def eval_genomes(genomes, config):
    paddles = []
    current_id = 1
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        paddle = NeatPaddle(10, get_random_color(), 30, initial_balls_on_screen, width, height, net, genome, current_id)
        paddles.append(paddle)
        current_id += 1

    while len(paddles) > 0:
        game = NeatGame(width, height, frame_rate, paddles)
        game.run()


def main(config_file):
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
    main(config_path)
