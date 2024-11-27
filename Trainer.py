import numpy as np
from game_logic import Game, Player
from q_learning_agent import DQNAgent
from config import *

def train_dqn():
    player1 = Player("AI_Player1", is_human=False)
    player2 = Player("AI_Player2", is_human=False)
    game = Game(player1, player2)

    agent1 = DQNAgent(STATE_SIZE, ACTION_SIZE, LEARNING_RATE, DISCOUNT_FACTOR, EXPLORATION_RATE, EXPLORATION_DECAY, MIN_EXPLORATION_RATE)
    agent2 = DQNAgent(STATE_SIZE, ACTION_SIZE, LEARNING_RATE, DISCOUNT_FACTOR, EXPLORATION_RATE, EXPLORATION_DECAY, MIN_EXPLORATION_RATE)

    metrics = {
        "victories_player1": 0,
        "victories_player2": 0,
        "total_ties": 0,
        "total_game_lengths": [],
        "rats_calls_player1": 0,
        "rats_calls_player2": 0
    }

    for episode in range(EPISODES):
        game.reset_game()
        state1 = game.get_state(player1)
        state2 = game.get_state(player2)
        game_length = 0

        while not game.game_over:
            # AI1's turn
            valid_actions1 = game.get_available_actions()  # Get valid actions for Player 1
            action1 = agent1.choose_action(state1, valid_actions1)
            action1_name = valid_actions1[action1]  # Get the corresponding action name
            reward1 = game.perform_action(player1, action1_name, agent1)  # Pass agent1 to perform_action
            next_state1 = game.get_state(player1)
            agent1.remember(state1, action1, reward1, next_state1, game.game_over)
            state1 = next_state1
            if action1_name == "call_rats": 
                metrics["rats_calls_player1"] += 1

            if game.game_over:
                break

            # AI2's turn
            valid_actions2 = game.get_available_actions()  # Get valid actions for Player 2
            action2 = agent2.choose_action(state2, valid_actions2)
            action2_name = valid_actions2[action2]  # Get the corresponding action name
            reward2 = game.perform_action(player2, action2_name, agent2)  # Pass agent2 to perform_action
            next_state2 = game.get_state(player2)
            agent2.remember(state2, action2, reward2, next_state2, game.game_over)
            state2 = next_state2
            if action2_name == "call_rats": 
                metrics["rats_calls_player2"] += 1

            game_length += 1

        # Metrics tracking
        points_player1 = player1.get_total_score()
        points_player2 = player2.get_total_score()
        metrics["total_game_lengths"].append(game_length)
        if points_player1 < points_player2:
            metrics["victories_player1"] += 1
        elif points_player2 < points_player1:
            metrics["victories_player2"] += 1
        else:
            metrics["total_ties"] += 1

    # Save results and weights
    agent1.save("./weights/dqn_weights_player1.weights.h5")
    agent2.save("./weights/dqn_weights_player2.weights.h5")
    print("Training Complete!")
    print("Metrics:", metrics)

if __name__ == "__main__":
    train_dqn()
