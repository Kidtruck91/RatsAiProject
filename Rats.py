from tkinter import *
from PIL import Image, ImageTk
from game_logic import Game, Player
from q_learning_agent import DQNAgent
import random

root = Tk()
root.title("Rats!")
root.geometry("900x500")
root.configure(background="green")

# Initialize players and game
player1 = Player("Player 1")
player2 = Player("AI Player")
game = Game(player1, player2)

agent1 = DQNAgent(21, 5)
agent2 = DQNAgent(21, 5)

# Load AI weights
agent1.load("/Users/kishanbhagwandas/Downloads/RatsAiProject-main-2/weights/dqn_weights_player1.weights.h5")
agent2.load("/Users/kishanbhagwandas/Downloads/RatsAiProject-main-2/weights/dqn_weights_player2.weights.h5")

# Resize card images
def resize_cards(card_path):
    card_img = Image.open("/Users/kishanbhagwandas/Downloads/RatsAiProject-main-2/cards")
    resized_image = card_img.resize((150, 218))
    return ImageTk.PhotoImage(resized_image)

# Card display variables
player_card_label = None
ai_card_label = None

def update_cards():
    global player_card_label, ai_card_label

    # Display Player 1 cards
    if player1.get_visible_cards():
        card_path = f"/Users/kishanbhagwandas/Downloads/RatsAiProject-main-2/cards{player1.get_visible_cards()[-1]}.png"
        player_card_image = resize_cards(card_path)
        player_card_label.config(image=player_card_image)
        player_card_label.image = player_card_image

    # Display AI Player cards
    if player2.get_visible_cards():
        card_path = f"/Users/kishanbhagwandas/Downloads/RatsAiProject-main-2/cards{player2.get_visible_cards()[-1]}.png"
        ai_card_image = resize_cards(card_path)
        ai_card_label.config(image=ai_card_image)
        ai_card_label.image = ai_card_image

def ai_turn(player, agent):
    state = game.get_state(player)
    action = agent.choose_action(state)
    game.perform_action(player, ['draw', 'call_rats', 'peek_opponent', 'peek_self', 'swap_with_queen'][action])
    update_cards()

def human_turn(player):
    state = game.get_state(player)
    print(f"Your cards: {player.get_visible_cards()}")
    action = input("Choose an action (draw, call_rats, peek_opponent, peek_self, swap_with_queen): ").strip()
    game.perform_action(player, action)
    update_cards()

def run_game(mode):
    game.reset_game()
    update_cards()
    if mode == 1:  # AI vs AI
        while not game.game_over:
            ai_turn(player1, agent1)
            if not game.game_over:
                ai_turn(player2, agent2)
    elif mode == 2:  # Human vs AI
        while not game.game_over:
            human_turn(player1)
            if not game.game_over:
                ai_turn(player2, agent2)
    elif mode == 3:  # AI vs Human
        while not game.game_over:
            ai_turn(player1, agent1)
            if not game.game_over:
                human_turn(player2)

# Setup Tkinter Frames
frame = Frame(root, bg="green")
frame.pack(pady=20)

player_frame = LabelFrame(frame, text="Player 1", bd=0)
player_frame.grid(row=0, column=0, padx=20)

ai_frame = LabelFrame(frame, text="AI Player", bd=0)
ai_frame.grid(row=0, column=1, padx=20)

# Labels for cards
player_card_label = Label(player_frame, text='', bg="green")
player_card_label.pack(pady=20)

ai_card_label = Label(ai_frame, text='', bg="green")
ai_card_label.pack(pady=20)

# Buttons
def start_human_vs_ai():
    run_game(2)

shuffle_button = Button(root, text="Start Human vs AI", font=("Helvetica", 14), command=start_human_vs_ai)
shuffle_button.pack(pady=20)

# Initialize card display
update_cards()

root.mainloop()
