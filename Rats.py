import argparse
from game_logic import Game, Player
from q_learning_agent import DQNAgent
from tkinter import Tk
from GuiRes import RatsGameGUI
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run Rats game.")
    parser.add_argument("--gui", action="store_true", help="Enable GUI mode")
    args = parser.parse_args()

    # Create players and game
    player1 = Player("Player 1", True)
    player2 = Player("AI Player")
    game = Game(player1, player2)

    if args.gui:
        # Run the game with the GUI
        

        root = Tk()
        gui = RatsGameGUI(root, game, player1, player2)
        gui.update_gui()
        root.mainloop()
    else:
        # Run the game in CLI mode
        run_cli_game(game, player1, player2)

def run_cli_game(game, player1, player2):
    print("Welcome to Rats (CLI Mode)!")
    
    # Initialize AI Agent
    agent = DQNAgent(state_size=21, action_size=5)

    while not game.game_over:
        # Determine the active player and opponent dynamically
        current_player = game.players[game.turn]
        opponent = game.players[1 - game.turn]

        if current_player.is_human:
            print(f"\n{current_player.name}'s turn!")
            print(f"Your cards: {game.display_hand(current_player)}")
            print("Available actions:", ", ".join(game.get_available_actions()))
            action = input("Choose an action: ").strip().lower()
            if action in game.get_available_actions():
                game.perform_action(current_player, action)
            else:
                print("Invalid action. Try again.")
        else:
            print(f"\n{current_player.name}'s turn (AI)...")
            print(f"{current_player.name}'s cards: {game.display_hand(current_player)}")
            valid_actions = game.get_available_actions()
            state = game.get_state(current_player)
            action_index = agent.choose_action(state, valid_actions)
            action = valid_actions[action_index]
            print(f"{current_player.name} (AI) chose action: {action}")
            game.perform_action(current_player, action, agent=agent)

        # Check if the game is over
        if game.game_over:
            print("\nGame Over!")
            for player in game.players:
                print(f"{player.name}: {player.get_total_score()} points")
            if game.players[0].get_total_score() < game.players[1].get_total_score():
                print(f"{game.players[0].name} wins!")
            elif game.players[0].get_total_score() > game.players[1].get_total_score():
                print(f"{game.players[1].name} wins!")
            else:
                print("It's a tie!")

if __name__ == "__main__":
    main()
