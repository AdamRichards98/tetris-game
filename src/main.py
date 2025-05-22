import itertools
import random
import pygame
import sys

from tetromino import TETROMINOS
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

    # Pick a random tetromino
    shape_key = random.choice(list(TETROMINOS.keys()))
    shape_rotation = 0
    shape_matrix = TETROMINOS[shape_key][shape_rotation]

    # Position of the shape (in grid units)
    shape_x = GRID_WIDTH // 2 - len(shape_matrix[0]) // 2
    shape_y = 0

    MOVE_DELAY = 150  # milliseconds
    last_move_time = pygame.time.get_ticks()  # Get the current time

    while True:
        
        screen.fill(BACKGROUND_COLOR) # Fill the screen with the background color
        
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_z]:
                    # Rotate the shape
                    shape_rotation = (shape_rotation + 1) % len(TETROMINOS[shape_key])
                    shape_matrix = TETROMINOS[shape_key][shape_rotation]
                    
        if current_time - last_move_time > MOVE_DELAY:
            if keys[pygame.K_LEFT  ]:
                shape_x -= 1
                last_move_time = current_time
            elif keys[pygame.K_RIGHT ]:
                shape_x += 1
                last_move_time = current_time
            elif keys[pygame.K_DOWN  ]:
                shape_y += 1
                last_move_time = current_time
                    
                
                

        draw_grid(screen) # Draw the grid
        
        # Draw active tetromino
        for row_idx, row in enumerate(shape_matrix):
            for col_idx, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (shape_x + col_idx) * GRID_SIZE,
                        (shape_y + row_idx) * GRID_SIZE,
                        GRID_SIZE, GRID_SIZE
                    )
                    pygame.draw.rect(screen, (255, 255, 255), rect)  # White block

        
        pygame.display.flip()
        clock.tick(60)
        


# This is a simple Tetris game skeleton using Pygame.
if __name__ == "__main__":
    main()