import itertools
import random
import pygame
import sys

try:
    from tetromino import TETROMINOS
    if not isinstance(TETROMINOS, dict) or not TETROMINOS:
        raise ValueError("TETROMINOS must be a non-empty dictionary of tetromino shapes.")
except ImportError as e:
    raise ImportError("Failed to import TETROMINOS from 'tetromino'. Ensure the module exists and is correctly defined.") from e
from config import *

# Fallback for BACKGROUND_COLOR if not defined or improperly imported
try:
    BACKGROUND_COLOR
except NameError:
    BACKGROUND_COLOR = (0, 0, 0)  # Default to black

board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
class Game:
    def __init__(self):
        self.score = 0
        self.font = None

def lock_piece(matrix, offset_x, offset_y):
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                x = offset_x + col_idx
                y = offset_y + row_idx
                if y >= 0:  # Only lock pieces that are above the bottom of the grid
                    board[y][x] = 1

def full_line_clear():
    global board
    new_board = []
    rows_cleared = 0
    
    for row in board:
        if all(row):
            rows_cleared += 1
        else:
            new_board.append(row)
            
    while len(new_board) < GRID_HEIGHT:
        new_board.insert(0, [0 for _ in range(GRID_WIDTH)])
    
    board = new_board
    return rows_cleared

def collision_check(matrix,offset_x, offset_y):
    
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                x = offset_x + col_idx
                y = offset_y + row_idx
                if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
                    return True

                if y >= 0 and board[y][x]:
                    return True

    return False

# Validate BACKGROUND_COLOR
if not isinstance(BACKGROUND_COLOR, (tuple, list)) or len(BACKGROUND_COLOR) != 3 or not all(0 <= c <= 255 for c in BACKGROUND_COLOR):
    raise ValueError("BACKGROUND_COLOR must be a tuple or list of three integers between 0 and 255.")

def draw_grid(screen):
    for x, y in itertools.product(range(GRID_WIDTH), range(GRID_HEIGHT)):
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, GRID_COLOR, rect, 1)


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

def draw_board(screen):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    x * GRID_SIZE,
                    y * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE
                )
                pygame.draw.rect(screen, (100, 100, 100), rect)

def draw_next_tetromino(screen, font, next_tetromino):
    next_shape_key, next_shape_rotation, next_shape_matrix, _, _ = next_tetromino
    preview_x = SCREEN_WIDTH - 6 * GRID_SIZE
    preview_y = 2 * GRID_SIZE
    label = font.render("Next:", True, (255, 255, 255))
    screen.blit(label, (preview_x, preview_y - 30))
    for row_idx, row in enumerate(next_shape_matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    preview_x + col_idx * GRID_SIZE,
                    preview_y + row_idx * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE
                )
                pygame.draw.rect(screen, (200, 200, 200), rect)

def active_tetromino(screen, shape_matrix, shape_x, shape_y):
    for row_idx, row in enumerate(shape_matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (shape_x + col_idx) * GRID_SIZE,
                    (shape_y + row_idx) * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE
                )
                pygame.draw.rect(screen, (255, 255, 255), rect)

def draw_score(screen, game):
    font = game.font
    score = game.score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def spawn_new_tetromino():
    shape_key = random.choice(list(TETROMINOS.keys()))
    shape_rotation = 0
    shape_matrix = TETROMINOS[shape_key][shape_rotation]
    shape_x = GRID_WIDTH // 2 - len(shape_matrix[0]) // 2
    shape_y = 0
    return shape_key, shape_rotation, shape_matrix, shape_x, shape_y

def handle_events(shape_key, shape_rotation, shape_matrix, shape_x, shape_y):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_z]:
                shape_rotation, shape_matrix = handle_rotation(
                    shape_key, shape_rotation, shape_matrix, shape_x, shape_y
                )


def handle_movement_logic(keys, shape_matrix, shape_x, shape_y, last_move_time, current_time, MOVE_DELAY):
    return handle_movement(keys, shape_matrix, shape_x, shape_y, last_move_time, current_time, MOVE_DELAY)


def handle_gravity_logic(shape_matrix, shape_x, shape_y, last_gravity_time, current_time, GRAVITY_DELAY):
    return handle_gravity(shape_matrix, shape_x, shape_y, last_gravity_time, current_time, GRAVITY_DELAY)


def handle_locking_and_clearing(shape_matrix, shape_x, shape_y, game, current_tetromino, next_tetromino):
    lock_piece(shape_matrix, shape_x, shape_y)
    cleared_lines = full_line_clear()
    if cleared_lines:
        game.score += {1: 100, 2: 300, 3: 500, 4: 800}.get(cleared_lines, 1000)

    current_tetromino = next_tetromino
    next_tetromino = spawn_new_tetromino()
    shape_key, shape_rotation, shape_matrix, shape_x, shape_y = current_tetromino

    if collision_check(shape_matrix, shape_x, shape_y):
        print("Game Over")
        pygame.quit()
        sys.exit()

    return current_tetromino, next_tetromino

def redraw_screen(screen, shape_matrix, shape_x, shape_y, game, next_tetromino):
    draw_grid(screen)
    draw_board(screen)
    active_tetromino(screen, shape_matrix, shape_x, shape_y)
    draw_score(screen, game)
    draw_next_tetromino(screen, game.font, next_tetromino)


def main():
    pygame.init()
    pygame.font.init()
    game = Game()
    game.font = pygame.font.SysFont("Arial", 24)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

    redraw_needed = True  # Flag to track if redraw is needed

    while True:
        if redraw_needed:
            screen.fill(BACKGROUND_COLOR)

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        handle_events(shape_key, shape_rotation, shape_matrix, shape_x, shape_y)
        shape_x, shape_y, last_move_time = handle_movement_logic(
            keys, shape_matrix, shape_x, shape_y, last_move_time, current_time, MOVE_DELAY
        )
        shape_y, last_gravity_time, locked = handle_gravity_logic(
            shape_matrix, shape_x, shape_y, last_gravity_time, current_time, GRAVITY_DELAY
        )

        if locked:
            current_tetromino, next_tetromino, shape_key, shape_rotation, shape_matrix, shape_x, shape_y = handle_locking_and_clearing(
                shape_matrix, shape_x, shape_y, game, current_tetromino, next_tetromino
            )

        if redraw_needed:
            redraw_screen(
                screen, shape_matrix, shape_x, shape_y, game, next_tetromino
            )
            redraw_needed = False

        clock.tick(FRAME_RATE)
        pygame.display.flip()
        clock.tick(60)
        


# This is a simple Tetris game skeleton using Pygame.
if __name__ == "__main__":
    main()