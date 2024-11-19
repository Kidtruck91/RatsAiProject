# Game and Training Parameters
EPISODES = 1000             # Total number of training episodes
BATCH_SIZE = 32             # Batch size for training from memory replay
STATE_SIZE = 21             # The size of the state representation (update as necessary)
ACTION_SIZE = 5             # Number of actions the agent can take

# Reward and Penalty Parameters
REWARD_FOR_DRAW = 1               # Reward for drawing to prolong the game
BASE_RATS_REWARD = 20             # Base reward for calling "Rats" with a lower score
PENALTY_FOR_EARLY_RATS = -15       # Penalty for calling "Rats" early
MIN_TURN_FOR_RATS = 5             # Minimum turns before "Rats" is called without penalty
REWARD_DECAY_RATE = 0.9           # Decay rate for "Rats" reward based on game length
PENALTY_FOR_HIGH_SCORE_RATS = -10 # Penalty for calling "Rats" with a high score

# DQN Agent Parameters
LEARNING_RATE = 0.001             # Learning rate for the agent's neural network
DISCOUNT_FACTOR = 0.95            # Discount factor for future rewards
EXPLORATION_RATE = 1.0            # Initial exploration rate (epsilon) for exploration/exploitation
EXPLORATION_DECAY = 0.995         # Decay rate for exploration
MIN_EXPLORATION_RATE = 0.01       # Minimum exploration rate