import random
import numpy as np
from collections import Counter
from config import REWARD_FOR_DRAW, BASE_RATS_REWARD, PENALTY_FOR_EARLY_RATS, MIN_TURN_FOR_RATS, REWARD_DECAY_RATE, PENALTY_FOR_HIGH_SCORE_RATS
class Deck:
    def __init__(self):
        self.cards = self.create_deck()
        random.shuffle(self.cards)

    def create_deck(self):
        # Create a standard 52-card deck with Kings (K), Jacks (J), and Queens (Q)
        deck = []
        for value in range(1, 14):  # 1 to 13
            if value == 11:  # Jack
                card_value = 'J'
            elif value == 12:  # Queen
                card_value = 'Q'
            elif value == 13:  # King
                card_value = 'K'
            else:
                card_value = value
            deck.extend([card_value] * 4)  # 4 of each value (one per suit)
        return deck

    def draw(self):
        return self.cards.pop() if self.cards else None

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = [None, None, None]  # The player's three cards
        self.revealed_cards = [None, None, None]  # Known values for the player
        self.known_opponent_cards = set()  # Tracks specific opponent cards the player has seen

    def set_initial_cards(self, card1, card2, card3):
        self.cards = [card1, card2, card3]
        self.revealed_cards[0] = card1  # Initially reveal first card
        self.revealed_cards[1] = card2  # Initially reveal second card
        self.revealed_cards[2] = "?"  # Third card is hidden

    def replace_card(self, index, new_card):
        old_card = self.cards[index]
        self.cards[index] = new_card
        self.revealed_cards[index] = new_card  # Update visibility
        return old_card  # Discarded card

    def get_visible_cards(self):
        return [self.revealed_cards[i] if self.revealed_cards[i] is not None else "?" for i in range(3)]

    def get_total_score(self):
        total = 0
        for card in self.cards:
            if card == 'K':  # Kings are worth 0
                total += 0
            elif card in ['J', 'Q']:  # Jacks and Queens are worth 11
                total += 11
            else:
                total += card
        return total

    def knows_opponent_card(self, card):
        """Check if the player knows a specific opponent card."""
        return card in self.known_opponent_cards

    def add_known_opponent_card(self, card):
        """Mark a specific opponent card as known (e.g., after peeking with Jack)."""
        self.known_opponent_cards.add(card)

class Game:
    def __init__(self, player1, player2):
        self.deck = Deck()
        self.discard_pile = []  # Tracks all discarded cards
        self.players = [player1, player2]
        self.turn = 0
        self.rats_called = False
        self.game_over = False
        self.deal_initial_cards()

    def handle_card_replacement(self, player, index, drawn_card):
        """Replace a card in the player's hand and add the old card to the discard pile."""
        discarded = player.replace_card(index, drawn_card)
        self.discard_pile.append(discarded)

    def deal_initial_cards(self):
        for player in self.players:
            player.set_initial_cards(self.deck.draw(), self.deck.draw(), self.deck.draw())

    def reset_game(self):
        """Resets the game for a new round (used in training)."""
        self.deck = Deck()
        self.discard_pile = []
        self.turn = 0
        self.rats_called = False
        self.game_over = False
        self.deal_initial_cards()

    def get_state(self, player):
        """Returns a state representation with the player's own known cards, partial knowledge of opponent's hand, and discard information."""
        state = []

        # Player's own cards
        for card in player.get_visible_cards():
            if card == "K":
                state.append(0)  # King as 0
            elif card == "J" or card == "Q":
                state.append(11)  # Jack and Queen as 11
            elif card == "?":
                state.append(-1)  # Hidden card as -1
            else:
                state.append(card)  # Numeric card values (1-10)

        # Placeholder for opponent’s cards
        opponent = self.players[1 - self.turn]
        for card in opponent.get_visible_cards():
            if card == "?":
                state.append(-1)
            else:
                state.append(card if player.knows_opponent_card(card) else -1)

        # Additional information: player's current score and remaining deck count
        state.append(player.get_total_score())  # Player's current score estimate
        state.append(len(self.deck.cards))      # Remaining cards in the deck

        # Discard pile summary
        discard_counts = self.get_discard_counts()
        state.extend(discard_counts)  # Append discard counts to state

        return np.array(state, dtype=np.float32)

    def get_discard_counts(self):
        """Returns a count of discarded cards as a list of integers."""
        count = Counter(self.discard_pile)
        discard_counts = []
        for value in range(1, 14):  # For values 1 to King (represented as 13)
            if value == 11:
                discard_counts.append(count['J'])
            elif value == 12:
                discard_counts.append(count['Q'])
            elif value == 13:
                discard_counts.append(count['K'])
            else:
                discard_counts.append(count[value])
        return discard_counts

    def perform_action(self, player, action):
        """Handles actions and returns the updated game state, reward, and game-over status."""
        reward = 0

        if action == 'draw':
            drawn_card = self.deck.draw()
            if drawn_card:
                self.handle_card_replacement(player, 0, drawn_card)
                reward += REWARD_FOR_DRAW  # Reward for drawing a new card
            return self.get_state(player), reward, self.game_over

        elif action == 'call_rats':
            points = player.get_total_score()
            opponent_points = self.players[1 - self.turn].get_total_score()
            game_length = len(self.discard_pile)  # Use discard pile length as game length estimate

            if points < opponent_points:
                reward += BASE_RATS_REWARD * (REWARD_DECAY_RATE ** game_length)  # Decayed reward
            elif points > 15:
                reward += PENALTY_FOR_HIGH_SCORE_RATS  # Penalty for high score when calling "Rats"

            if game_length < MIN_TURN_FOR_RATS:
                reward += PENALTY_FOR_EARLY_RATS  # Penalty for calling "Rats" too early

            self.call_rats()
            return self.get_state(player), reward, self.game_over

        elif action == 'peek_opponent':
            # Player uses a Jack to peek at one of the opponent’s hidden cards
            opponent = self.players[1 - self.turn]
            hidden_index = opponent.revealed_cards.index("?")
            if hidden_index != -1:
                opponent_card = opponent.cards[hidden_index]
                player.add_known_opponent_card(opponent_card)
                reward += 5  # Reward for gaining information about opponent's hand
            return self.get_state(player), reward, self.game_over

        elif action == 'peek_self':
            # Player uses a Jack to peek at one of their own hidden cards
            hidden_index = player.revealed_cards.index("?")
            if hidden_index != -1:
                card = player.cards[hidden_index]
                player.add_known_card(card)
                reward += 5  # Reward for self-inspection
            return self.get_state(player), reward, self.game_over

        elif action == 'swap_with_queen':
            # Player uses a Queen to swap one of their own known cards with an opponent's
            card_to_swap = player.cards[0]  # Example: player chooses to swap the first card
            opponent = self.players[1 - self.turn]
            opponent_card = opponent.cards[0]  # Example: opponent's first card

            # Execute the swap between players
            player.cards[0], opponent.cards[0] = opponent_card, card_to_swap
            reward += 5  # Reward for taking the Queen action
            return self.get_state(player), reward, self.game_over


    def call_rats(self):
        """Ends the game when a player calls 'Rats'."""
        self.rats_called = True
        self.game_over = True
        print(f"{self.players[self.turn].name} calls 'Rats'! Game over.")
        self.end_game()

    def end_game(self):
        """Calculates scores and determines the winner."""
        self.game_over = True
        print("Game over! Final scores:")
        for player in self.players:
            print(f"{player.name}: {player.get_total_score()} points")
