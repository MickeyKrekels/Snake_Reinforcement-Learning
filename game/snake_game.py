import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    EAST = 1
    WEST = 2
    NORTH = 3
    SOUTH = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
BACKGROUND = (77, 31, 0)
FOOD = (240, 105, 35)
SNAKE_COLOR_1 = (155, 50, 175)
SNAKE_COLOR_2 = (187, 186, 176)

BLOCK_SIZE = 20
SPEED = 15

REWARD_REWARD_POINTS = 15
REWARD_ERROR_POINTS = -15


MAX_FRAMES = 100

class Game:
    
    def __init__(self, w=1280, h=720):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset_game()
        
    def reset_game(self):
        self.direction = Direction.EAST
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y),Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]  
        self.score = 0
        self.food = None
        self._place_food()
        self.frame = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def update_frame(self):
        self.frame += 1

    def agent_step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.K_ESCAPE:
                pygame.quit()
                quit()
        
        # 2. move
        derection_array = [Direction.EAST, Direction.WEST, Direction.NORTH, Direction.SOUTH]
        index = derection_array.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            action = derection_array[index] # do nothing
        elif np.array_equal(action, [0, 1, 0]):
            index = (index + 1) % 4
            action = derection_array[index] # right turn
        else:
            index = (index - 1) % 4
            action = derection_array[index] # left turn

        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self._is_collision() or self.frame > MAX_FRAMES:
            print("Game over")
            game_over = True
            reward = REWARD_ERROR_POINTS
            return reward, game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = REWARD_REWARD_POINTS
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward , game_over, self.score
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.WEST
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.EAST
                elif event.key == pygame.K_UP:
                    self.direction = Direction.NORTH
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.SOUTH
    
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            print("Game over")
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self,point=None):
        if point is None:
            point = self.head
        # hits boundary
        if point.x > self.w - BLOCK_SIZE or point.x < 0 or point.y > self.h - BLOCK_SIZE or point.y < 0:
            return True
        # hits itself
        if point in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BACKGROUND)
        
        drawnhead = False
        for pt in self.snake:

            if not drawnhead:
                pygame.draw.rect(self.display, SNAKE_COLOR_2, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, SNAKE_COLOR_1, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

                drawnhead = True
                continue
               
            pygame.draw.rect(self.display, SNAKE_COLOR_1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, SNAKE_COLOR_2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, FOOD, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("| Frames: " + str(self.frame), True, WHITE)
        self.display.blit(text, [100, 0])
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):       
        x = self.head.x
        y = self.head.y
        if direction == Direction.EAST:
            x += BLOCK_SIZE
        elif direction == Direction.WEST:
            x -= BLOCK_SIZE
        elif direction == Direction.SOUTH:
            y += BLOCK_SIZE
        elif direction == Direction.NORTH:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

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