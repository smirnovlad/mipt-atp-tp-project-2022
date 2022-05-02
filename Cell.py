import pygame
from Constants import CELL_SIZE

class Cell:
    def __init__(self, x, y, screen):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.used = False
        self.screen = screen

    def draw_cell(self, is_current):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE
        if is_current:
            pygame.draw.rect(self.screen, pygame.Color('deeppink3'),
                             (x + 2, y + 2, CELL_SIZE - 2, CELL_SIZE - 2))
        else:
            pygame.draw.rect(self.screen, pygame.Color('gray27'), (x, y, CELL_SIZE, CELL_SIZE))
        self.draw_walls()

    def draw_walls(self):
        x, y = self.x * CELL_SIZE, self.y * CELL_SIZE
        if self.walls['top']:
            pygame.draw.line(self.screen, pygame.Color('darkgoldenrod3'),
                             (x, y), (x + CELL_SIZE, y), 2)
        if self.walls['right']:
            pygame.draw.line(self.screen, pygame.Color('darkgoldenrod3'),
                             (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls['bottom']:
            pygame.draw.line(self.screen, pygame.Color('darkgoldenrod3'),
                             (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls['left']:
            pygame.draw.line(self.screen, pygame.Color('darkgoldenrod3'),
                             (x, y + CELL_SIZE), (x, y), 2)
