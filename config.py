# Game and Training Parameters
EPISODES = 10000             # Total number of training episodes
BATCH_SIZE = 32            # Batch size for training from memory replay

# Reward and Penalty Parameters
REWARD_FOR_DRAW = 25
BASE_RATS_REWARD = 20
PENALTY_FOR_EARLY_RATS = -45
MIN_TURN_FOR_RATS = 5
REWARD_DECAY_RATE = 0.9
PENALTY_FOR_HIGH_SCORE_RATS = -10
REWARD_FOR_DISCOVERY = 5
REWARD_FOR_DISCOVERY_OPPONENT = 5
LEAD_THRESHOLD=5
SIGNIFICANT_LEAD_BONUS=5
PENALTY_FOR_CALL_WHILE_BEHIND = -20

# DQN Agent Parameters
LEARNING_RATE = 0.001
DISCOUNT_FACTOR = 0.95
EXPLORATION_RATE = 1.0
EXPLORATION_DECAY = 0.5
MIN_EXPLORATION_RATE = 0.01

# STATE_SIZE and ACTION_SIZE are dynamically added by dynamic_config.py

STATE_SIZE = 21
ACTION_SIZE = 2
