# RatsAiProject
Project Structure
1. config.py
Purpose: Holds all configurable parameters that influence agent behavior, rewards, penalties, and training settings. By adjusting values here, you can influence the agent's strategies and outcomes without modifying other files.

Key Parameters:

EPISODES: Total number of training episodes.
BATCH_SIZE: The size of memory replay batches.
STATE_SIZE and ACTION_SIZE: Define the state and action space for the DQN agent.
Reward and Penalty Parameters:
REWARD_FOR_DRAW: Reward for drawing a card to extend the game.
BASE_RATS_REWARD: Base reward for calling "Rats" when likely to win.
PENALTY_FOR_EARLY_RATS: Penalty for calling "Rats" too early.
MIN_TURN_FOR_RATS: Minimum number of turns before calling "Rats" without penalty.
REWARD_DECAY_RATE: Decay rate for rewards when calling "Rats" based on game length.
PENALTY_FOR_HIGH_SCORE_RATS: Penalty for calling "Rats" with a high score.
DQN Agent Parameters:
LEARNING_RATE: Learning rate for the DQN model.
DISCOUNT_FACTOR: Discount factor for future rewards.
EXPLORATION_RATE, EXPLORATION_DECAY, MIN_EXPLORATION_RATE: Parameters for balancing exploration and exploitation.

2. game_logic.py
Purpose: Contains the logic for the Rats game, managing game state, actions, rewards, and penalties for player moves. This file orchestrates each player's turn and handles specific actions like drawing and calling "Rats."

Key Classes and Functions:

Game: The main class that manages game state, actions, and rewards.

__init__(self, player1, player2): Initializes the game with two players.
deal_initial_cards(self): Deals initial cards to each player.
reset_game(self): Resets the game for a new round.
get_state(self, player): Returns the current state for a player, including visible cards and discard counts.
perform_action(self, player, action): Executes an action (draw, call_rats, etc.) and returns the updated game state, reward, and game-over status.
call_rats(self): Ends the game when a player calls "Rats" and calculates the final score.
Player: Represents each player in the game, tracking known cards, scores, and actions.

get_visible_cards(self): Returns the cards visible to the player.
get_total_score(self): Calculates the total score of the player's hand.

3. q_learning_agent.py
Purpose: Defines the DQNAgent class, which represents the Deep Q-Learning agent. This file handles the neural network structure, memory replay, and exploration/exploitation strategy.

Key Functions and Methods:

DQNAgent: Defines the DQN agent and its training strategy.
__init__(self, state_size, action_size, ...): Initializes agent parameters such as learning rate, discount factor, and exploration decay.
build_model(self): Builds the neural network model for Q-learning, consisting of two hidden layers.
choose_action(self, state): Selects an action based on the current exploration rate or Q-values.
train_from_replay(self, batch_size=32): Trains the model from past experiences stored in memory.
update_target_network(self): Updates the target network with the current model weights.
remember(self, state, action, reward, next_state, done): Stores experiences for replay.
save(self, name) and load(self, name): Save and load model weights for persistence.

4. Trainer.py
Purpose: Orchestrates the training loop, initializes agents, and manages metrics for performance analysis. This script uses parameters from config.py to control training dynamics and save results.

Key Functions and Main Workflow:

train_dqn(episodes=1000): Main function that runs the training loop for a specified number of episodes.
Initializes two Player instances and the Game.
Creates two DQNAgent instances (agent1 for Player 1 and agent2 for Player 2) with parameters from config.py.
Executes each player's actions in alternating turns until the game is over.
Records victories, ties, and game length for each episode.
Trains each agent on past experiences using experience replay.
Prints summary metrics at the end of training, including victory percentages and average game length.
Saves both agents’ weights after training for future use.
