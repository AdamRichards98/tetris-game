import itertools
import pygame

from config import *

def draw_grid(screen):
    for x, y in itertools.product(range(GRID_WIDTH), range(GRID_HEIGHT)):
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, GRID_COLOR, rect, 1)
        
def draw_next_tetromino(screen, font, next_shape_matrix):
    sidebar_x = SCREEN_WIDTH + 20
    preview_y = 120
    label = font.render("Next:", True, (255, 255, 255))
    screen.blit(label, (sidebar_x, preview_y - 30))

    for row_idx, row in enumerate(next_shape_matrix):
        for col_idx, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    sidebar_x + col_idx * GRID_SIZE,
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

def draw_score(screen, font, score):
    sidebar_x = SCREEN_WIDTH + 20
    screen.blit(font.render("Score:", True, (255, 255, 255)), (sidebar_x, 30))
    screen.blit(font.render(str(score), True, (255, 255, 255)), (sidebar_x, 60))
                
