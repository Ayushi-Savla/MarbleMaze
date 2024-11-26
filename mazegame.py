import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 500
CELL_SIZE = 40
MOUSE_SIZE = 25  # Increased size for better Jerry appearance
SPEED = 5
BASE_SPEED = 5
LEVEL_TIME = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
CHEESE_COLOR = (255, 215, 0)
WALL_DARK = (100, 100, 100)
WALL_LIGHT = (130, 130, 130)
JERRY_BROWN = (205, 170, 125)  # Main body color for Jerry
JERRY_BELLY = (245, 220, 180)  # Lighter belly color for Jerry

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jerry's Maze Adventure")

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
score = 0
current_level = 0
start_ticks = pygame.time.get_ticks()
mouse_pos = [CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 1 + CELL_SIZE // 2]
mouse_direction = [1, 0]

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


def draw_mouse(pos, direction):
    """Draw a Jerry-style mouse with characteristic round ears and cartoon features"""
    x, y = pos

    # Body (rounder for cartoon look)
    body_length = MOUSE_SIZE * 1.8
    body_width = MOUSE_SIZE * 1.6

    # Draw body shadow for cartoon effect
    pygame.draw.ellipse(screen, (160, 140, 100),
                        (x - body_length // 2 + 3, y - body_width // 2 + 3,
                         body_length, body_width))

    # Main body
    pygame.draw.ellipse(screen, JERRY_BROWN,
                        (x - body_length // 2, y - body_width // 2,
                         body_length, body_width))

    # Belly (characteristic oval shape)
    pygame.draw.ellipse(screen, JERRY_BELLY,
                        (x - body_length // 2 + 5, y - body_width // 2 + 5,
                         body_length - 10, body_width - 10))

    # Head (larger and rounder for cartoon style)
    head_size = MOUSE_SIZE * 1.2
    head_x = x + direction[0] * (body_length // 2 - head_size // 2)
    head_y = y + direction[1] * (body_width // 2 - head_size // 2)

    # Draw head shadow
    pygame.draw.circle(screen, (160, 140, 100),
                       (int(head_x) + 2, int(head_y) + 2),
                       int(head_size // 2))

    # Main head
    pygame.draw.circle(screen, JERRY_BROWN,
                       (int(head_x), int(head_y)),
                       int(head_size // 2))

    # Large round ears (Jerry's trademark)
    ear_size = head_size * 0.8
    for ear_offset in [-1, 1]:
        # Ear shadow
        pygame.draw.circle(screen, (160, 140, 100),
                           (int(head_x + ear_offset * ear_size // 2) + 2,
                            int(head_y - ear_size // 2) + 2),
                           int(ear_size // 2))
        # Main ear
        pygame.draw.circle(screen, JERRY_BROWN,
                           (int(head_x + ear_offset * ear_size // 2),
                            int(head_y - ear_size // 2)),
                           int(ear_size // 2))
        # Inner ear
        pygame.draw.circle(screen, JERRY_BELLY,
                           (int(head_x + ear_offset * ear_size // 2),
                            int(head_y - ear_size // 2)),
                           int(ear_size // 3))

    # Large cartoon eyes
    eye_offset = head_size // 2.5
    eye_size = head_size // 4
    for eye_x in [head_x - eye_offset // 2, head_x + eye_offset // 2]:
        # White of the eye
        pygame.draw.circle(screen, WHITE,
                           (int(eye_x), int(head_y)),
                           int(eye_size))
        # Black outline
        pygame.draw.circle(screen, BLACK,
                           (int(eye_x), int(head_y)),
                           int(eye_size), 1)
        # Pupil (slightly larger)
        pygame.draw.circle(screen, BLACK,
                           (int(eye_x), int(head_y)),
                           int(eye_size // 2))
        # Eye highlight
        pygame.draw.circle(screen, WHITE,
                           (int(eye_x - eye_size // 4),
                            int(head_y - eye_size // 4)),
                           int(eye_size // 4))

    # Nose (round black nose like Jerry's)
    nose_x = head_x + direction[0] * head_size // 2
    nose_y = head_y + direction[1] * head_size // 2
    pygame.draw.circle(screen, BLACK,
                       (int(nose_x), int(nose_y)), 4)

    # Whiskers (longer and more pronounced)
    whisker_length = head_size * 1.2
    whisker_spread = [-4, 0, 4]  # More spread out whiskers
    for whisker_y in whisker_spread:
        # Left whiskers
        start_x = int(nose_x - head_size // 4)
        start_y = int(nose_y + whisker_y)
        end_x = int(start_x - whisker_length)
        end_y = int(start_y + whisker_y * 0.8)
        pygame.draw.line(screen, BLACK,
                         (start_x, start_y),
                         (end_x, end_y),
                         2)
        # Right whiskers
        end_x = int(start_x + whisker_length)
        pygame.draw.line(screen, BLACK,
                         (start_x, start_y),
                         (end_x, end_y),
                         2)


def draw_cheese(x, y, is_goal=False):
    """Draw a simple cheese wedge with 3D effect"""
    size = 15 if is_goal else 10
    points = [
        (x, y - size),  # top
        (x - size, y + size),  # bottom left
        (x + size, y + size),  # bottom right
    ]
    pygame.draw.polygon(screen, CHEESE_COLOR, points)
    # Add holes
    pygame.draw.circle(screen, (200, 160, 0), (int(x), int(y)), 3)


def draw_wall(x, y):
    """Draw a wall block with 3D effect"""
    # Main wall
    pygame.draw.rect(screen, WALL_DARK, (x, y, CELL_SIZE, CELL_SIZE))
    # Top highlight
    pygame.draw.rect(screen, WALL_LIGHT, (x, y, CELL_SIZE, 5))
    # Right shadow
    pygame.draw.rect(screen, BLACK, (x + CELL_SIZE - 5, y, 5, CELL_SIZE))


def randomize_c_positions(maze, num_items=5):
    empty_positions = []
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == " ":
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


def draw_maze():
    for y, row in enumerate(mazes[current_level]):
        for x, cell in enumerate(row):
            pos_x = x * CELL_SIZE
            pos_y = y * CELL_SIZE
            if cell == "#":
                draw_wall(pos_x, pos_y)
            elif cell == "G":
                draw_cheese(pos_x + CELL_SIZE // 2, pos_y + CELL_SIZE // 2, True)
            elif cell == "C":
                draw_cheese(pos_x + CELL_SIZE // 2, pos_y + CELL_SIZE // 2, False)


def is_collision(position):
    x, y = position
    margin = MOUSE_SIZE - 10

    check_points = [
        (x - margin, y - margin),
        (x + margin, y - margin),
        (x - margin, y + margin),
        (x + margin, y + margin)
    ]

    for check_x, check_y in check_points:
        cell_x = int(check_x // CELL_SIZE)
        cell_y = int(check_y // CELL_SIZE)

        if (
            cell_y < 0 or cell_y >= len(mazes[current_level]) or
            cell_x < 0 or cell_x >= len(mazes[current_level][0])
        ):
            print("Collision: Out of bounds")
            return True

        cell = mazes[current_level][cell_y][cell_x]

        if cell == "#":
            return True

    return False


def check_goal(position):
    x, y = position
    cell_x = int(x // CELL_SIZE)
    cell_y = int(y // CELL_SIZE)
    return mazes[current_level][cell_y][cell_x] == "G"


def collect_items(position):
    global score
    x, y = position
    cell_x = int(x // CELL_SIZE)
    cell_y = int(y // CELL_SIZE)

    if mazes[current_level][cell_y][cell_x] == "C":
        row = list(mazes[current_level][cell_y])
        row[cell_x] = " "
        mazes[current_level][cell_y] = "".join(row)
        return True
    return False


def reset_game(level_index=0):
    global mouse_pos, start_ticks, score, speed, current_level, mouse_direction
    mouse_pos = [CELL_SIZE * 3 + CELL_SIZE // 2, CELL_SIZE * 1 + CELL_SIZE // 2]
    mouse_direction = [1, 0]
    start_ticks = pygame.time.get_ticks()
    score = 0
    speed = BASE_SPEED
    current_level = level_index
    mazes[current_level] = randomize_c_positions(mazes[current_level])


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


def main():
    global mouse_pos, score, current_level, mouse_direction

    reset_game()  # Initialize game state

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
        new_pos = mouse_pos.copy()

        if keys[pygame.K_LEFT]:
            new_pos[0] -= SPEED
            mouse_direction = [-1, 0]
        elif keys[pygame.K_RIGHT]:
            new_pos[0] += SPEED
            mouse_direction = [1, 0]
        elif keys[pygame.K_UP]:
            new_pos[1] -= SPEED
            mouse_direction = [0, -1]
        elif keys[pygame.K_DOWN]:
            new_pos[1] += SPEED
            mouse_direction = [0, 1]

        print(f"New position: {new_pos}")

        if not is_collision(new_pos):
            mouse_pos = new_pos
            print(f"Updated position: {mouse_pos}")

        else:
            print("Collision detected, movement blocked")

        if collect_items(mouse_pos):
            score += 1

        if check_goal(mouse_pos):
            current_level += 1
            if current_level >= len(mazes):
                display_end_screen(f"Congratulations! Final score: {score}")
            else:
                reset_game(current_level)

        # Drawing
        screen.fill(WHITE)
        draw_maze()
        draw_mouse(mouse_pos, mouse_direction)

        # UI
        timer_text = font.render(f"Time left: {remaining_time}s", True, RED)

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
