# Rats.py - Runner script
from game_logic import Game, Player

# Create players
player1 = Player("Player 1")
player2 = Player("Player 2")

# Create game instance
game = Game(player1, player2)

# Deal initial cards to players
game.deal_initial_cards()

# Start game loop
while not game.game_over:
    game.next_turn()