import pygame
import sys

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
#This maze drawing outlines how the maze will look
mazes = [
    [
        "#################",
        "#       #       #",
        "# ##### # ## ## #",
        "# #   # C # G # #",
        "# # ### # # # # #",
        "# #   C #   #   #",
        "# # ## ##  ###  #",
        "#   C           #",
        "######## ########",
        "#               #",
        "#################",
    ],
    [
        "#################",
        "#C      ##      #",
        "# ##### ## ##### #",
        "#G#   #    C   # #",
        "# # # ##### ##### #",
        "# # #C    C   #  #",
        "# ### #### #### ##",
        "#       #        #",
        "######## #########",
        "#       C         #",
        "###################",
    ],
    [
        "#################",
        "#    C   #      #",
        "### #### ###### #",
        "# C#   #   C #G #",
        "#  ##### ##### ##",
        "#    C     C    #",
        "##### #### ##### #",
        "#     #   C      #",
        "####### ##########",
        "#   C            #",
        "###################",
    ]
]

def reset_game(level_index=0):
    global marble_pos, start_ticks, score, speed, current_level
    marble_pos = [CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 1 + CELL_SIZE // 2]
    start_ticks = pygame.time.get_ticks()
    score = 0
    speed = BASE_SPEED
    current_level = level_index

reset_game()

# Function to draw the maze
def draw_maze():
    for y, row in enumerate(mazes[current_level]):
        for x, cell in enumerate(row):
            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == "#":
                pygame.draw.rect(screen, BLACK, rect)          #This part translates the appearance of the code to what is demonstrated in the picture instead of just # signs
            elif cell == "G":
                pygame.draw.rect(screen, GREEN, rect)
            elif cell == "C":
                pygame.draw.circle(screen, YELLOW, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), 10)

# Function to draw a gradient circle to simulate a sphere
def draw_sphere(position):
    # Draw gradient circles to create a 3D effect with dark outside and light inside
    for i in range(MARBLE_RADIUS, 0, -1):
        # Calculate the color value based on the radius
        color_value = int(255 * ((MARBLE_RADIUS - i) / MARBLE_RADIUS))  # Darker on the outside
        color = (255, color_value, color_value)  # Full pink with varying shades
        pygame.draw.circle(screen, color, (position[0], position[1]), i)

# Check for collisions with walls
def is_collision(position):
    x, y = position

    # To restricts the marble's position to remain within the screen boundaries
    if x - MARBLE_RADIUS < 0 or x + MARBLE_RADIUS >= WIDTH:
        return True
    if y - MARBLE_RADIUS < 0 or y + MARBLE_RADIUS >= HEIGHT:
        return True

    # Check for collisions with walls
    for dx in [-MARBLE_RADIUS, MARBLE_RADIUS]:
        for dy in [-MARBLE_RADIUS, MARBLE_RADIUS]:
            edge_x = (x + dx) // CELL_SIZE
            edge_y = (y + dy) // CELL_SIZE

            if edge_y < 0 or edge_y >= len(mazes[current_level]):
                continue
            if edge_x < 0 or edge_x >= len(mazes[current_level][0]):
                continue
            # Check if the cell is a wall
            if mazes[current_level][edge_y][edge_x] == "#":
                return True
    return False

def check_goal(position):
    x,y = position
    cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE
    return mazes[current_level][cell_y][cell_x] == "G"

def collect_items(position):
    global score
    x,y = position
    cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE

    if mazes[current_level][cell_y][cell_x] == "C":
        mazes[current_level][cell_y] = (
            mazes[current_level][cell_y][:cell_x] + " " + mazes[current_level][cell_y][cell_x + 1]
        )
        score += 1
        return True
    return False

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
    global marble_pos, score, speed, current_level  # Declare marble_pos, score, speed, current_level as global

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(LEVEL_TIME - elapsed_time, 0)

        if remaining_time == 0:
            display_end_screen(f"Oh boy! Time's up! Final score: {score}")

        # the keys to control the sphere
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

        # Check for collision before updating position
        if not is_collision(new_marble_pos):
            marble_pos = new_marble_pos

        if collect_items(marble_pos):
            score += 1

        if check_goal(marble_pos):
            current_level += 1
            if current_level >= len(mazes):
                display_end_screen(f"Game over! Final score: {score}")
            else:
                reset_game(current_level)

        # Clear the screen
        screen.fill(WHITE)

        # Draw the maze and the marble
        draw_maze()
        draw_sphere(marble_pos)

        timer_text = font.render(f"Time left: {remaining_time}s", True, RED)
        score_text = font.render(f"Score: {score}", True, RED)
        level_text = font.render(f"Level: {current_level + 1}", True, RED)
        screen.blit(timer_text, (10, 10))
        screen.blit(score_text, (10, 50))
        screen.blit(level_text, (10, 90))

        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main() 