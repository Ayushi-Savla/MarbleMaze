# file: maze_game.py

import pygame
import random
from time import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
BALL_RADIUS = 10
MOUSE_SIZE = 15
CHEESE_SIZE = 10
FPS = 30
GAME_DURATION = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Maze Game")

# Fonts
font = pygame.font.Font(None, 36)

# Timer and score
start_time = time()
score = 0

# Maze (simple grid for demo purposes)
maze = [[random.choice([" ", "C"]) if random.random() < 0.1 else " " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
maze[0][0] = " "  # Start point is clear

# Player and mouse positions
player_pos = [0, 0]
mice_positions = [[random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)] for _ in range(5)]
cheese_positions = [[i, j] for i in range(GRID_SIZE) for j in range(GRID_SIZE) if maze[i][j] == "C"]

# Movement directions
directions = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}


def draw_maze():
    """Draw the maze grid."""
    cell_width = WIDTH // GRID_SIZE
    cell_height = HEIGHT // GRID_SIZE
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Draw grid
            if maze[y][x] == "C":  # Draw cheese
                pygame.draw.circle(
                    screen, YELLOW, (x * cell_width + cell_width // 2, y * cell_height + cell_height // 2), CHEESE_SIZE
                )


def draw_player():
    """Draw the player's ball."""
    cell_width = WIDTH // GRID_SIZE
    cell_height = HEIGHT // GRID_SIZE
    pygame.draw.circle(
        screen,
        BLUE,
        (player_pos[0] * cell_width + cell_width // 2, player_pos[1] * cell_height + cell_height // 2),
        BALL_RADIUS,
    )


def draw_mice():
    """Draw mice in the maze."""
    cell_width = WIDTH // GRID_SIZE
    cell_height = HEIGHT // GRID_SIZE
    for mouse in mice_positions:
        pygame.draw.circle(
            screen,
            RED,
            (mouse[0] * cell_width + cell_width // 2, mouse[1] * cell_height + cell_height // 2),
            MOUSE_SIZE,
        )


def move_mice():
    """Move mice randomly."""
    for mouse in mice_positions:
        if random.random() < 0.5:  # Move 50% of the time
            direction = random.choice(list(directions.values()))
            new_x = (mouse[0] + direction[0]) % GRID_SIZE
            new_y = (mouse[1] + direction[1]) % GRID_SIZE
            if maze[new_y][new_x] != "C":  # Avoid cheese
                mouse[0], mouse[1] = new_x, new_y
            else:  # Replicate mice on cheese
                mice_positions.append([new_x, new_y])


def check_collisions():
    """Check collisions between player and mice or cheese."""
    global score
    for mouse in mice_positions[:]:
        if mouse == player_pos:  # Player hits mouse
            mice_positions.remove(mouse)
            score += 10


def handle_input():
    """Handle player movement input."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos[1] = max(0, player_pos[1] - 1)
    if keys[pygame.K_DOWN]:
        player_pos[1] = min(GRID_SIZE - 1, player_pos[1] + 1)
    if keys[pygame.K_LEFT]:
        player_pos[0] = max(0, player_pos[0] - 1)
    if keys[pygame.K_RIGHT]:
        player_pos[0] = min(GRID_SIZE - 1, player_pos[0] + 1)


# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Game time
    elapsed_time = time() - start_time
    if elapsed_time > GAME_DURATION:
        running = False
        break

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    handle_input()
    move_mice()
    check_collisions()

    # Draw everything
    draw_maze()
    draw_player()
    draw_mice()

    # Display score and timer
    score_text = font.render(f"Score: {score}", True, WHITE)
    timer_text = font.render(f"Time: {int(GAME_DURATION - elapsed_time)}s", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(timer_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

# End screen
screen.fill(BLACK)
if len(mice_positions) > 5:
    end_text = font.render("You Lost!", True, RED)
else:
    end_text = font.render("You Won!", True, WHITE)
final_score_text = font.render(f"Final Score: {score}", True, WHITE)
screen.blit(end_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()

