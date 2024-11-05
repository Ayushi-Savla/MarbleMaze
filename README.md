# MARBLE MAZE
![Screenshot (116)](https://github.com/user-attachments/assets/d1081160-6793-4aff-ad58-c85d4500c9a0)
# What it does
This game is a simple maze navigation game called "Marble Maze." The player controls a marble and navigates it through a maze. The goal is to move the marble around the maze without colliding with walls.
# Dependencies
To build this game, the following dependencies/packages were used:
  Pygame to generate the game and the layout.
  Sys provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
# How we built it
In this project, we built a simple maze game where a player navigates a marble using the arrow keys. Key techniques include grid-based collision detection, layered rendering for a 3D marble effect, and real-time input handling. 
# Installation and Running
The game created can be created or installed throught the following procedure:
  1. Use the `pip` command to install the `pygame` and `sys` library.
  2. Download the file from the repository or copy the code into the compiler.
  3. Run the program from the `main` function.
# Code Overview
1. Initialisation
  - The game initialises the Pygame, screen setting and constants like colors and screen dimensions.
2. Game Elements
  - The maze is represented by a list of strings (`#` for walls; spaces for open paths.
  - The marble is drawn with a gradient effect to simulate a 3D sphere.
3. Functions
  - `draw_maze`: This function draws the maze walls base on the `maze` layout.
  - `draw_sphere`: creates a pink marble with a gradient for a 3D effect.
  - `is_collision`: checks if the marble is colliding with a wall.
4. Main Game Loop
  - Handles events, movement, collision detection and screen updates.
# Accomplishments
1. Developed responsive marble movement with real-time collision detection, allowing the marble to avoid walls naturally.
2. Successfully created a basic, interactive maze game where players can control a marble to navigate through a grid-based maze.
3. This project provided hands-on experience with Pygame, teaching the developer essential skills in game programming, rendering, and event handling.
# What's Next?
This structure could be expanded with additional game features like levels, timers, or goals, enhancing the gameplay experience.
