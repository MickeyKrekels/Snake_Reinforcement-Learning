import sys
import pygame

sys.path.append("..")
from game.snake_game import Game, Direction
from agent import Agent



def train(model = ''):
    total_score = 0
    record = 0
    agent = Agent(model)
    game = Game()

    while True:
        # get old state
        game.frame += 1
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.agent_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset_game()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save(str(score))

            total_score += score
            mean_score = total_score / agent.n_games
            print('Game', agent.n_games, 'Score', score , 'Record:', record, 'Mean Score:', mean_score)

def play():
    game = Game()
    # game loop
    while True:
        game.update_frame()
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)     
    pygame.quit()


if __name__ == '__main__':
    train('./best_model/20-10-2022_14-53-45_score-52_model.pth')
    # play()



