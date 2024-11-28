import numpy as np
from game_logic import Game, Player
from q_learning_agent import DQNAgent
from config import *
import json

def preprocess_metrics(data):
    """
    Recursively convert all non-JSON-serializable objects in the metrics dictionary.
    Specifically converts numpy arrays to lists.
    """
    if isinstance(data, dict):
        return {key: preprocess_metrics(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [preprocess_metrics(item) for item in data]
    elif isinstance(data, np.ndarray):
        return data.tolist()  # Convert numpy arrays to lists
    elif isinstance(data, tuple):
        return tuple(preprocess_metrics(item) for item in data)
    else:
        return data

def train_dqn():
    player1 = Player("AI_Player1", is_human=False)
    player2 = Player("AI_Player2", is_human=False)
    game = Game(player1, player2)

    agent1 = DQNAgent(
        STATE_SIZE,
        ACTION_SIZE,
        LEARNING_RATE,
        DISCOUNT_FACTOR,
        EXPLORATION_RATE,
        EXPLORATION_DECAY,
        MIN_EXPLORATION_RATE
    )
    agent2 = DQNAgent(
        STATE_SIZE,
        ACTION_SIZE,
        LEARNING_RATE,
        DISCOUNT_FACTOR,
        EXPLORATION_RATE,
        EXPLORATION_DECAY,
        MIN_EXPLORATION_RATE
    )

    metrics = {
        "victories_player1": 0,
        "victories_player2": 0,
        "total_ties": 0,
        "total_game_lengths": [],
        "rats_calls_player1": 0,
        "rats_calls_player2": 0,
        "average_score_player1": [],
        "average_score_player2": [],
        "game_logs": []  # Add this to store logs for each game
    }

    for episode in range(EPISODES):
        print(f"Starting Episode {episode + 1}/{EPISODES}")
        game.reset_game()
        state1 = game.get_state(player1)
        state2 = game.get_state(player2)
        game_length = 0
        game_log = []  # Log for the current game

        while not game.game_over:
            # AI1's turn
            valid_actions1 = game.get_available_actions()
            action1 = agent1.choose_action(state1, valid_actions1)
            action1_name = valid_actions1[action1]
            reward1 = game.perform_action(player1, action1_name, agent1)
            next_state1 = game.get_state(player1)
            agent1.remember(state1, action1, reward1, next_state1, game.game_over)
            state1 = next_state1
            game_log.append({
                "player": "AI_Player1",
                "action": action1_name,
                "state": state1.tolist(),
                "valid_actions": valid_actions1,
                "reward": reward1,
                "turn": game_length,
                "scores": [p.get_total_score() for p in game.players]
            })
            if action1_name == "call_rats":
                metrics["rats_calls_player1"] += 1

            if game.game_over:
                break

            # AI2's turn
            valid_actions2 = game.get_available_actions()
            action2 = agent2.choose_action(state2, valid_actions2)
            action2_name = valid_actions2[action2]
            reward2 = game.perform_action(player2, action2_name, agent2)
            next_state2 = game.get_state(player2)
            agent2.remember(state2, action2, reward2, next_state2, game.game_over)
            state2 = next_state2
            game_log.append({
                "player": "AI_Player2",
                "action": action2_name,
                "state": state2.tolist(),
                "valid_actions": valid_actions2,
                "reward": reward2,
                "turn": game_length,
                "scores": [p.get_total_score() for p in game.players]
            })
            if action2_name == "call_rats":
                metrics["rats_calls_player2"] += 1

            game_length += 1

        # Metrics tracking
        points_player1 = player1.get_total_score()
        points_player2 = player2.get_total_score()
        metrics["average_score_player1"].append(points_player1)
        metrics["average_score_player2"].append(points_player2)
        metrics["total_game_lengths"].append(game_length)

        if points_player1 < points_player2:
            metrics["victories_player1"] += 1
        elif points_player2 < points_player1:
            metrics["victories_player2"] += 1
        else:
            metrics["total_ties"] += 1

        metrics["game_logs"].append(game_log)  # Save the current game log

    # Save results and weights
    agent1.save("./weights/dqn_weights_player1.weights.h5")
    agent2.save("./weights/dqn_weights_player2.weights.h5")
    print("Training Complete!")
    print("Metrics:", metrics)
    return metrics
    


if __name__ == "__main__":
    metrics=train_dqn()
    processed_metrics = preprocess_metrics(metrics)

    with open("training_metrics.json", "w") as metrics_file:
        json.dump(processed_metrics, metrics_file, indent=4)

    print("Metrics and game logs saved.")