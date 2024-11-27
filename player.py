class Player:
    def __init__(self, name,is_human=False):
        self.name = name
        self.cards = [None, None, None]  # The player's three cards
        self.is_human = is_human
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
