from game_logic import Game, Player

def compute_sizes():
    # Initialize dummy players and game
    player1 = Player("Dummy_Player1", is_human=False)
    player2 = Player("Dummy_Player2", is_human=False)
    game = Game(player1, player2)

    # Dynamically calculate state and action sizes
    state_size = len(game.get_state(player1))
    action_size = len(game.get_available_actions())
    return state_size, action_size

if __name__ == "__main__":
    # Compute sizes and write to config.py
    state_size, action_size = compute_sizes()

    with open("config.py", "a") as config_file:
        config_file.write(f"\nSTATE_SIZE = {state_size}\n")
        config_file.write(f"ACTION_SIZE = {action_size}\n")

    print(f"STATE_SIZE set to: {state_size}")
    print(f"ACTION_SIZE set to: {action_size}")
