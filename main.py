import pygame
from random import choice
import time

WIDTH, HEIGHT = 800, 600
SCREEN_RES = (WIDTH, HEIGHT)

pygame.init()
screen = pygame.display.set_mode(SCREEN_RES)
screen_name = pygame.display.set_caption("Maze Generation")
clock = pygame.time.Clock()
FPS = 30


class Cell:
    CELL_SIZE = 70  # 35

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.used = False

    def draw_cell(self, is_current):
        x, y = self.x * self.CELL_SIZE, self.y * self.CELL_SIZE
        if is_current:
            pygame.draw.rect(screen, pygame.Color('deeppink3'),
                             (x + 2, y + 2, self.CELL_SIZE - 2, self.CELL_SIZE - 2))
        else:
            pygame.draw.rect(screen, pygame.Color('gray27'), (x, y, self.CELL_SIZE, self.CELL_SIZE))
        self.draw_walls()

    def draw_walls(self):
        x, y = self.x * self.CELL_SIZE, self.y * self.CELL_SIZE
        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color('darkgoldenrod3'),
                             (x, y), (x + self.CELL_SIZE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color('darkgoldenrod3'),
                             (x + self.CELL_SIZE, y), (x + self.CELL_SIZE, y + self.CELL_SIZE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color('darkgoldenrod3'),
                             (x + self.CELL_SIZE, y + self.CELL_SIZE), (x, y + self.CELL_SIZE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color('darkgoldenrod3'),
                             (x, y + self.CELL_SIZE), (x, y), 2)


class Grid:
    collumn_count, row_count = WIDTH // Cell.CELL_SIZE, HEIGHT // Cell.CELL_SIZE

    def __init__(self):
        self.grid_cells = [Cell(col, row) for row in range(self.row_count) for col in range(self.collumn_count)]

    def get_cell(self, x, y):
        get_index = lambda x, y: x + y * self.collumn_count
        if x < 0 or x > self.collumn_count - 1 or y < 0 or y > self.row_count - 1:
            return False
        return self.grid_cells[get_index(x, y)]

    def get_random_cell_neighbor(self, cell):
        neighbors = []
        top = self.get_cell(cell.x, cell.y - 1)
        right = self.get_cell(cell.x + 1, cell.y)
        bottom = self.get_cell(cell.x, cell.y + 1)
        left = self.get_cell(cell.x - 1, cell.y)
        candidates = (top, right, bottom, left)
        for cell in candidates:
            if cell and not cell.used:
                neighbors.append(cell)
        return choice(neighbors) if neighbors else False

    def get_neighbors(self, cell):
        neighbors = []
        if not cell.walls['top']:
            neighbors.append(self.get_cell(cell.x, cell.y - 1))
        if not cell.walls['right']:
            neighbors.append(self.get_cell(cell.x + 1, cell.y))
        if not cell.walls['bottom']:
            neighbors.append(self.get_cell(cell.x, cell.y + 1))
        if not cell.walls['left']:
            neighbors.append(self.get_cell(cell.x - 1, cell.y))
        return neighbors

    def remove_wall(self, current_cell, next_cell):
        delta_x = current_cell.x - next_cell.x
        if delta_x == 1:
            current_cell.walls['left'] = False
            next_cell.walls['right'] = False
        elif delta_x == -1:
            current_cell.walls['right'] = False
            next_cell.walls['left'] = False
        delta_y = current_cell.y - next_cell.y
        if delta_y == 1:
            current_cell.walls['top'] = False
            next_cell.walls['bottom'] = False
        elif delta_y == -1:
            current_cell.walls['bottom'] = False
            next_cell.walls['top'] = False

    def generating_DFS(self, cell, color, prev=None):
        cell.used = True
        cell.draw_cell(True)
        pygame.display.flip()
        cell.draw_cell(False)
        next_cell = self.get_random_cell_neighbor(cell)
        time.sleep(1 / FPS)
        if next_cell:
            colors.append((min(color, 255), 10, 100))
            color += 1
            self.remove_wall(cell, next_cell)
            # We need to remove board in two cells!!! Because that board is in two cells.
            cell.draw_cell(False)
            next_cell.draw_cell(False)
            pygame.draw.rect(screen, colors[-1],
                             (cell.x * Cell.CELL_SIZE + 5, cell.y * Cell.CELL_SIZE + 5,
                              Cell.CELL_SIZE - 10, Cell.CELL_SIZE - 10), border_radius=12)
            pygame.display.flip()
            stack.append(cell)
            self.generating_DFS(next_cell, color, cell)
            cell.draw_cell(False)
        elif stack:
            cell.draw_cell(False)
            self.generating_DFS(stack.pop(), color, cell)

    def DFS_to_solve(self, cell, finish_cell):
        cell.used = True
        cell.draw_cell(True)
        pygame.display.flip()
        if cell == finish_cell:
            return True
        else:
            neighbors = self.get_neighbors(cell)
            for next_cell in neighbors:
                if not next_cell.used:
                    time.sleep(10 / FPS)
                    stack.append(cell)
                    return self.DFS_to_solve(next_cell, finish_cell)
            cell.draw_cell(False)
            return self.DFS_to_solve(stack.pop(), finish_cell)

    def open_maze(self, file_name):
        with open(file_name, "r") as fin:
            matrix = fin.readlines()
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    y, x = i // 2, j // 2
                    cell = self.get_cell(x, y)
                    if matrix[i][j] == 'o':
                        cell.walls['top'] = (matrix[i - 1][j] == 'w')
                        cell.walls['right'] = (matrix[i][j + 1] == 'w')
                        cell.walls['bottom'] = (matrix[i + 1][j] == 'w')
                        cell.walls['left'] = (matrix[i][j - 1] == 'w')

    def save_maze(self, file_name):
        with open("binary_maze.txt", "w") as bin_fout:
            data = ("WIDTH: ", WIDTH, " HEIGHT: ", HEIGHT)
            bin_fout.write(''.join(str(x) for x in data) + '\n')
            for cell in self.grid_cells:
                data = (cell.walls['top'], cell.walls['right'], cell.walls['bottom'], cell.walls['left'])
                bin_fout.write(' '.join(str(int(x)) for x in data) + '\n')
        with open(file_name, "w") as fout:
            current_row = 'X'
            for j in range(self.collumn_count):
                current_row += "wX"
            fout.write(current_row + '\n')
            for i in range(self.row_count):
                current_row_1 = current_row_2 = ""
                for j in range(self.collumn_count):
                    cell = self.get_cell(j, i)
                    if cell.walls['left']:
                        current_row_1 += 'w'
                    else:
                        current_row_1 += 'e'
                    current_row_1 += 'o'
                    current_row_2 += 'X'
                    if cell.walls['bottom']:
                        current_row_2 += 'w'
                    else:
                        current_row_2 += 'e'
                current_row_1 += 'w'
                if j == self.collumn_count - 1:
                    current_row_2 += 'X'
                else:
                    current_row_2 += 'w'
                fout.write(current_row_1 + '\n')
                fout.write(current_row_2 + '\n')
        print("\t\033[33m{}".format("The {} was created successfully.".format(file_name)))

    def write(self):
        # TODO: this file could exist
        self.save_maze("temp.txt")
        with open("temp.txt", "r") as fout:
            lines = fout.readlines()
            for line in lines:
                print('\t' + line, end='')


grid = Grid()
screen.fill(pygame.Color('burlywood3'))
[cell.draw_cell(False) for cell in grid.grid_cells]
pygame.display.flip()

is_running = True
while is_running:
    print("\033[34m{}".format("Do you want to generate maze or to open an existing maze? "
                              "(1 or 2):\n1. generate;\n2. open existing."))
    mode = input()
    grid = Grid()
    screen.fill(pygame.Color('burlywood3'))
    [cell.draw_cell(False) for cell in grid.grid_cells]
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            is_running = False
    if mode == "1":
        # print("Choose a way to create a maze (1 or 2):\n1. DFS;\n2. MST.")
        # method = input()
        start_cell = grid.grid_cells[0]
        # if method == "1":
        stack = []
        color = 40
        colors = [color]
        if not start_cell.used:
            grid.generating_DFS(start_cell, color)
            print("\033[34m{}".format("Do you want to save it at txt file? (Yes or No) "), end='')
            time.sleep(50 / FPS)
            start_cell.draw_cell(False)
            pygame.display.flip()
            to_save = input()
            if to_save == "Yes":
                print("\033[34m{}".format("\tEnter file name: "), end='')
                file_name = input()
                grid.save_maze(file_name)
    else:
        print("\033[34m{}".format("\tEnter file name: "), end='')
        file_name = input()
        grid.open_maze(file_name)
        [cell.draw_cell(False) for cell in grid.grid_cells]
        pygame.display.flip()
    print("\033[34m{}".format("Do you want to write maze at terminal? (Yes or No) "), end='')
    to_write = input()
    if to_write == "Yes":
        grid.write()

    print("\033[34m{}".format("Do you want to solve it? (Yes or No) "), end='')
    to_solve = input()
    if to_solve == "Yes":
        print("Print coords_cell_1 and coords_cell_2:")
        print("x1 = ", end='')
        x1 = int(input())
        print("y1 = ", end='')
        y1 = int(input())
        print("x2 = ", end='')
        x2 = int(input())
        print("y2 = ", end='')
        y2 = int(input())
        first_cell, second_cell = grid.get_cell(x1, y1), grid.get_cell(x2, y2)
        for cell in grid.grid_cells:
            cell.used = False
        stack = []
        grid.DFS_to_solve(first_cell, second_cell)
        pygame.display.flip()
