import os
import tkinter as tk
from game_logic import Game, Player

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(BASE_DIR, "cards")

CARD_IMAGES = {
    1: os.path.join(CARDS_DIR, "14_of_clubs.png"),
    2: os.path.join(CARDS_DIR, "2_of_clubs.png"),
    # ... Other card images ...
    "?": os.path.join(CARDS_DIR, "default.png"),
}


class RatsGameGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.player1 = game.players[0]
        self.player2 = game.players[1]
        self.drawn_card = None  # Tracks the most recently drawn card
        self.card_images = self.load_card_images()
        self.setup_gui()

    def load_card_images(self):
        images = {}
        for value, path in CARD_IMAGES.items():
            try:
                images[value] = tk.PhotoImage(file=path).subsample(3, 3)  # Scale down
            except Exception as e:
                print(f"Error loading image for {value}: {e}")
                images[value] = None
        return images

    def setup_gui(self):
        # Create game layout
        self.status_text = tk.Text(self.root, height=6, width=50, state="disabled")
        self.status_text.pack(pady=10)

        self.pile_frame = tk.Frame(self.root)
        self.pile_frame.pack()

        self.draw_pile_label = tk.Label(self.pile_frame, text="Draw Pile")
        self.draw_pile_label.grid(row=0, column=0)
        self.draw_pile_card = tk.Label(self.pile_frame, image=self.card_images["?"])
        self.draw_pile_card.grid(row=1, column=0)

        self.discard_pile_label = tk.Label(self.pile_frame, text="Discard Pile")
        self.discard_pile_label.grid(row=0, column=1)
        self.discard_pile_card = tk.Label(self.pile_frame, image=self.card_images["?"])
        self.discard_pile_card.grid(row=1, column=1)

        self.action_frame = tk.Frame(self.root)
        self.action_frame.pack()

        self.draw_button = tk.Button(self.action_frame, text="Draw", command=self.handle_draw)
        self.draw_button.pack(side="left", padx=5)

        self.call_rats_button = tk.Button(self.action_frame, text="Call Rats", command=lambda: self.handle_action("call_rats"))
        self.call_rats_button.pack(side="left", padx=5)

        self.xray_button = tk.Button(self.action_frame, text="Toggle X-Ray", command=self.toggle_xray_mode)
        self.xray_button.pack(side="left", padx=5)

        self.start_button = tk.Button(self.action_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(side="left", padx=5)

        self.select_buttons = []
        self.setup_player_hands()

    def setup_player_hands(self):
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack()

        for i, card in enumerate(self.player1.cards):
            frame = tk.Frame(self.player_frame)
            frame.pack(side="left", padx=5)
            card_label = tk.Label(frame, image=self.card_images["?"])
            card_label.pack()
            button = tk.Button(frame, text="Select", command=lambda i=i: self.handle_select(i))
            button.pack()
            self.select_buttons.append((card_label, button))

    def update_gui(self):
        # Update player and opponent hands
        for i, (label, button) in enumerate(self.select_buttons):
            card_value = self.player1.cards[i] if self.game.xray_mode else "?"
            label.config(image=self.card_images[card_value])

        # Update draw and discard piles
        top_discard = self.game.discard_pile[-1] if self.game.discard_pile else None
        self.discard_pile_card.config(image=self.card_images.get(top_discard, self.card_images["?"]))
        self.draw_pile_card.config(image=self.card_images["?"])

    def handle_draw(self):
        self.handle_action("draw")

    def handle_select(self, index):
        self.handle_action(f"replace_{index}")

    def handle_action(self, action):
        self.game.perform_action(self.player1, action)
        self.update_gui()
        if self.game.turn == 1:  # AI's turn
            self.perform_ai_turn()

    def perform_ai_turn(self):
        self.append_status("AI is playing...")
        self.game.perform_action(self.player2, "draw")  # Simplified AI logic
        self.update_gui()
        self.append_status("Your turn.")

    def start_game(self):
        self.game.reset_game()
        self.update_gui()

    def toggle_xray_mode(self):
        self.game.xray_mode = not self.game.xray_mode
        self.update_gui()

    def append_status(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.config(state="disabled")
