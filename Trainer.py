import numpy as np
import random
from collections import deque
import tensorflow as tf
import os
from tensorflow import keras
from game_logic import Game, Player
from q_learning_agent import DQNAgent
from config import (EPISODES, BATCH_SIZE, STATE_SIZE, ACTION_SIZE, REWARD_FOR_DRAW,
                    BASE_RATS_REWARD, PENALTY_FOR_EARLY_RATS, MIN_TURN_FOR_RATS,
                    REWARD_DECAY_RATE, PENALTY_FOR_HIGH_SCORE_RATS,
                    LEARNING_RATE, DISCOUNT_FACTOR, EXPLORATION_RATE,
                    EXPLORATION_DECAY, MIN_EXPLORATION_RATE)

# Check if the weight file exists and delete it
if os.path.exists("dqn_weights_player1.weights.h5"):
    os.remove("dqn_weights_player1.weights.h5")
if os.path.exists("dqn_weights_player2.weights.h5"):
    os.remove("dqn_weights_player2.weights.h5")
def train_dqn():
    player1 = Player("AI_Player1")
    player2 = Player("AI_Player2")
    game = Game(player1, player2)

    # Initialize agents with parameters from config.py
    agent1 = DQNAgent(state_size=STATE_SIZE, action_size=ACTION_SIZE, learning_rate=LEARNING_RATE, 
                      discount_factor=DISCOUNT_FACTOR, exploration_rate=EXPLORATION_RATE, 
                      exploration_decay=EXPLORATION_DECAY, min_exploration_rate=MIN_EXPLORATION_RATE)
    agent2 = DQNAgent(state_size=STATE_SIZE, action_size=ACTION_SIZE, learning_rate=LEARNING_RATE, 
                      discount_factor=DISCOUNT_FACTOR, exploration_rate=EXPLORATION_RATE, 
                      exploration_decay=EXPLORATION_DECAY, min_exploration_rate=MIN_EXPLORATION_RATE)

    # Metrics to track
    victories_player1 = 0
    victories_player2 = 0
    total_ties = 0
    total_game_lengths = []

    for episode in range(EPISODES):
        game.reset_game()
        state1 = np.reshape(game.get_state(player1), [1, STATE_SIZE])
        state2 = np.reshape(game.get_state(player2), [1, STATE_SIZE])
        done = False
        game_length = 0

        while not game.game_over:
            # Player 1 (Agent 1) takes an action
            action1 = agent1.choose_action(state1)
            action_str1 = 'draw' if action1 == 0 else 'call_rats'
            next_state1, reward1, done = game.perform_action(player1, action_str1)
            next_state1 = np.reshape(next_state1, [1, STATE_SIZE])
            agent1.remember(state1, action1, reward1, next_state1, done)
            state1 = next_state1

            # Player 2 (Agent 2) takes a turn if game isn't over
            if not done:
                action2 = agent2.choose_action(state2)
                action_str2 = 'draw' if action2 == 0 else 'call_rats'
                next_state2, reward2, done = game.perform_action(player2, action_str2)
                next_state2 = np.reshape(next_state2, [1, STATE_SIZE])
                agent2.remember(state2, action2, reward2, next_state2, done)
                state2 = next_state2

            game_length += 1

            if done:
                points_player1 = player1.get_total_score()
                points_player2 = player2.get_total_score()

                # Track victories and ties
                if points_player1 < points_player2:
                    victories_player1 += 1
                elif points_player2 < points_player1:
                    victories_player2 += 1
                else:
                    total_ties += 1

                total_game_lengths.append(game_length)
                print(f"Episode {episode+1}/{EPISODES} - Player 1 Points: {points_player1}, Player 2 Points: {points_player2}, Game Length: {game_length}")

            # Train both agents
            agent1.train_from_replay(batch_size=BATCH_SIZE)
            agent2.train_from_replay(batch_size=BATCH_SIZE)

    # Summary with average game length
    avg_game_length = np.mean(total_game_lengths)
    print("\nTraining Summary:")
    print(f"Player 1 Victory Percentage: {(victories_player1 / EPISODES) * 100:.2f}%")
    print(f"Player 2 Victory Percentage: {(victories_player2 / EPISODES) * 100:.2f}%")
    print(f"Tie Percentage: {(total_ties / EPISODES) * 100:.2f}%")
    print(f"Average Game Length: {avg_game_length:.2f} turns")

    # Save both agents' weights
    agent1.save("dqn_weights_player1.weights.h5")
    agent2.save("dqn_weights_player2.weights.h5")

if __name__ == "__main__":
    train_dqn()
