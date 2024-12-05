# Game and Training Parameters
EPISODES = 10000             # Total number of training episodes
BATCH_SIZE = 32            # Batch size for training from memory replay

# Reward and Penalty Parameters
REWARD_FOR_DRAW = 5
BASE_RATS_REWARD = 3
PENALTY_FOR_EARLY_RATS = -10
MIN_TURN_FOR_RATS = 8
REWARD_DECAY_RATE = 0.8
PENALTY_FOR_HIGH_SCORE_RATS = -1
REWARD_FOR_DISCOVERY = 5
REWARD_FOR_DISCOVERY_OPPONENT = 5
LEAD_THRESHOLD = 10
SIGNIFICANT_LEAD_BONUS = 3
PENALTY_FOR_CALL_WHILE_BEHIND = -6

# DQN Agent Parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.99
EXPLORATION_RATE = 1.0
EXPLORATION_DECAY = 0.99
MIN_EXPLORATION_RATE = 0.05

# STATE_SIZE and ACTION_SIZE are dynamically added by dynamic_config.py

STATE_SIZE = 21
ACTION_SIZE = 2
