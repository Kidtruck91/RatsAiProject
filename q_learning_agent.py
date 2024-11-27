import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow import keras

# Swap action mappings
SWAP_ACTIONS = {
    "give_0": 0,  # Give card at index 0
    "give_1": 1,  # Give card at index 1
    "give_2": 2,  # Give card at index 2
    "take_0": 3,  # Take card at index 0
    "take_1": 4,  # Take card at index 1
    "take_2": 5,  # Take card at index 2
}
class DQNAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001, discount_factor=0.95, exploration_rate=1.0, exploration_decay=0.995, min_exploration_rate=0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.min_exploration_rate = min_exploration_rate
        self.exploration_decay = exploration_decay
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.update_target_network()

    def build_model(self):
        model = keras.Sequential([
            keras.layers.Dense(24, input_dim=self.state_size, activation='relu'),
            keras.layers.Dense(24, activation='relu'),
            keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate), loss='mse')
        return model

    def update_target_network(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def choose_action(self, state, valid_actions):
        """
        Select an action based on Q-values, constrained to valid actions.
        """
        if np.random.rand() <= self.exploration_rate:
            # Choose a random action from valid actions
            return random.choice(range(len(valid_actions)))
    
        state = np.reshape(state, [1, self.state_size])
        q_values = self.model.predict(state)[0]

        # Filter Q-values to only consider valid actions
        valid_q_values = [q_values[action] for action in range(len(q_values)) if action in valid_actions]

        # Map back to original index for the valid actions
        valid_action_indices = [action for action in range(len(q_values)) if action in valid_actions]

        return valid_action_indices[np.argmax(valid_q_values)]


    def train_from_replay(self, batch_size=32):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                next_state = np.reshape(next_state, [1, self.state_size])
                target = reward + self.discount_factor * np.amax(self.target_model.predict(next_state)[0])
            state = np.reshape(state, [1, self.state_size])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.exploration_rate > self.min_exploration_rate:
            self.exploration_rate *= self.exploration_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)
