import itertools
import random
import pygame
import sys

from tetromino import TETROMINOS
from config import *

def collision_check(matrix,offset_x, offset_y):
    
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                x = offset_x + col_idx
                y = offset_y + row_idx
                if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
                    return True
                
    return False

# Validate BACKGROUND_COLOR
if not isinstance(BACKGROUND_COLOR, (tuple, list)) or len(BACKGROUND_COLOR) != 3 or not all(0 <= c <= 255 for c in BACKGROUND_COLOR):
    raise ValueError("BACKGROUND_COLOR must be a tuple or list of three integers between 0 and 255.")

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
    if not TETROMINOS:
        raise ValueError("TETROMINOS is empty. Please define tetromino shapes in the 'tetromino' module.")
    shape_key = random.choice(list(TETROMINOS.keys()))
    shape_rotation = 0
    shape_matrix = TETROMINOS[shape_key][shape_rotation]
    if not shape_matrix or not shape_matrix[0]:
        raise ValueError("Invalid shape_matrix: It is empty or malformed.")
    shape_x = GRID_WIDTH // 2 - len(shape_matrix[0]) // 2
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
                    new_rotation = shape_rotation = (shape_rotation + 1) % len(TETROMINOS[shape_key])
                    new_matrix = TETROMINOS[shape_key][shape_rotation]
                    
                    if not collision_check(shape_matrix, shape_x, shape_y):
                        shape_rotation = new_rotation
                        shape_matrix = new_matrix
                    
        if current_time - last_move_time > MOVE_DELAY:
            if keys[pygame.K_LEFT  ]:
                if not collision_check(shape_matrix, shape_x - 1, shape_y):
                        shape_x -= 1
                        last_move_time = current_time
            elif keys[pygame.K_RIGHT ]:
                if not collision_check(shape_matrix, shape_x + 1, shape_y):
                    shape_x += 1
                    last_move_time = current_time
            elif keys[pygame.K_DOWN  ]:
                if not collision_check(shape_matrix, shape_x, shape_y + 1):
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