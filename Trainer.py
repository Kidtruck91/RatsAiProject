import numpy as np
from game_logic import Game, Player
from q_learning_agent import DQNAgent
from config import *


def train_dqn():
    player1 = Player("AI_Player1")
    player2 = Player("AI_Player2")
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
            action1 = agent1.choose_action(state1)
            _, reward1, _ = game.perform_action(player1, ['draw', 'call_rats', 'peek_opponent', 'peek_self', 'swap_with_queen'][action1])
            state1 = game.get_state(player1)
            agent1.remember(state1, action1, reward1, game.get_state(player1), game.game_over)
            if action1 == 1: metrics["rats_calls_player1"] += 1

            if game.game_over:
                break

            # AI2's turn
            action2 = agent2.choose_action(state2)
            _, reward2, _ = game.perform_action(player2, ['draw', 'call_rats', 'peek_opponent', 'peek_self', 'swap_with_queen'][action2])
            state2 = game.get_state(player2)
            agent2.remember(state2, action2, reward2, game.get_state(player2), game.game_over)
            if action2 == 1: metrics["rats_calls_player2"] += 1

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
    print(metrics)

if __name__ == "__main__":
    train_dqn()
