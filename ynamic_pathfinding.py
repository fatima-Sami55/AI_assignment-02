import pygame
import random
import math
import time
from queue import PriorityQueue

# ---------------- SETTINGS ----------------
WIDTH = 800
HEIGHT = 800
ROWS = 25
SPAWN_PROBABILITY = 0.03  # Dynamic obstacle probability
OBSTACLE_DENSITY = 0.3
# ------------------------------------------

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamic Pathfinding Agent")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# ------------------------------------------
class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = PURPLE

    def make_path(self):
        self.color = GREEN

    def make_open(self):
        self.color = YELLOW

    def make_closed(self):
        self.color = RED

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color,
                         (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        for d in directions:
            r = self.row + d[0]
            c = self.col + d[1]
            if 0 <= r < ROWS and 0 <= c < ROWS:
                if not grid[r][c].is_barrier():
                    self.neighbors.append(grid[r][c])


# ---------------- HEURISTICS ----------------
def manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def euclidean(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


# ---------------- ALGORITHMS ----------------
def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        current = came_from[current]
        current.make_path()
        path.append(current)
    return path


def search(draw, grid, start, end, heuristic, mode="astar"):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    nodes_visited = 0
    start_time = time.time()

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)
        nodes_visited += 1

        if current == end:
            total_time = (time.time() - start_time) * 1000
            path = reconstruct_path(came_from, end)
            return True, nodes_visited, len(path), total_time

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1

            if mode == "gbfs":
                temp_g = 0

            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + heuristic(
                    neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False, nodes_visited, 0, 0


# ---------------- GRID ----------------
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def random_obstacles(grid, density):
    for row in grid:
        for node in row:
            if random.random() < density:
                node.make_barrier()


# ---------------- MAIN ----------------
def main(win, width):
    grid = make_grid(ROWS, width)
    start = grid[0][0]
    end = grid[ROWS-1][ROWS-1]
    start.make_start()
    end.make_end()

    random_obstacles(grid, OBSTACLE_DENSITY)

    heuristic = manhattan
    mode = "astar"

    run = True
    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "astar"
                if event.key == pygame.K_2:
                    mode = "gbfs"
                if event.key == pygame.K_m:
                    heuristic = manhattan
                if event.key == pygame.K_e:
                    heuristic = euclidean
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    result = search(lambda: draw(win, grid, ROWS, width),
                                    grid, start, end, heuristic, mode)

                    print("Nodes Visited:", result[1])
                    print("Path Cost:", result[2])
                    print("Execution Time (ms):", result[3])

                if event.key == pygame.K_r:
                    grid = make_grid(ROWS, width)
                    start = grid[0][0]
                    end = grid[ROWS-1][ROWS-1]
                    start.make_start()
                    end.make_end()
                    random_obstacles(grid, OBSTACLE_DENSITY)

    pygame.quit()


main(WIN, WIDTH)