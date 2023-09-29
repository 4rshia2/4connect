# 4Connect

## 4 Connect Game with AI Bot
This Python program allows you to play a game of 4 Connect against an AI bot. You can choose to play against the AI or watch two AI bots play against each other.

## Game Modes
1.Player vs. AI: You can play against an AI bot.  
2.AI vs. AI: You can watch two AI bots play against each other.  

## Rules
The game is played on a grid with a user-specified number of rows and columns.  
The goal is to connect four of your pieces (either player or AI) horizontally, vertically, or diagonally.  
Players take turns placing their pieces on the grid.  
The game ends when either a player wins by connecting four pieces or the grid is full, resulting in a draw.
## Setup
Run the program and choose the game mode (Player vs. AI or AI vs. AI).  
Enter the number of rows and columns for the game grid.  
Follow the on-screen instructions to play the game or watch AI vs. AI.  
## How to Play
### Player vs. AI
In this mode, you play as the player, and the AI bot is your opponent.  
Click on the desired column where you want to place your piece.  
The AI bot will take its turn, and the game will continue until there is a winner or a draw.  
### AI vs. AI
In this mode, you can sit back and watch two AI bots play against each other.  
The AI bots will take turns automatically.  
The game will display the winner when the AI bots finish playing.  
## Code Structure
4_connect_game.py: Contains the main Python code for the game.  
Numpy: Utilizes the NumPy library for game board operations.  
Pygame: Uses the Pygame library for the game's graphical interface.  
Various functions and variables for game logic, AI bot moves, and user interface.
