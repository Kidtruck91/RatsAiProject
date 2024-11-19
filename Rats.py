from game_logic import Game, Player
from q_learning_agent import DQNAgent

player1 = Player("Player 1")
player2 = Player("AI Player")
game = Game(player1, player2)

agent1 = DQNAgent(21, 5)
agent2 = DQNAgent(21, 5)

agent1.load("./weights/dqn_weights_player1.weights.h5")
agent2.load("./weights/dqn_weights_player2.weights.h5")

def ai_turn(player, agent):
    state = game.get_state(player)
    action = agent.choose_action(state)
    _, _, _ = game.perform_action(player, ['draw', 'call_rats', 'peek_opponent', 'peek_self', 'swap_with_queen'][action])

def human_turn(player):
    state = game.get_state(player)
    print(f"Your cards: {player.get_visible_cards()}")
    action = input("Choose an action (draw, call_rats, peek_opponent, peek_self, swap_with_queen): ").strip()
    _, _, _ = game.perform_action(player, action)

def run_game(mode):
    game.reset_game()
    if mode == 1:  # AI vs AI
        while not game.game_over:
            ai_turn(player1, agent1)
            if not game.game_over: ai_turn(player2, agent2)
    elif mode == 2:  # Human vs AI
        while not game.game_over:
            human_turn(player1)
            if not game.game_over: ai_turn(player2, agent2)
    elif mode == 3:  # AI vs Human
        while not game.game_over:
            ai_turn(player1, agent1)
            if not game.game_over: human_turn(player2)

if __name__ == "__main__":
    mode = int(input("Choose game mode:\n1. AI vs AI\n2. Human vs AI\n3. AI vs Human\n"))
    run_game(mode)
