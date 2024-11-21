RatsAiProject
==============

This project implements a deep reinforcement learning AI for the card game **Rats**. It uses Deep Q-Learning (DQN) to train agents to compete in the game.

Environment Setup
-----------------
To run this project, you need to set up your Python environment with the required packages. Follow these steps:

### Prerequisites
1. **Python**: Make sure Python 3.8 or higher is installed.

2. **Install Required Packages**: Use `pip` to install the necessary libraries. Run the following command in your terminal:
pip install numpy tensorflow keras

### Directory Structure
Ensure your project directory looks like this:
RatsAiProject/  
Trainer.py 
Rats.py
game_logic.py
q_learning_agent.py 
config.py 
weights/

### Notes:
- Create a folder named `weights` in the project directory if it doesn't already exist. This is where model weights will be saved.

Running the Project
-------------------
### Step 1: Train the AI (Trainer.py)
First, train the AI agents by running the `Trainer.py` file. This step initializes the game environment and uses DQN to train two AI agents to compete against each other.

python Trainer.py
Output:
The script will display the training progress, including metrics like:
Victory percentages for both agents.
Average game length.
Number of "Rats" calls by each agent.
Once training is complete, model weights will be saved in the weights directory.
Step 2: Play the Game (Rats.py)
After training, you can simulate or play games using Rats.py. The script provides options for:

AI vs AI
Player vs AI
AI vs Player
Run the script:
python Rats.py

Gameplay Options:

Follow the on-screen prompts to choose the game mode and take actions during the game.
##File Descriptions
1. Trainer.py
Trains two AI agents using Deep Q-Learning.
Saves trained weights in the weights folder.
2. Rats.py
Runs the game using the trained AI models or lets a human player interact with the game.
3. game_logic.py
Contains the mechanics of the game:
Drawing cards.
Calling "Rats."
Managing hands, discards, and scoring.
4. q_learning_agent.py
Implements the DQN agent:
Neural network structure.
Replay memory.
Exploration vs exploitation strategy.
5. config.py
Stores configuration for:
Rewards and penalties.
Hyperparameters for DQN training (e.g., learning rate, discount factor, exploration rate).
6. weights/
Stores the saved weights of the trained models.

Troubleshooting
Model Weight Shape Mismatch:

If you encounter an error while loading model weights (e.g., shape mismatch), delete the existing weights in the weights directory and re-train the models using Trainer.py.

Game Crashing or Logic Issues:

Check for errors in game_logic.py, especially in the perform_action method.

Missing Dependencies:

Ensure all required Python packages are installed by running:
pip install numpy tensorflow keras

Future Enhancements
Improved AI Logic: Adjust rewards and penalties to enhance strategy.
Performance Tracking: Log gameplay data for more insights into AI performance.
GUI Support: Build a graphical interface for better user experience.
Enjoy exploring AI strategies for the game Rats! 🚀 """

Save to a .txt file
readme_path = "/mnt/data/RatsAiProject_README.txt" with open(readme_path, "w") as file: file.write(readme_content)

readme_path
