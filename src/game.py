import random
import pygame
import itertools

from config import *
from tetromino import TETROMINOS
from board import collision_check, lock_piece, full_line_clear
from ui import draw_grid, draw_score, draw_next_tetromino, active_tetromino

def spawn_new_tetromino():
    shape_key = random.choice(list(TETROMINOS.keys()))
    shape_rotation = 0
    shape_matrix = TETROMINOS[shape_key][shape_rotation]
    shape_x = GRID_WIDTH // 2 - len(shape_matrix[0]) // 2
    shape_y = 0
    return shape_key, shape_rotation, shape_matrix, shape_x, shape_y

def handle_rotation(shape_key, shape_rotation, shape_matrix, shape_x, shape_y):
    new_rotation = (shape_rotation + 1) % len(TETROMINOS[shape_key])
    new_matrix = TETROMINOS[shape_key][new_rotation]
    if not collision_check(new_matrix, shape_x, shape_y):
        return new_rotation, new_matrix
    return shape_rotation, shape_matrix

def handle_movement(keys, shape_matrix, shape_x, shape_y, last_move_time, current_time, MOVE_DELAY):
    moved = False
    if current_time - last_move_time > MOVE_DELAY:
        if keys[pygame.K_LEFT]:
            if not collision_check(shape_matrix, shape_x - 1, shape_y):
                shape_x -= 1
                moved = True
        elif keys[pygame.K_RIGHT]:
            if not collision_check(shape_matrix, shape_x + 1, shape_y):
                shape_x += 1
                moved = True
        elif keys[pygame.K_DOWN]:
            if not collision_check(shape_matrix, shape_x, shape_y + 1):
                shape_y += 1
                moved = True
    if moved:
        last_move_time = current_time
    return shape_x, shape_y, last_move_time

def handle_gravity(shape_matrix, shape_x, shape_y, last_gravity_time, current_time, GRAVITY_DELAY):
    if current_time - last_gravity_time > GRAVITY_DELAY:
        if not collision_check(shape_matrix, shape_x, shape_y + 1):
            shape_y += 1
            locked = False
        else:
            locked = True
        last_gravity_time = current_time
    else:
        locked = False
    return shape_y, last_gravity_time, locked