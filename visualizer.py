import pygame
import math
from queue import PriorityQueue
from collections import deque

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)

class Square:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows


    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = BLUE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = GREY

    def draw(self, win):
        if self.color == BLUE:
            pygame.draw.circle(win, self.color, (self.x + self.width/2, self.y+ self.width/2), 8)
        elif self.color == PURPLE:
            pygame.draw.circle(win, self.color, (self.x + self.width/2, self.y+ self.width/2), 8)
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])



class Algorithm:
    def __init__(self):
        pass

    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)


    def reconstruct_path(self, came_from, current, draw, start):
        while current in came_from:
            current = came_from[current]
            if current == start:
                continue
            current.make_path()
            draw()



    def algorithm(self, draw, grid, start, end, alg):
        if alg: # if true, it will use a star algortihm, else it uses bfs
            count = 0
            open_set = PriorityQueue()
            open_set.put((0, count, start))
            came_from = {}
            g_score = {square: float("inf") for row in grid for square in row}
            g_score[start] = 0
            f_score = {square: float("inf") for row in grid for square in row}
            f_score[start] = self.h(start.get_pos(), end.get_pos())

            open_set_hash = {start}

            while not open_set.empty():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                current = open_set.get()[2]
                open_set_hash.remove(current)

                if current == end:
                    self.reconstruct_path(came_from, end, draw, start)
                    end.make_end()
                    return True


                for neighbor in current.neighbors:
                    temp_g_score = g_score[current] + 1

                    if temp_g_score < g_score[neighbor]:
                        g_score[neighbor] = temp_g_score
                        came_from[neighbor] = current
                        f_score[neighbor] = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())
                        if neighbor not in open_set_hash:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            open_set_hash.add(neighbor)
                            neighbor.make_open()

                if current != start:
                    current.make_closed()

                draw()
        else:
            queue1 = deque()
            queue1.append(start)
            came_from2 = {}
            visited_node = {start}

            while len(queue1) > 0:
                current_node = queue1.popleft()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                if current_node == end:
                    self.reconstruct_path(came_from2, end, draw, start)

                    end.make_end()
                    return True

                for neighbor2 in current_node.neighbors:
                    if neighbor2 not in visited_node:
                        visited_node.add(neighbor2)
                        queue1.append(neighbor2)
                        neighbor2.make_open()
                        came_from2[neighbor2] = current_node
                        if neighbor2 == end:
                            self.reconstruct_path(came_from2, end, draw, start)
                            end.make_end()
                            return True

                if current_node != start:
                    current_node.make_closed()

                draw()


        return False


    def make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                square = Square(i, j, gap, rows)
                grid[i].append(square)

        return grid


    def draw_grid(self, win, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


    def draw(self, win, grid, rows, width):
        win.fill(WHITE)

        for row in grid:
            for square in row:
                square.draw(win)

        self.draw_grid(win, rows, width)
        pygame.display.update()


    def get_clicked_pos(self, pos, rows, width):
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col


    def main(self, win, width, alg):
        ROWS = 50
        grid = self.make_grid(ROWS, width)

        start = None
        end = None

        run = True
        while run:
            self.draw(win, grid, ROWS, width)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if pygame.mouse.get_pressed()[0]: # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos, ROWS, width)
                    square = grid[row][col]
                    if not start and square != end:
                        start = square
                        start.make_start()

                    elif not end and square != start:
                        end = square
                        end.make_end()

                    elif square != end and square != start:
                        square.make_barrier()

                elif pygame.mouse.get_pressed()[2]: # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos, ROWS, width)
                    square = grid[row][col]
                    square.reset()
                    if square == start:
                        start = None
                    elif square == end:
                        end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        return False
                    if event.key == pygame.K_SPACE and start and end:
                        for row in grid:
                            for square in row:
                                square.update_neighbors(grid)

                        path_found = self.algorithm(lambda: self.draw(win, grid, ROWS, width), grid, start, end, alg)

                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = self.make_grid(ROWS, width)

                    if event.key == pygame.K_BACKSPACE:
                        return False

        pygame.quit()


