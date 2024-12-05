import numpy as np
from collections import Counter
from deck import Deck
from player import Player
from config import *
class Game:
    def __init__(self, player1, player2):
        self.deck = Deck()
        self.discard_pile = []
        self.last_discard = None
        self.special_action_available = False
        self.players = [player1, player2]
        self.turn = 0
        self.rats_caller = None
        self.rats_called = False
        self.final_turn = False
        self.last_action = None
        self.game_over = False
        self.special_action_owner = None
        self.turn_counter = 0
        self.deal_initial_cards()

    def deal_initial_cards(self):
        """Deal initial cards to each player."""
        for player in self.players:
            player.set_initial_cards(self.deck.draw(), self.deck.draw(), self.deck.draw())

    def reset_game(self):
        """Reset the game to its initial state."""
        self.deck = Deck()
        self.discard_pile = []
        self.last_discard = None
        self.special_action_available = False
        self.turn = 0
        self.rats_caller = None
        self.rats_called = False
        self.final_turn = False
        self.last_action = None
        self.game_over = False
        self.turn_counter = 0  # Reset turn counter
        self.deal_initial_cards()

    def get_state(self, player):
        """Return the game state for the specified player."""
        state = []
        # Player's own cards
        for card, revealed in zip(player.cards, player.revealed_cards):
            if not revealed:
                state.append(-1)  # Unknown card
            elif card == "K":
                state.append(0)
            elif card in ["J", "Q"]:
                state.append(11)
            else:
                state.append(card)

        # Opponent's visible cards
        opponent = self.players[1 - self.turn]
        for card, revealed in zip(opponent.cards, opponent.revealed_cards):
            if revealed:
                if card == "K":
                    state.append(0)
                elif card in ["J", "Q"]:
                    state.append(11)
                else:
                    state.append(card)
            else:
                state.append(-1)

        # Additional game information
        state.append(player.get_total_score())  # Player's score
        state.append(len(self.deck.cards))  # Cards left in the deck
        state.extend(self.get_discard_counts())  # Discard pile summary
        return np.array(state, dtype=np.float32)
    def display_hand(self, player):
   
        return [
            card if revealed else "?"
            for card, revealed in zip(player.cards, player.revealed_cards)
    ]
    
    def handle_card_replacement(self, player, index, new_card):
        """
        Handle replacing a player's card and updating the discard pile.
        Tracks the last discarded card for potential special actions.
        """
        if index == -1:
            # Discard the drawn card
            self.discard_pile.append(new_card)
            self.last_discard = new_card
            print(f"{player.name} discarded: {new_card}")
        else:
            # Replace the card in the player's hand
            discarded_card = player.replace_card(index, new_card)
            self.discard_pile.append(discarded_card)
            self.last_discard = discarded_card
            print(f"{player.name} replaced card {index} with {new_card} and discarded: {discarded_card}")

        # Check if the discarded card triggers a special action
        if self.last_discard == "J":
            self.special_action_available = True
            self.special_action_owner = player.name
            print(f"{player.name} discarded a Jack! Special action available: Peek.")
        elif self.last_discard == "Q":
            self.special_action_available = True
            self.special_action_owner = player.name
            print(f"{player.name} discarded a Queen! Special action available: Swap.")
        else:
            self.special_action_available = False
            self.special_action_owner = None

    def get_discard_counts(self):
        """Return the count of each card type in the discard pile."""
        count = Counter(self.discard_pile)
        discard_counts = []
        for value in range(1, 14):  # 1 to 13 (King)
            if value == 11:
                discard_counts.append(count["J"])
            elif value == 12:
                discard_counts.append(count["Q"])
            elif value == 13:
                discard_counts.append(count["K"])
            else:
                discard_counts.append(count[value])
        return discard_counts

    def get_available_actions(self):
        """Return a list of valid actions based on the current game state."""
        actions = []

        # Default actions at the start of a turn
        if self.last_action is None or self.last_action in ["discard", "call_rats"]:
            actions = ["draw"]
            if not self.rats_called:  # All
                actions.append("call_rats")
        # Special actions based on last discard
        if self.last_discard == "J" and self.special_action_available and self.special_action_owner == self.players[self.turn].name:
            actions = ["peek_self", "peek_opponent"]

        if self.last_discard == "Q" and self.special_action_available and self.special_action_owner == self.players[self.turn].name:
            actions = ["swap_with_queen"]

        # Actions after drawing a card
        if self.last_action == "draw":
            actions = ["replace_0", "replace_1", "replace_2", "discard"]

        return actions
    def advance_turn(self):
        """Advance the turn to the next player and increment the turn counter."""
        self.turn = (self.turn + 1) % 2  # Alternate between 0 (Player 1) and 1 (Player 2)
        self.turn_counter += 1
        print(f"Turn counter incremented to {self.turn_counter}")
        print(f"Turn has advanced to: {self.players[self.turn].name}")
    def perform_action(self, player, action,agent=None):
        """
        Perform the specified action for the current player.
        Handles drawing, calling Rats, peeking, and swapping.
        """
        print(f"Starting Perform action")
        self.special_action_available = False
        reward=0
        state_before_action = self.get_state(player)
        if len(self.deck.cards) == 0:
            print("Deck is empty. Ending the game.")
            self.end_game()
        if self.rats_caller and self.players[self.turn].name == self.rats_caller:
            print(f"{self.players[self.turn].name} has completed their final turn. Ending the game.")
            self.end_game()
            return state_before_action, reward, self.get_state(player), action
        elif action == "draw":
            if player.is_human:
                self.draw_human(player)
            else:
                reward+=self.draw_ai(player, agent)
        elif action == "peek_self":
            print(f"{player.name} executed peek_self.")
            if player.is_human:
                self.peek_self(player)
            else:
                reward += self.peek_self_ai(player, agent)
        elif action == "peek_opponent":
            print(f"{player.name} executed peek_opponent.")
            if player.is_human:
                self.peek_opponent(player)
            else:
                reward += self.peek_opponent_ai(player, agent)
        elif action == "swap_with_queen":
            print(f"{player.name} executed swap.")
            if player.is_human:
                self.swap_with_queen_human(player)
            else:
                reward += self.swap_with_queen_ai(player, agent)
        elif action == "call_rats":
            points = player.get_total_score()
            opponent_points = self.players[1 - self.turn].get_total_score()
            game_length = self.turn_counter
            # Reward or penalize based on conditions
            if points < opponent_points - LEAD_THRESHOLD:  # Encourage calling if leading significantly
                reward += SIGNIFICANT_LEAD_BONUS
            elif points >= opponent_points:  # Discourage calling when losing or very close
                reward += PENALTY_FOR_CALL_WHILE_BEHIND
            # Penalize high scores (bad hands)
            if points > 10:
                reward += PENALTY_FOR_HIGH_SCORE_RATS

            # Penalize early turns (alternative to deck-based penalty)
            if game_length < MIN_TURN_FOR_RATS:
                reward += PENALTY_FOR_EARLY_RATS

            self.call_rats()
        
        self.advance_turn()
        print(f"Ending Perform action")
        # Capture the next state after the action
        next_state = self.get_state(player)

        # Return state, reward, and next state
        return state_before_action, reward, next_state,action


    def draw_ai(self, player, agent):
        """
        AI logic for drawing a card and making a decision about replacement or discarding.
        Special actions (peeking or swapping) are routed through perform_action.
        """
        # Attempt to draw a card from the deck
        drawn_card = self.deck.draw()
        if not drawn_card:
            print(f"{player.name} cannot draw because the deck is empty.")
            return 0  # No reward if the deck is empty

        print(f"{player.name} drew: {drawn_card}")

        # Get the current state and valid actions for decision-making
        state = self.get_state(player)
        valid_actions = ["replace_0", "replace_1", "replace_2", "discard"]

        # AI chooses an action based on state and valid actions
        action_index = agent.choose_action(state, valid_actions)
        action = valid_actions[action_index]

        # Perform the chosen action
        if action == "discard":
            self.discard_pile.append(drawn_card)
            self.last_discard = drawn_card
            print(f"{player.name} discarded: {drawn_card}")
        else:
            replace_index = int(action.split("_")[1])  # Extract index from "replace_X"
            self.handle_card_replacement(player, replace_index, drawn_card)

        reward = REWARD_FOR_DRAW  # Adjust reward logic if necessary

        # Handle special actions (peeking or swapping) if triggered
        if self.special_action_available and self.special_action_owner == player.name:
            special_actions = []
            if self.last_discard == "J":
                special_actions = ["peek_self", "peek_opponent"]
            elif self.last_discard == "Q":
                special_actions = ["swap_with_queen"]

            if special_actions:
                special_action_index = agent.choose_action(state, special_actions)
                special_action = special_actions[special_action_index]

                # Route special actions through perform_action
                _, special_action_reward, _, _ = self.perform_action(player, special_action, agent)
                reward += special_action_reward

    # Clear the special action flags after use
        self.special_action_available = False
        self.special_action_owner = None

        return reward

    def draw_human(self, player):
        """
        Human logic for drawing a card and making a decision about replacement or discarding.
        Special actions (peeking or swapping) are routed through perform_action.
        """
        drawn_card = self.deck.draw()
        if not drawn_card:
            print("Deck is empty. Cannot draw.")
            return

        print(f"You drew: {drawn_card}")
        while True:
            try:
                replace_index = int(input("Choose which card to replace (0, 1, 2) or -1 to discard: "))
                if replace_index == -1:
                    # Discard the drawn card
                    self.handle_card_replacement(player, -1, drawn_card)
                    break
                elif 0 <= replace_index < len(player.cards):
                    # Replace the card in the player's hand
                    self.handle_card_replacement(player, replace_index, drawn_card)
                    break
                else:
                    print("Invalid choice. Please choose 0, 1, 2, or -1.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Handle special actions (peeking or swapping) if triggered
        if self.special_action_available and self.special_action_owner == player.name:
            special_actions = []
            if self.last_discard == "J":
                special_actions = ["peek_self", "peek_opponent"]
            elif self.last_discard == "Q":
                special_actions = ["swap_with_queen"]

            if special_actions:
                while True:
                    print(f"Special action available: {special_actions}.")
                    choice = input(f"Type one of the following: {special_actions} or 'skip': ").strip().lower()
                    if choice in special_actions:
                        self.perform_action(player, choice)
                        break
                    elif choice == "skip":
                        print("Skipping special action.")
                        break
                    else:
                        print(f"Invalid choice. Please type one of {special_actions} or 'skip'.")

        # Clear the special action flags after use
        self.special_action_available = False
        self.special_action_owner = None
    
    def peek_self_ai(self, player, agent):
            """
            AI logic for peeking at one of its own hidden cards.
            """
            # Determine hidden cards to peek at
            hidden_indices = [i for i, revealed in enumerate(player.revealed_cards) if not revealed]
            
            # If no hidden cards are available, do nothing
            if not hidden_indices:
                print(f"{player.name} has no hidden cards to peek at.")
                reward = 0  # No reward if no hidden cards are available
                return reward

            # AI chooses a hidden card to peek at
            state = self.get_state(player)
            valid_actions = [f"peek_{i}" for i in hidden_indices]
            action_index = agent.choose_action(state, valid_actions)
            action = valid_actions[action_index]
            chosen_index = int(action.split("_")[1])

            # Reveal the chosen card
            player.reveal_card(chosen_index)
            revealed_card = player.cards[chosen_index]
            print(f"{player.name} peeked at their card at index {chosen_index}: {revealed_card}")

            # Assign a reward for gaining information
            reward = REWARD_FOR_DISCOVERY  # Adjust the reward value as needed
            
            # Update AI's memory for reinforcement learning
            next_state = self.get_state(player)
            agent.remember(state, action_index, reward, next_state, False)
            return reward
    
    def peek_self(self, player):
        hidden_indices = [i for i, revealed in enumerate(player.revealed_cards) if not revealed]

        if not hidden_indices:
            print("You have no hidden cards left to peek at.")
            return

        print(f"Your hidden card indices: {hidden_indices}")
        while True:
            try:
                peek_index = int(input(f"Choose a card index to peek at: {hidden_indices}: "))
                if peek_index in hidden_indices:
                    card = player.cards[peek_index]
                    player.reveal_card(peek_index)
                    print(f"You peeked at your card: {card}")
                    break
                else:
                    print("Invalid choice. Please select from the hidden indices.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def peek_opponent_ai(self, player, agent):
            """
            AI logic for peeking at one of the opponent's hidden cards.
            """
            opponent = self.players[1 - self.turn]  # Get the opponent player
            hidden_indices = [i for i, revealed in enumerate(opponent.revealed_cards) if not revealed]
            
            # If no hidden cards are available, do nothing
            if not hidden_indices:
                print(f"{player.name} cannot peek as the opponent has no hidden cards.")
                reward = 0  # No reward for no hidden cards
                return reward

            # AI chooses a hidden opponent card to peek at
            state = self.get_state(player)
            valid_actions = [f"peek_opponent_{i}" for i in hidden_indices]
            action_index = agent.choose_action(state, valid_actions)
            action = valid_actions[action_index]
            chosen_index = int(action.split("_")[-1])

            # Reveal the chosen opponent card
            revealed_card = opponent.cards[chosen_index]
            opponent.reveal_card(chosen_index)
            player.add_known_opponent_card(revealed_card)
            print(f"{player.name} peeked at opponent's card at index {chosen_index}: {revealed_card}")

            # Assign a reward for gaining information
            reward = REWARD_FOR_DISCOVERY_OPPONENT  # Adjust this reward value as needed
            
            # Update AI's memory for reinforcement learning
            next_state = self.get_state(player)
            agent.remember(state, action_index, reward, next_state, False)

            return reward
    
    def peek_opponent(self, player):
        opponent = self.players[1 - self.turn]
        hidden_indices = [i for i, revealed in enumerate(opponent.revealed_cards) if not revealed]

        if not hidden_indices:
            print("Opponent has no hidden cards left to peek at.")
            return

        print(f"Hidden card indices: {hidden_indices}")
        while True:
            try:
                peek_index = int(input(f"Choose a card index to peek at from the opponent: {hidden_indices}: "))
                if peek_index in hidden_indices:
                    card = opponent.cards[peek_index]
                    player.add_known_opponent_card(card)
                    print(f"You peeked at opponent's card: {card}")
                    break
                else:
                    print("Invalid choice. Please select from the hidden indices.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def swap_with_queen_ai(self, player, agent):
            """
            AI logic for deciding whether to use a queen swap and executing it.
            """
            opponent = self.players[1 - self.turn]  # Get the opponent player
            
            # AI chooses whether to use the swap or decline
            state = self.get_state(player)
            valid_swap_decision = ["decline_swap", "use_swap"]
            swap_decision_index = agent.choose_action(state, valid_swap_decision)
            swap_decision = valid_swap_decision[swap_decision_index]

            if swap_decision == "decline_swap":
                print(f"{player.name} declines to use the queen swap.")
                return 0  # Neutral reward for declining

            print(f"{player.name} chooses to use the queen swap.")
            
            # AI chooses which card to give to the opponent
            valid_give_actions = [f"give_{i}" for i in range(3)]
            give_action_index = agent.choose_action(state, valid_give_actions)
            give_action = valid_give_actions[give_action_index]
            give_index = int(give_action.split("_")[-1])  # Extract the index to give

            # Card to be given to the opponent
            given_card = player.cards[give_index]

            # AI chooses which card to take from the opponent
            valid_take_actions = [f"take_{i}" for i in range(3)]
            take_action_index = agent.choose_action(state, valid_take_actions)
            take_action = valid_take_actions[take_action_index]
            take_index = int(take_action.split("_")[-1])  # Extract the index to take

            # The AI does not know the value of hidden cards; treat them as unknown
            opponent_card = opponent.cards[take_index]
            opponent_revealed = opponent.revealed_cards[take_index]
            if not opponent_revealed:
                print(f"{player.name} is taking an unknown card from {opponent.name}.")

            # Perform the swap
            print(f"{player.name} is swapping cards...")
            opponent.cards[take_index] = given_card
            player.cards[give_index] = opponent_card

            print(f"{player.name} gave {given_card} to {opponent.name} and took {opponent_card} from {opponent.name}.")
            
            # Assign rewards based on the effect of the swap
            previous_score = player.get_total_score()
            current_score = player.get_total_score()
            if current_score < previous_score:
                reward = 5  # Reward for reducing score
            elif current_score > previous_score:
                reward = -2  # Penalty for increasing score
            else:
                reward = 1  # Small reward for neutral swap
            
            # Update AI memory
            next_state = self.get_state(player)
            agent.remember(state, take_action_index, reward, next_state, False)
            
            return reward
    
    def swap_with_queen_human(self, player):
            """
            Human logic for deciding whether to use a queen swap and executing it.
            """
            opponent = self.players[1 - self.turn]

            # Ask the player if they want to use the swap
            use_swap = input(f"{player.name}, do you want to use the queen swap? (yes/no): ").strip().lower()
            if use_swap != "yes":
                print(f"{player.name} declines to use the queen swap.")
                return

            # Human chooses which card to give to the opponent
            print(f"{player.name}, choose a card to give to {opponent.name}:")
            for i, (card, revealed) in enumerate(zip(player.cards, player.revealed_cards)):
                print(f"{i}: {card}")
            give_index = int(input("Enter the index of the card to give: "))

            # Human chooses which card to take from the opponent
            print(f"{player.name}, choose a card to take from {opponent.name}:")
            for i, (card, revealed) in enumerate(zip(opponent.cards, opponent.revealed_cards)):
                display_value = card if revealed else "?"
                print(f"{i}: {display_value}")
            take_index = int(input("Enter the index of the card to take: "))

            # Perform the swap
            given_card = player.cards[give_index]
            opponent_card = opponent.cards[take_index]
            opponent.cards[take_index] = given_card
            player.cards[give_index] = opponent_card

            print(f"{player.name} gave {given_card if player.revealed_cards[give_index] else '?'} to {opponent.name} and took {opponent_card if opponent.revealed_cards[take_index] else '?'} from {opponent.name}.")
    
    def call_rats(self):
        
        """Handle the 'Rats' call and set up the final turn."""
        print(f"{self.players[self.turn].name} calls 'Rats'!")
        self.rats_called = True
        self.rats_caller = self.players[self.turn].name
        print(f"{self.players[1 - self.turn].name} gets one final turn!")
        # Set the flag for the game to end after this final turn


    def end_game(self):
        
        scores = [player.get_total_score() for player in self.players]
        if scores[0] < scores[1]:
            print(f"{self.players[0].name} wins!")
        elif scores[1] < scores[0]:
            print(f"{self.players[1].name} wins!")
        else:
            print("It's a tie!")

        # Mark the game as over
        self.game_over = True
