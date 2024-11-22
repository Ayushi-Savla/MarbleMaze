import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 500
CELL_SIZE = 40
MARBLE_RADIUS = 15
SPEED = 5
BASE_SPEED = 5
LEVEL_TIME = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Marble Maze")

# Fonts
font = pygame.font.Font(None, 36)

# Marble position
marble_pos = [CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 1 + CELL_SIZE // 2]  # Start in an open space

# Maze layout
mazes = [
    [
        "#################",
        "#       #       #",
        "# ##### # ## ## #",
        "# #   #   # G # #",
        "# # ### # # # # #",
        "# #             #",
        "# # ## ##  ###  #",
        "#               #",
        "######## ########",
        "#               #",
        "#################",
    ],
    [
        "#################",
        "#        #      #",
        "# ##### ## ##### #",
        "# #   #        # #",
        "# # # ##### ##### #",
        "# # #         #  #",
        "# ### #### #### ##",
        "#       #        #",
        "######## #########",
        "#                 #",
        "###################",
    ],
    [
        "#################",
        "#        #      #",
        "### #### ###### #",
        "#  #   #     # G #",
        "#  ##### ##### ##",
        "#               #",
        "##### #### ##### #",
        "#     #          #",
        "####### ##########",
        "#                 #",
        "###################",
    ]
]

# Function to randomize `C` positions in the maze
def randomize_c_positions(maze, num_items=5):
    empty_positions = []
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == " ":  # Empty space
                empty_positions.append((x, y))

    random_positions = random.sample(empty_positions, min(num_items, len(empty_positions)))

    maze_with_c = []
    for y, row in enumerate(maze):
        row_list = list(row)
        for x, cell in enumerate(row_list):
            if (x, y) in random_positions:
                row_list[x] = "C"
        maze_with_c.append("".join(row_list))

    return maze_with_c

# Function to reset the game
def reset_game(level_index=0):
    global marble_pos, start_ticks, score, speed, current_level, mazes
    marble_pos = [CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 1 + CELL_SIZE // 2]
    start_ticks = pygame.time.get_ticks()
    score = 0
    speed = BASE_SPEED
    current_level = level_index
    mazes[current_level] = randomize_c_positions(mazes[current_level], num_items=5)

reset_game()

# Function to draw the maze
def draw_maze():
    for y, row in enumerate(mazes[current_level]):
        for x, cell in enumerate(row):
            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == "#":
                pygame.draw.rect(screen, BLACK, rect)
            elif cell == "G":
                pygame.draw.rect(screen, GREEN, rect)
            elif cell == "C":
                pygame.draw.circle(screen, YELLOW, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 10)

# Function to draw a gradient circle to simulate a sphere
def draw_sphere(position):
    for i in range(MARBLE_RADIUS, 0, -1):
        color_value = int(255 * ((MARBLE_RADIUS - i) / MARBLE_RADIUS))
        color = (255, color_value, color_value)
        pygame.draw.circle(screen, color, (position[0], position[1]), i)

# Check for collisions with walls
def is_collision(position):
    x, y = position
    if x - MARBLE_RADIUS < 0 or x + MARBLE_RADIUS >= WIDTH:
        return True
    if y - MARBLE_RADIUS < 0 or y + MARBLE_RADIUS >= HEIGHT:
        return True

    for dx in [-MARBLE_RADIUS, MARBLE_RADIUS]:
        for dy in [-MARBLE_RADIUS, MARBLE_RADIUS]:
            edge_x = (x + dx) // CELL_SIZE
            edge_y = (y + dy) // CELL_SIZE

            if edge_y < 0 or edge_y >= len(mazes[current_level]):
                continue
            if edge_x < 0 or edge_x >= len(mazes[current_level][0]):
                continue
            if mazes[current_level][edge_y][edge_x] == "#":
                return True
    return False

# Function to check if the marble reached the goal
def check_goal(position):
    x, y = position
    cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE
    return mazes[current_level][cell_y][cell_x] == "G"

# Function to collect items
def collect_items(position):
    global score
    x, y = position
    cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE

    if mazes[current_level][cell_y][cell_x] == "C":
        row = list(mazes[current_level][cell_y])
        row[cell_x] = " "
        mazes[current_level][cell_y] = "".join(row)
        score += 1
        return True
    return False

# Function to display the end screen
def display_end_screen(message):
    screen.fill(WHITE)
    end_text = font.render(message, True, RED)
    restart_text = font.render("Press R to restart or Q to quit", True, RED)
    screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            reset_game()
            return
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

# Main game loop
def main():
    global marble_pos, score, speed, current_level

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(LEVEL_TIME - elapsed_time, 0)

        if remaining_time == 0:
            display_end_screen(f"Time's up! Final score: {score}")

        keys = pygame.key.get_pressed()
        new_marble_pos = marble_pos.copy()

        if keys[pygame.K_LEFT]:
            new_marble_pos[0] -= SPEED
        if keys[pygame.K_RIGHT]:
            new_marble_pos[0] += SPEED
        if keys[pygame.K_UP]:
            new_marble_pos[1] -= SPEED
        if keys[pygame.K_DOWN]:
            new_marble_pos[1] += SPEED

        if not is_collision(new_marble_pos):
            marble_pos = new_marble_pos

        if collect_items(marble_pos):
            score += 1

        if check_goal(marble_pos):
            current_level += 1
            if current_level >= len(mazes):
                display_end_screen(f"Congratulations! Final score: {score}")
            else:
                reset_game(current_level)

        screen.fill(WHITE)
        draw_maze()
        draw_sphere(marble_pos)

        timer_text = font.render(f"Time left: {remaining_time}s", True, RED)
        score_text = font.render(f"Score: {score}", True, RED)
        level_text = font.render(f"Level: {current_level + 1}", True, RED)
        screen.blit(timer_text, (10, 10))
        screen.blit(score_text, (10, 50))
        screen.blit(level_text, (10, 90))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()
