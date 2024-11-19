# MARBLE MAZE
![Screenshot (116)](https://github.com/user-attachments/assets/d1081160-6793-4aff-ad58-c85d4500c9a0)
# What it does
This game is a simple maze navigation game called "Marble Maze." The player controls a marble and navigates it through a maze. The goal is to move the marble around the maze without colliding with walls.
# Dependencies
To build this game, the following dependencies/packages were used:
  1. Pygame to generate the game and the layout.
  2. Sys to provide access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
# How we built it
In this project, we built a simple maze game where a player navigates a marble using the arrow keys. Key techniques include grid-based collision detection, layered rendering for a 3D marble effect, and real-time input handling. 
# Installation and Running
The game created can be created or installed through the following procedure:
  1. Download the latest version of Python onto your machine. This can be done from this link: [Download Python](https://www.python.org/downloads/). It is applicable for both Windows/MacOS systems.
  2. Once the downloaded file is completely downloaded, click on it to execute the file which will install the Python program on the machine.
  3. Once the installation is complete, to verify that Python downloaded successfully, navigate to the command prompt/terminal and type the following command: `python --version` which will display the version of python downloaded.
  4. To run a test to see if it installed properly, use the following:
     ```
     py
     print("Hello World!")
     ```
     It should return the output: *Hello World!*
  5. In the navigation window/bar, search for the IDLE Shell which is downloaded together with other Python modules. Click on it to open it and you can run the same command above to test if it is working.
  6. Ensure to have Git downloaded to clone the repository from GitHub. [Download Git](https://git-scm.com/downloads)
  7. Clone the repository using this link: [Marble Maze Python Game](https://github.com/Ayushi-Savla/MarbleMaze) or directly from a terminal/command line using the commands: 
     ```
     git clone https://github.com/Ayushi-Savla/MarbleMaze.git
     cd marble-maze
     ```
  8. **Install the dependencies** using the `pip` command from any python editor like Pycharm or directly from a command line terminal. In our case, we made use of the following dependencies:
     ```
     pip install pygame
     pip install sys
     ```
  9. Once your environment is set, with all the dependencies and the files downloaded, run the command `python mazegame.py` to run the main script. If using an IDE like Pycharm or Visual Studio, once you have cloned the repository, just run the main file from the IDE by clicking the **run** button.
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
