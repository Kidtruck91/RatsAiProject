# game_logic.py - Handles game logic
import random

# Deck class for managing cards
class Deck:
    def __init__(self):
        self.cards = self.create_deck()
        random.shuffle(self.cards)

    def create_deck(self):
        # Create a standard 52-card deck with Kings (K), Jacks (J), Queens (Q)
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
            deck.extend([card_value] * 4)  # 4 of each value (for each suit)
        return deck

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None  # No more cards to draw

# Player class for handling player actions
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = [None, None, None]  # 3 cards, face-down initially
        self.revealed_cards = [None, None, None]  # Revealed card values

    def set_initial_cards(self, card1, card2, card3):
        self.cards = [card1, card2, card3]
        self.revealed_cards[0] = card1  # Player gets to see the first and third cards
        self.revealed_cards[2] = card3

    def replace_card(self, index, new_card):
        old_card = self.cards[index]
        self.cards[index] = new_card
        self.revealed_cards[index] = new_card  # Player knows the new card
        return old_card  # Return the discarded card

    def get_visible_cards(self):
        # Only show what the player remembers (initial revealed cards), '?' for hidden or swapped cards
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

# Game class to handle game logic
class Game:
    def __init__(self, player1, player2):
        self.deck = Deck()
        self.discard_pile = []
        self.players = [player1, player2]
        self.turn = 0  # Track whose turn it is
        self.rats_called = False
        self.game_over = False
        self.rats_caller = None

    def deal_initial_cards(self):
        # Deal initial cards to both players
        for player in self.players:
            player.set_initial_cards(self.deck.draw(), self.deck.draw(), self.deck.draw())

    def next_turn(self):
        if self.game_over:
            return

        current_player = self.players[self.turn]
        print(f"\n{current_player.name}'s turn.")
        print(f"Your cards: {current_player.get_visible_cards()}")
        print(f"Top of the discard pile: {self.discard_pile[-1] if self.discard_pile else 'Empty'}")

        # Player chooses to draw a card or call Rats, only if Rats hasn't already been called
        if not self.rats_called:
            action = input("Do you want to (d)raw a card or call 'Rats' (r)? ").lower()
            if action == 'r':
                self.call_rats()
                return

        # Player draws a card from the draw pile
        drawn_card = self.deck.draw()
        if drawn_card is None:
            self.end_game()
            return

        print(f"Drawn card: {drawn_card}")

        # Player chooses to replace or discard the drawn card
        replace_or_discard = input("Do you want to (r)eplace a card or (d)iscard the drawn card? ").lower()
        if replace_or_discard == 'r':
            card_index = int(input("Which card do you want to replace (1, 2, 3)? "))-1
            self.handle_card_replacement(current_player, card_index, drawn_card)
        else:
            self.handle_discard(current_player, drawn_card)

        # Switch to the next player
        self.turn = (self.turn + 1) % 2

    def handle_card_replacement(self, player, index, drawn_card):
        discarded = player.replace_card(index, drawn_card)
        self.discard_pile.append(discarded)

        # Check if the replaced card is Jack or Queen and apply its effect
        if discarded in ['J', 'Q']:
            self.use_special_power(discarded)

    def handle_discard(self, player, drawn_card):
        self.discard_pile.append(drawn_card)

        # Check if the discarded card is Jack or Queen and apply its effect
        if drawn_card in ['J', 'Q']:
            self.use_special_power(drawn_card)

    def use_special_power(self, card_value):
        if card_value == 'Q':  # Queen: Swap cards
            if input("Do you want to swap a card with the opponent? (y/n) ").lower() == "y":
                self.swap_card()

        elif card_value == 'J':  # Jack: Peek at any card
            if input("Do you want to peek at any card? (y/n) ").lower() == "y":
                self.peek_at_card()

    def swap_card(self):
        current_player = self.players[self.turn]
        opponent = self.players[(self.turn + 1) % 2]
        card_to_swap = int(input(f"Which card do you want to swap? (1, 2, 3): "))-1
        opponent_card_to_swap = int(input(f"Which of your opponent's cards do you want to swap? (1, 2, 3): "))-1

        # Swap cards between players
        temp = current_player.cards[card_to_swap]
        current_player.cards[card_to_swap] = opponent.cards[opponent_card_to_swap]
        opponent.cards[opponent_card_to_swap] = temp

        # Both players lose knowledge of the swapped cards
        current_player.revealed_cards[card_to_swap] = None
        opponent.revealed_cards[opponent_card_to_swap] = None

    def peek_at_card(self):
        player_to_peek_at = int(input("Peek at your (0) or opponent's (1) card? "))
        card_index = int(input("Which card (1, 2, 3)? "))-1

        if player_to_peek_at == 0:
            print(f"Your card: {self.players[self.turn].cards[card_index]}")
            self.players[self.turn].revealed_cards[card_index] = self.players[self.turn].cards[card_index]  # Reveal card until swapped by a Queen
        else:
            print(f"Opponent's card: {self.players[(self.turn + 1) % 2].cards[card_index]}")
            self.players[self.turn].revealed_cards[card_index] = self.players[(self.turn + 1) % 2].cards[card_index]  # Reveal card until swapped by a Queen

    def call_rats(self):
        if self.rats_called:
            print("Rats has already been called.")
            return

        self.rats_called = True
        self.rats_caller = self.turn
        print(f"{self.players[self.turn].name} calls 'Rats'!")
        # The other player gets one last full turn (including the option to replace or discard)
        self.turn = (self.turn + 1) % 2
        self.next_turn()
        # End the game immediately after the other player's turn is complete
        self.end_game()

    def end_game(self):
        self.game_over = True
        print("\nGame over! Time to reveal the hands.")
        for player in self.players:
            print(f"{player.name}'s cards: {player.cards}")
        self.calculate_scores()

    def calculate_scores(self):
        # Calculate each player's score and announce the winner
        for player in self.players:
            total = player.get_total_score()
            print(f"{player.name}'s total score: {total}")

        if self.players[0].get_total_score() < self.players[1].get_total_score():
            print(f"{self.players[0].name} wins!")
        elif self.players[0].get_total_score() > self.players[1].get_total_score():
            print(f"{self.players[1].name} wins!")
        else:
            print("It's a tie!")

    def check_game_state(self):
        # After every turn, check if the game should end (deck empty)
        if len(self.deck.cards) == 0:
            self.end_game()
        else:
            self.turn = (self.turn + 1) % 2  # Switch turns