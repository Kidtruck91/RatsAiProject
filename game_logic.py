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
        self.revealed_cards = [False, False, False]  # True if the card is visible, False if hidden
        self.known_opponent_cards = set()  # Tracks specific opponent cards the player has seen

    def set_initial_cards(self, card1, card2, card3):
        self.cards = [card1, card2, card3]
        self.revealed_cards = [True, False, True]  # Default visibility of cards

    def replace_card(self, index, new_card):
        old_card = self.cards[index]
        self.cards[index] = new_card
        self.revealed_cards[index] = True  # Reveal the replaced card
        return old_card

    def reveal_card(self, index):
        if 0 <= index < len(self.cards):
            self.revealed_cards[index] = True

    def get_visible_cards(self):
        return [
            card if revealed else "?"
            for card, revealed in zip(self.cards, self.revealed_cards)
        ]

    def get_total_score(self):
        total = 0
        for card in self.cards:
            if card == 'K':  # Kings are worth 0
                total += 0
            elif card in ['J', 'Q']:  # Jacks and Queens are worth 11
                total += 11
            else:
                total += card  # Numeric cards retain their value
        return total

    def knows_opponent_card(self, card):
        return card in self.known_opponent_cards

    def add_known_opponent_card(self, card):
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
        discarded_card = player.replace_card(index, drawn_card)
        self.discard_pile.append(discarded_card)

    def deal_initial_cards(self):
        for player in self.players:
            player.set_initial_cards(self.deck.draw(), self.deck.draw(), self.deck.draw())

    def reset_game(self):
        self.deck = Deck()
        self.discard_pile = []
        self.turn = 0
        self.rats_called = False
        self.game_over = False
        self.deal_initial_cards()

    def get_state(self, player):
        state = []

        # Player's own cards
        for card, revealed in zip(player.cards, player.revealed_cards):
            if card == "K":
                state.append(0)  # King as 0
            elif card in ["J", "Q"]:
                state.append(11)  # Jack and Queen as 11
            elif not revealed:
                state.append(-1)  # Unknown card
            else:
                state.append(card)  # Numeric card values (1-10)

        # Opponent's visible cards
        opponent = self.players[1 - self.turn]
        for card in opponent.get_visible_cards():
            state.append(card if player.knows_opponent_card(card) else -1)

        # Additional game information
        state.append(player.get_total_score())  # Player's score
        state.append(len(self.deck.cards))  # Remaining deck size

        # Discard pile summary
        discard_counts = self.get_discard_counts()
        state.extend(discard_counts)

        return np.array(state, dtype=np.float32)

    def get_discard_counts(self):
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
                reward += REWARD_FOR_DRAW
            else:
                print("Deck is empty. Ending the game.")
                self.game_over = True

        elif action == 'call_rats':
            points = player.get_total_score()
            opponent_points = self.players[1 - self.turn].get_total_score()
            game_length = len(self.discard_pile)
            if points < opponent_points:
                reward += BASE_RATS_REWARD * (REWARD_DECAY_RATE ** game_length)
            elif points > 15:
                reward += PENALTY_FOR_HIGH_SCORE_RATS
            if game_length < MIN_TURN_FOR_RATS:
                reward += PENALTY_FOR_EARLY_RATS
            self.call_rats()

        elif action == 'peek_opponent':
            opponent = self.players[1 - self.turn]
            if False in opponent.revealed_cards:
                hidden_index = opponent.revealed_cards.index(False)
                opponent_card = opponent.cards[hidden_index]
                player.add_known_opponent_card(opponent_card)
                print(f"{player.name} peeked at opponent's card: {opponent_card}")
                reward += 5
            else:
                print(f"{opponent.name} has no hidden cards to peek at.")

        elif action == 'peek_self':
            if False in player.revealed_cards:
                hidden_index = player.revealed_cards.index(False)
                card = player.cards[hidden_index]
                player.reveal_card(hidden_index)
                print(f"{player.name} peeked at their card: {card}")
                reward += 5
            else:
                print(f"{player.name} has no hidden cards to peek at.")

        elif action == 'swap_with_queen':
            opponent = self.players[1 - self.turn]
            if player.cards and opponent.cards:
                card_to_swap = player.cards[0]
                opponent_card = opponent.cards[0]
                player.cards[0], opponent.cards[0] = opponent_card, card_to_swap
                reward += 5
                print(f"{player.name} swapped {card_to_swap} with {opponent_card}.")
            else:
                print("Swap cannot be performed. One or both players have no cards.")

        if not self.game_over:
            self.turn = (self.turn + 1) % 2

        return self.get_state(player), reward, self.game_over

    def call_rats(self):
        self.rats_called = True
        self.game_over = True
        print(f"{self.players[self.turn].name} calls 'Rats'! Game over.")
        self.end_game()

    def end_game(self):
        print("Final Scores:")
        for player in self.players:
            print(f"{player.name}: {player.get_total_score()} points")
