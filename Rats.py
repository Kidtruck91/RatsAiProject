from tkinter import Tk
from game_logic import Game, Player
from GuiRes import RatsGameGUI
from q_learning_agent import DQNAgent


def main():
    # Initialize Tkinter
    root = Tk()

    # Create players and game
    player1 = Player("Player 1", True)
    player2 = Player("AI Player")
    game = Game(player1, player2)

    # Initialize AI agents
    agent1 = DQNAgent(state_size=21, action_size=5)
    agent2 = DQNAgent(state_size=21, action_size=5)

    # Initialize GUI
    gui = RatsGameGUI(root, game, player1, player2)

    # Start game logic
    def game_loop():
        """
        The main game loop. Alternates turns between the human and AI.
        """
        if game.game_over:
            print("Game Over!")
            return

        if game.turn == 0:  # Human turn
            gui.update_gui()
            print("Human turn. Waiting for action...")
        else:  # AI turn
            print("AI turn.")
            state = game.get_state(player2)
            valid_actions = game.get_available_actions()
            action = agent2.choose_action(state, valid_actions)
            print(f"AI chose action: {action}")
            game.perform_action(player2, action)
            gui.update_gui()

            # Check game status after the AI's turn
            if game.game_over:
                print("Game Over!")
                return

            # Switch back to the human turn
            game.turn = 0
            game_loop()

    # Start GUI event loop
    gui.update_gui()
    root.after(100, game_loop)  # Start the game loop with a delay
    root.mainloop()


if __name__ == "__main__":
    main()