from config import *
import pygame

board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def get_board():
    return board    

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
                if y >= 0:
                    board[y][x] = shape_key