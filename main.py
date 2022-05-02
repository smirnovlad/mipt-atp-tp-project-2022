import pygame
import sys
from Question import Question
from Grid import Grid
from Constants import SCREEN_RES, FPS

pygame.init()
screen = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("Maze Generation")
clock = pygame.time.Clock()

grid = Grid(screen)
screen.fill(pygame.Color('burlywood3'))
grid.draw()
pygame.display.flip()

while True:
    message = Question("Choose "
                       "(1 or 2 or 3):\n1. Generate maze;\n2. Open existing maze;\n3. Exit.")
    mode = message.state

    grid = Grid(screen)
    screen.fill(pygame.Color('burlywood3'))
    grid.draw()
    pygame.display.flip()

    if mode == "1":
        grid.generate()
    elif mode == "2":
        grid.open()
    elif mode == "3":
        break

    message = Question("Do you want to solve it? (Yes or No)")
    if message.state == "Yes":
        grid.solve()

    clock.tick(10)

pygame.quit()
