import numpy as np
from game_logic import Game, Player
from q_learning_agent import DQNAgent
from config import *
import json


def train_dqn():
    player1 = Player("AI_Player1", is_human=False)
    player2 = Player("AI_Player2", is_human=False)
    game = Game(player1, player2)

    agent1 = DQNAgent(
        STATE_SIZE, ACTION_SIZE, LEARNING_RATE, DISCOUNT_FACTOR,
        EXPLORATION_RATE, EXPLORATION_DECAY, MIN_EXPLORATION_RATE
    )
    agent2 = DQNAgent(
        STATE_SIZE, ACTION_SIZE, LEARNING_RATE, DISCOUNT_FACTOR,
        EXPLORATION_RATE, EXPLORATION_DECAY, MIN_EXPLORATION_RATE
    )

    metrics = {
        "victories_player1": 0,
        "victories_player2": 0,
        "total_ties": 0,
        "average_game_length": [],
        "turn_counters": [],  # Track turn counts for each game
        "rats_calls_player1": 0,
        "rats_calls_player2": 0,
        "peeks_player1": 0,
        "peeks_player2": 0,
        "swaps_player1": 0,
        "swaps_player2": 0,
        "average_score_player1": [],
        "average_score_player2": [],
    }

    for episode in range(EPISODES):
        game.reset_game()
        state1 = game.get_state(player1)
        state2 = game.get_state(player2)
        game_length = 0

        while not game.game_over:
            # AI1's turn
            valid_actions1 = game.get_available_actions()
            action1 = agent1.choose_action(state1, valid_actions1)
            action1_name = valid_actions1[action1]
            reward1, state_log1 = process_action(game, player1, action1_name, agent1)

            # Update metrics based on executed action
            executed_action1 = state_log1["action"]
            print(f"AI_Player1 executed action: {executed_action1}")
            if executed_action1 == "call_rats":
                metrics["rats_calls_player1"] += 1
            elif executed_action1 in ["peek"]:
                metrics["peeks_player1"] += 1
            elif executed_action1 == "swap":
                metrics["swaps_player1"] += 1

            if game.game_over:
                break

            # AI2's turn
            valid_actions2 = game.get_available_actions()
            action2 = agent2.choose_action(state2, valid_actions2)
            action2_name = valid_actions2[action2]
            reward2, state_log2 = process_action(game, player2, action2_name, agent2)

            # Update metrics based on executed action
            executed_action2 = state_log2["action"]
            print(f"AI_Player2 executed action: {executed_action2}")
            if executed_action2 == "call_rats":
                metrics["rats_calls_player2"] += 1
            elif executed_action2 in ["peek_self", "peek_opponent"]:
                metrics["peeks_player2"] += 1
            elif executed_action2 == "swap_with_queen":
                metrics["swaps_player2"] += 1

            game_length += 1

        # Log the turn counter
        metrics["turn_counters"].append(game.turn_counter)

        # Metrics tracking
        points_player1 = player1.get_total_score()
        points_player2 = player2.get_total_score()
        metrics["average_score_player1"].append(points_player1)
        metrics["average_score_player2"].append(points_player2)
        metrics["average_game_length"].append(game_length)

        if points_player1 > points_player2:
            metrics["victories_player1"] += 1
        elif points_player2 > points_player1:
            metrics["victories_player2"] += 1
        else:
            metrics["total_ties"] += 1

    # Finalize metrics with averages
    summarized_metrics = {
        "victories_player1": metrics["victories_player1"],
        "victories_player2": metrics["victories_player2"],
        "total_ties": metrics["total_ties"],
        "average_game_length": np.mean(metrics["average_game_length"]),
        "average_turns": np.mean(metrics["turn_counters"]),
        "rats_calls_player1": metrics["rats_calls_player1"],
        "rats_calls_player2": metrics["rats_calls_player2"],
        "peeks_player1": metrics["peeks_player1"],
        "peeks_player2": metrics["peeks_player2"],
        "swaps_player1": metrics["swaps_player1"],
        "swaps_player2": metrics["swaps_player2"],
        "average_score_player1": np.mean(metrics["average_score_player1"]),
        "average_score_player2": np.mean(metrics["average_score_player2"]),
    }

    # Save results and weights
    agent1.save("./weights/dqn_weights_player1.weights.h5")
    agent2.save("./weights/dqn_weights_player2.weights.h5")
    print("Training Complete!")
    print("Metrics:", summarized_metrics)
    with open("training_metrics.json", "w") as f:
        json.dump(summarized_metrics, f, indent=4)
    print("Metrics saved to training_metrics.json")


def process_action(game, player, action_name, agent):
    """
    Perform an action, log state information, and return the reward and state log.
    """
    state_before, reward, next_state, executed_action = game.perform_action(player, action_name, agent)
    print(f"process_action: {player.name} executed {executed_action}") 
    state_log = {
        "player": player.name,
        "action": executed_action,  # Use the executed action for logging
        "state": state_before.tolist(),
        "valid_actions": game.get_available_actions(),
        "reward": reward,
        "turn": game.turn_counter,
        "scores": [p.get_total_score() for p in game.players]
    }
    return reward, state_log

if __name__ == "__main__":
    train_dqn()
