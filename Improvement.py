import pygame
import sys
import random
from math import sqrt

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 500
CELL_SIZE = 40
MOUSE_SIZE = 25
BALL_RADIUS = 15
CHEESE_SIZE = 15
SPEED = 5
MOUSE_SPEED = 2
LEVEL_TIME = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WALL_COLOR = (100, 100, 100)
JERRY_BROWN = (205, 170, 125)
JERRY_BELLY = (245, 220, 180)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jerry's Maze Adventure")

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
score = 0
start_ticks = pygame.time.get_ticks()
player_pos = [CELL_SIZE + CELL_SIZE // 2, CELL_SIZE + CELL_SIZE // 2]
mouse_positions = [[CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 1 + CELL_SIZE // 2]]
cheese_positions = []
maze = [
    "#################",
    "#       #       #",
    "# ##### # ## ## #",
    "# #   #   # C # #",
    "# # ### # # # # #",
    "# #             #",
    "# # ## ##  ###  #",
    "#               #",
    "######## ########",
    "#               #",
    "#################",
]


def draw_maze():
    """Draw the maze walls and cheese."""
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "#":
                pygame.draw.rect(screen, WALL_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif cell == "C":
                draw_cheese(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)


def draw_cheese(x, y):
    """Draw cheese as a yellow triangle."""
    points = [(x, y - CHEESE_SIZE), (x - CHEESE_SIZE, y + CHEESE_SIZE), (x + CHEESE_SIZE, y + CHEESE_SIZE)]
    pygame.draw.polygon(screen, YELLOW, points)


def draw_player():
    """Draw the player ball."""
    pygame.draw.circle(screen, BLUE, (int(player_pos[0]), int(player_pos[1])), BALL_RADIUS)


def draw_mice():
    """Draw all mice."""
    for mouse in mouse_positions:
        draw_mouse(mouse)


def draw_mouse(pos):
    """Draw a Jerry-style mouse."""
    x, y = pos

    # Body
    body_length = MOUSE_SIZE * 1.8
    body_width = MOUSE_SIZE * 1.6
    pygame.draw.ellipse(screen, JERRY_BROWN, (x - body_length // 2, y - body_width // 2, body_length, body_width))

    # Belly
    pygame.draw.ellipse(screen, JERRY_BELLY, (x - body_length // 2 + 5, y - body_width // 2 + 5, body_length - 10, body_width - 10))

    # Head
    head_size = MOUSE_SIZE * 1.2
    pygame.draw.circle(screen, JERRY_BROWN, (int(x), int(y)), int(head_size // 2))


def move_player():
    """Move the player based on key input."""
    keys = pygame.key.get_pressed()
    new_pos = player_pos.copy()

    if keys[pygame.K_UP]:
        new_pos[1] -= SPEED
    if keys[pygame.K_DOWN]:
        new_pos[1] += SPEED
    if keys[pygame.K_LEFT]:
        new_pos[0] -= SPEED
    if keys[pygame.K_RIGHT]:
        new_pos[0] += SPEED

    if not is_collision(new_pos):
        player_pos[0], player_pos[1] = new_pos


def move_mice():
    """Move each mouse toward the nearest cheese."""
    for mouse in mouse_positions:
        if cheese_positions:
            target_cheese = min(cheese_positions, key=lambda c: distance(mouse, c))
            dx, dy = target_cheese[0] - mouse[0], target_cheese[1] - mouse[1]
            dist = sqrt(dx ** 2 + dy ** 2)
            if dist > 0:
                mouse[0] += MOUSE_SPEED * dx / dist
                mouse[1] += MOUSE_SPEED * dy / dist


def is_collision(pos):
    """Check if the given position collides with a wall."""
    x, y = int(pos[0] // CELL_SIZE), int(pos[1] // CELL_SIZE)
    return maze[y][x] == "#"


def check_cheese_collision():
    """Check if any mouse reaches a cheese."""
    global cheese_positions
    for mouse in mouse_positions[:]:
        for cheese in cheese_positions[:]:
            if distance(mouse, cheese) < MOUSE_SIZE + CHEESE_SIZE:
                cheese_positions.remove(cheese)  # Cheese disappears
                mouse_positions.append([mouse[0], mouse[1]])  # Replicate mouse


def check_player_collision():
    """Check if the player collides with any mouse."""
    global score
    for mouse in mouse_positions[:]:
        if distance(player_pos, mouse) < BALL_RADIUS + MOUSE_SIZE:
            mouse_positions.remove(mouse)
            score += 10


def distance(pos1, pos2):
    """Calculate distance between two points."""
    return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def load_cheese_positions():
    """Load cheese positions from the maze."""
    positions = []
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "C":
                positions.append([x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2])
    return positions


def display_end_screen(message):
    """Display the end screen with a message."""
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
            main()
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()


def main():
    global cheese_positions, mouse_positions, player_pos, score
    cheese_positions = load_cheese_positions()
    mouse_positions = [[CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 1 + CELL_SIZE // 2]]
    player_pos = [CELL_SIZE + CELL_SIZE // 2, CELL_SIZE + CELL_SIZE // 2]
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        remaining_time = max(LEVEL_TIME - elapsed_time, 0)

        if remaining_time == 0:
            display_end_screen(f"Time's up! Final score: {score}")

        move_player()
        move_mice()
        check_cheese_collision()
        check_player_collision()

        screen.fill(WHITE)
        draw_maze()
        draw_player()
        draw_mice()

        # UI
        timer_text = font.render(f"Time left: {remaining_time}s", True, RED)
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(timer_text, (10, 10))
        screen.blit(score_text, (10, 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    main()
