#src/main.py

import itertools
import random
import pygame
import sys

from tetromino import TETROMINOS
from config import *
from game import (
    handle_rotation, handle_movement, handle_gravity, spawn_new_tetromino
)
from board import (
    draw_board, lock_piece, full_line_clear, collision_check
)
from ui import (
    draw_grid, draw_score, draw_next_tetromino, active_tetromino
)


score = 0
font = None

# Validate BACKGROUND_COLOR
if not isinstance(BACKGROUND_COLOR, (tuple, list)) or len(BACKGROUND_COLOR) != 3 or not all(0 <= c <= 255 for c in BACKGROUND_COLOR):
    raise ValueError("BACKGROUND_COLOR must be a tuple or list of three integers between 0 and 255.")

def main():
    global score, font

    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 24)
    screen = pygame.display.set_mode((SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    if not TETROMINOS:
        raise ValueError("TETROMINOS is empty. Please define tetromino shapes in the 'tetromino' module.")

    current_tetromino = spawn_new_tetromino()
    next_tetromino = spawn_new_tetromino()
    shape_key, shape_rotation, shape_matrix, shape_x, shape_y = current_tetromino


    GRAVITY_DELAY = 800
    last_gravity_time = pygame.time.get_ticks()
    MOVE_DELAY = 150
    last_move_time = pygame.time.get_ticks()

    while True:
        screen.fill(BACKGROUND_COLOR)
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_z]:
                    shape_rotation, shape_matrix = handle_rotation(
                        shape_key, shape_rotation, shape_matrix, shape_x, shape_y
                    )

        shape_x, shape_y, last_move_time = handle_movement(
            keys, shape_matrix, shape_x, shape_y, last_move_time, current_time, MOVE_DELAY
        )

        shape_y, last_gravity_time, locked = handle_gravity(
            shape_matrix, shape_x, shape_y, last_gravity_time, current_time, GRAVITY_DELAY
        )

        if locked:
            
            lock_piece(shape_matrix, shape_x, shape_y)
            if cleared_lines := full_line_clear():
                score += {1: 100, 2: 300, 3: 500, 4: 800}.get(cleared_lines, 1000)
            
            current_tetromino = next_tetromino
            next_tetromino = spawn_new_tetromino()
            
            draw_score(screen, font, score)
            draw_next_tetromino(screen, font, next_tetromino[2])
            
            shape_key, shape_rotation, shape_matrix, shape_x, shape_y = current_tetromino
            
            if collision_check(shape_matrix, shape_x, shape_y):
                print("Game Over")
                pygame.quit()
                sys.exit()

        draw_grid(screen)
        draw_board(screen)
        active_tetromino(screen, shape_matrix, shape_x, shape_y)
        draw_score(screen, font, score)
        draw_next_tetromino(screen, font, next_tetromino[2])

        pygame.display.flip()
        clock.tick(60)
        


# This is a simple Tetris game skeleton using Pygame.
if __name__ == "__main__":
    main()