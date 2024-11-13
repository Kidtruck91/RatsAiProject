import random
import numpy as np

class QLearningAgent:
    def __init__(self, environment, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0, min_exploration_rate=0.01, exploration_decay=0.995):
        self.env = environment
        self.q_table = {}  # Initialize Q-table as a dictionary
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.min_exploration_rate = min_exploration_rate
        self.exploration_decay = exploration_decay
        self.actions = ['draw', 'call_rats']  # Define possible actions

    def choose_action(self, state):
        # Epsilon-greedy choice
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)
        else:
            return max(self.q_table.get(state, {}), key=self.q_table.get(state, {}).get, default=random.choice(self.actions))

    def update_q_value(self, state, action, reward, next_state):
        old_q_value = self.q_table.get(state, {}).get(action, 0)
        future_reward = max(self.q_table.get(next_state, {}).values(), default=0)
        new_q_value = old_q_value + self.learning_rate * (reward + self.discount_factor * future_reward - old_q_value)
        
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_q_value

    def train(self, episodes=1000):
        for episode in range(episodes):
            state = self.env.get_state(self.env.players[0])  # Assuming player 0 is AI
            done = False

            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.perform_action(self.env.players[0], action)
                self.update_q_value(state, action, reward, next_state)
                state = next_state

            # Decay exploration rate
            self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)