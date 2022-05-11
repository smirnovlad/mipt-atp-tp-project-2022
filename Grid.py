import pygame
import time
from Cell import Cell
from random import choice
from Constants import WIDTH, HEIGHT, FPS, CELL_SIZE
from Button import Question, Report
import os.path

class Grid:
    collumn_count, row_count = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

    def __init__(self, screen):
        self.grid_cells = [Cell(col, row, screen) for row in range(self.row_count) for col in range(self.collumn_count)]
        self.screen = screen

    def draw(self):
        [cell.draw_cell(False) for cell in self.grid_cells]

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
            if cell and not cell.is_used:
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

    def generate(self):
        start_cell = self.grid_cells[0]
        stack = []
        color = 40
        colors = [color]
        if not start_cell.is_used:
            self.generating_dfs(start_cell, color, stack, colors)
            time.sleep(50 / FPS)
            start_cell.draw_cell(False)
            pygame.display.flip()
            message = Question("Do you want to save it at txt file? (Yes or No)")
            if message.state == "Yes":
                message = Question("Enter file name: ")
                file_name = message.state
                self.save_maze(file_name)
            elif message.state != "No":
                message = Report("Wrong input.")

    def generating_dfs(self, cell, color, stack, colors):
        cell.is_used = True
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
            pygame.draw.rect(self.screen, colors[-1],
                             (cell.x * CELL_SIZE + 5, cell.y * CELL_SIZE + 5,
                              CELL_SIZE - 10, CELL_SIZE - 10), border_radius=12)
            pygame.display.flip()
            stack.append(cell)
            self.generating_dfs(next_cell, color, stack, colors)
            cell.draw_cell(False)
        elif stack:
            cell.draw_cell(False)
            self.generating_dfs(stack.pop(), color, stack, colors)

    def solve(self):
        message = Report("Click on the first cell")
        first_cell = None
        while not first_cell:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    first_cell = pygame.mouse.get_pos()
                    break
        x1 = first_cell[0] - (first_cell[0] % CELL_SIZE)
        y1 = first_cell[1] - (first_cell[1] % CELL_SIZE)
        first_cell = self.get_cell(x1 // CELL_SIZE, y1 // CELL_SIZE)
        
        message = Report("Click on the second cell")
        second_cell = None
        while not second_cell:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    second_cell = pygame.mouse.get_pos()
                    break
        x2 = second_cell[0] - (second_cell[0] % CELL_SIZE)
        y2 = second_cell[1] - (second_cell[1] % CELL_SIZE)
        second_cell = self.get_cell(x2 // CELL_SIZE, y2 // CELL_SIZE)
        
        for cell in self.grid_cells:
            cell.is_used = False
        stack = []
        self.dfs_to_solve(first_cell, second_cell, stack)
        pygame.display.flip()

    def dfs_to_solve(self, cell, finish_cell, stack):
        cell.is_used = True
        cell.draw_cell(True)
        pygame.display.flip()
        if cell == finish_cell:
            return True
        else:
            neighbors = self.get_neighbors(cell)
            for next_cell in neighbors:
                if not next_cell.is_used:
                    time.sleep(2 / FPS)  # 10 / FPS
                    stack.append(cell)
                    return self.dfs_to_solve(next_cell, finish_cell, stack)
            cell.draw_cell(False)
            return self.dfs_to_solve(stack.pop(), finish_cell, stack)

    def open(self):
        message = Question("Enter file name: ")
        file_name = message.state
        if(os.path.exists(file_name)):
            self.open_maze(file_name)
            self.draw()
            pygame.display.flip()
        else:
            message = Report("Wrong input. Try again.")
            self.open()

    def open_maze(self, file_name):
        with open(file_name, "r") as fin:
            matrix = fin.readlines()
            b = True
            l = len(matrix[0]) - 1
            for i in range(len(matrix)):
                if len(matrix[i]) - 1 != l:
                    b = False
                    break
            if b:
                for i in range (1, len(matrix), 2):
                    for j in range(1, len(matrix[i]) - 1, 2):
                        if matrix[i][j] != 'o':
                            b = False
                            break
                        else:
                            if ((matrix[i - 1][j] != 'w' and matrix[i - 1][j] != 'e')
                                or (matrix[i][j + 1] != 'w' and matrix[i][j + 1] != 'e')
                                or (matrix[i + 1][j] != 'w' and matrix[i + 1][j] != 'e')
                                or (matrix[i][j - 1] != 'w' and matrix[i][j - 1] != 'e')):
                                b = False
                                break
            if b:
                for i in range(len(matrix)):
                    for j in range(len(matrix[i])):
                        y, x = i // 2, j // 2
                        cell = self.get_cell(x, y)
                        if matrix[i][j] == 'o':
                            cell.walls['top'] = (matrix[i - 1][j] == 'w')
                            cell.walls['right'] = (matrix[i][j + 1] == 'w')
                            cell.walls['bottom'] = (matrix[i + 1][j] == 'w')
                            cell.walls['left'] = (matrix[i][j - 1] == 'w')
            else:
                message = Report("Wrong input data in file. Try again.")
                self.open()

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
