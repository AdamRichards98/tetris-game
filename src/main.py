import pygame
import sys

def main():
    pygame.init() # Initialize Pygame
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock() # Create a clock object to control the frame rate

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)

# This is a simple Tetris game skeleton using Pygame.
if __name__ == "__main__":
    main()