import sys
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

sys.path.append("..")
from game.snake_game import Game


if __name__ == '__main__':
    game = Game()
    
    # game loop
    while True:
        game.update_frame()
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
        
    pygame.quit()

