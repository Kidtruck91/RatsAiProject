from tkinter import *
from PIL import Image, ImageTk
from game_logic import Game, Player
from q_learning_agent import DQNAgent
from GuiRes import CARD_IMAGES
import os

# Initialize Tkinter window
root = Tk()
root.title("Rats!")
root.geometry("900x500")
root.configure(background="green")

# Initialize players and game
player1 = Player("Player 1")
player2 = Player("AI Player")
game = Game(player1, player2)

# Initialize agents
agent1 = DQNAgent(21, 5)
agent2 = DQNAgent(21, 5)

# Load AI weights from the weights folder
weights_dir = "./weights"
agent1.load(os.path.join(weights_dir, "dqn_weights_player1.weights.h5"))
agent2.load(os.path.join(weights_dir, "dqn_weights_player2.weights.h5"))

# Resize card images
def resize_cards(card_path):
    """
    Resize a card image to fit the display size.
    :param card_path: Path to the card image file.
    :return: Resized card image as a PhotoImage object.
    """
    try:
        card_img = Image.open(card_path)
        resized_image = card_img.resize((150, 218))  # Adjust size as needed
        return ImageTk.PhotoImage(resized_image)
    except FileNotFoundError:
        print(f"Card image not found: {card_path}")
        return None

# Card display variables
player_card_labels = []
ai_card_labels = []

def update_cards():
    """
    Update card displays for both players.
    """
    # Clear old labels
    for label in player_card_labels:
        label.destroy()
    for label in ai_card_labels:
        label.destroy()

    # Display Player 1 cards
    for i, card in enumerate(player1.get_visible_cards()):
        card_path = CARD_IMAGES.get(card, "./cards/default.png")
        card_image = resize_cards(card_path)
        if card_image:
            card_label = Label(player_frame, image=card_image, bg="green")
            card_label.image = card_image
            card_label.grid(row=0, column=i)
            player_card_labels.append(card_label)

    # Display AI Player cards
    for i, card in enumerate(player2.get_visible_cards()):
        card_path = CARD_IMAGES.get(card, "./cards/default.png")
        card_image = resize_cards(card_path)
        if card_image:
            card_label = Label(ai_frame, image=card_image, bg="green")
            card_label.image = card_image
            card_label.grid(row=0, column=i)
            ai_card_labels.append(card_label)

def ai_turn(player, agent):
    """
    Handle AI player's turn.
    """
    state = game.get_state(player)
    action = agent.choose_action(state)
    game.perform_action(player, ['draw', 'call_rats', 'peek_opponent', 'peek_self', 'swap_with_queen'][action])
    update_cards()

def human_turn(player):
    """
    Handle Human player's turn.
    """
    state = game.get_state(player)
    print(f"Your cards: {player.get_visible_cards()}")
    action = input("Choose an action (draw, call_rats, peek_opponent, peek_self, swap_with_queen): ").strip().lower()
    game.perform_action(player, action)
    update_cards()

def run_game(mode):
    """
    Start the game in the selected mode.
    """
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

player_frame = LabelFrame(frame, text="Player 1", bd=0, bg="green", fg="white", font=("Helvetica", 14))
player_frame.grid(row=0, column=0, padx=20)

ai_frame = LabelFrame(frame, text="AI Player", bd=0, bg="green", fg="white", font=("Helvetica", 14))
ai_frame.grid(row=0, column=1, padx=20)

# Buttons
def start_human_vs_ai():
    run_game(2)

start_button = Button(root, text="Start Human vs AI", font=("Helvetica", 14), command=start_human_vs_ai)
start_button.pack(pady=20)

# Initialize card display
update_cards()

# Start Tkinter main loop
root.mainloop()
