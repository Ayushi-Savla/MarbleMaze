import getopt
#torieeimport sys
import glm
import pygame
import pygame.display
from world import World
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


RESOLUTION = 1024, 720
FPS = 60
LEVEL = 1


def game_loop(world):
    clock = pygame.time.Clock()
    last_millis = pygame.time.get_ticks()
    world.sound.play_sound('start')
    world.sound.play_music()

    while True:
        # Delta timing
        millis = pygame.time.get_ticks()
        world.delta = min(max((millis - last_millis) / 1000.0, 0.00000001), 0.1)
        last_millis = millis

        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                return

        # Update world
        world.process()

        # Control FPS
        clock.tick(FPS)


def main():
    pygame.init()
    pygame.display.init()

    # Set up the OpenGL context
    pygame.display.set_mode(RESOLUTION, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Le maze: 3D-Packman - just a bit worse")
    pygame.mouse.set_visible(False)

    # Ensure that the OpenGL context is active
    if not pygame.display.get_surface():
        print("Failed to create a valid OpenGL context!")
        pygame.quit()
        sys.exit(1)

    # Create the world object
    world = World(glm.vec2(RESOLUTION), LEVEL)

    # Start the game loop
    game_loop(world)

    # Clean up resources after the game ends
    world.cleanup()


def get_level_from_cmd(argv):
    level = 0
    try:
        opts, args = getopt.getopt(argv, "l:", ["level="])
    except getopt.GetoptError:
        print('main.py --level <level>\nor \nmain.py -l <level>')
        sys.exit(2)
    for opt, arg in opts:
        if opt not in ("-l", "--level"):
            print('main.py --level <level>\nor \nmain.py -l <level>')
            sys.exit()
        elif opt in ("-l", "--level"):
            try:
                level = int(arg)
            except ValueError:
                print('Level argument must be an integer!')
                sys.exit()
    return level


def choose_level(argv):
    global LEVEL
    got_arg = False
    level = get_level_from_cmd(argv)
    if 3 >= level > 0:
        LEVEL = level
        got_arg = True
    elif not got_arg and (level < 0 or level > 3):
        print('The --level argument should be either 1, 2 or 3')
        sys.exit()
    if not got_arg:
        print('Please choose a level!')
        print('Choose:\n\t1 for Beginner (Noob)\n\t2 for Intermediate\n\t3 for Pro\n\n')
        while True:
            show = False
            val = 0
            try:
                val = int(input('Enter your choice: '))
            except ValueError:
                print('You should choose a number between 1, 2 or 3 inclusive!')
                show = False
            if 3 >= val > 0:
                LEVEL = val
                if val == 3:
                    print('Excellent choice!')
                    break
                break
            if val < 0 or val > 3:
                show = True
            if show:
                print('You should choose either 1, 2 or 3!')


if __name__ == '__main__':
    choose_level(sys.argv[1:])
    print('\nPress Escape to quit!\n')
    main()
    pygame.quit()
    print('You quit the game!')

