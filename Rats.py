from game_logic import Game, Player
from q_learning_agent import DQNAgent

player1 = Player("Player 1")  # Human or AI
player2 = Player("AI Player")  # AI agent
game = Game(player1, player2)

state_size = 4
action_size = 2
agent1 = DQNAgent(state_size, action_size)  # Player 1's trained agent
agent2 = DQNAgent(state_size, action_size)  # Player 2's trained agent

# Load the trained weights
agent1.load("dqn_weights_player1.weights.h5")
agent2.load("dqn_weights_player2.weights.h5")

def run_game(player1_type="human", player2_type="ai"):
    game.reset_game()
    game_over = False
    current_agent = agent1 if player1_type == "ai" else agent2

    while not game.game_over:
        current_player = game.players[game.turn]
        if game.turn == 0 and player1_type == "ai":
            state = game.get_state(current_player)
            action = agent1.choose_action(state)
            action_str = 'draw' if action == 0 else 'call_rats'
            game.perform_action(current_player, action_str)
        elif game.turn == 1 and player2_type == "ai":
            state = game.get_state(current_player)
            action = agent2.choose_action(state)
            action_str = 'draw' if action == 0 else 'call_rats'
            game.perform_action(current_player, action_str)
        else:
            print(f"\n{current_player.name}'s turn.")
            print(f"Visible cards: {current_player.get_visible_cards()}")
            action = input("Choose an action ('draw' or 'call_rats'): ").strip().lower()
            game.perform_action(current_player, action)

    game.end_game()

if __name__ == "__main__":
    run_game(player1_type="human", player2_type="ai")
