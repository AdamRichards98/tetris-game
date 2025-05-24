import pygame

from config import GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, BACKGROUND_COLOR, GRID_COLOR

board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def get_board():
    return board

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

def lock_piece(matrix, offset_x, offset_y):
    for row_idx, row in enumerate(matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                x = offset_x + col_idx
                y = offset_y + row_idx
                if y >= 0:  # Only lock pieces that are above the bottom of the grid
                    board[y][x] = 1