from config import *
import pygame

board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def get_board():
    return board    

def full_line_clear():
    global board
    rows_cleared = 0

    # Remove full rows
    new_board = [row for row in board if not all(row)]
    rows_cleared = GRID_HEIGHT - len(new_board)

    # Add empty rows at the top
    empty_rows = [[0 for _ in range(GRID_WIDTH)] for _ in range(rows_cleared)]
    board = empty_rows + new_board 

    print("BOARD AFTER CLEAR:")
    for row in board:
        print(''.join(str(cell)[0] if cell else '.' for cell in row))
    print(f"Total rows: {len(board)}")

    
    return rows_cleared


def draw_board(screen):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                piece_color = TETROMINO_COLORS.get(cell, (100, 100, 100))
                rect = pygame.Rect(
                    x * GRID_SIZE,
                    y * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE
                )
                pygame.draw.rect(screen, piece_color, rect)

def lock_piece(matrix, offset_x, offset_y, shape_key):
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                x = offset_x + col_idx
                y = offset_y + row_idx
                if 0 <= y < GRID_HEIGHT:
                    board[y][x] = shape_key

