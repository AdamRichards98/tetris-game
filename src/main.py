import itertools
import pygame
import sys
from config import *

def draw_grid(screen):
    for x, y in itertools.product(range(GRID_WIDTH), range(GRID_HEIGHT)):
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, GRID_COLOR, rect, 1)


def main():
    pygame.init() # Initialize Pygame
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock() # Create a clock object to control the frame rate

    while True:
        
        screen.fill(BACKGROUND_COLOR) # Fill the screen with the background color
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_grid(screen) # Draw the grid
        pygame.display.flip()
        clock.tick(60)

# This is a simple Tetris game skeleton using Pygame.
if __name__ == "__main__":
    main()