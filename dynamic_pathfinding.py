import tkinter as tk
from tkinter import ttk
import math
import random
import time
from queue import PriorityQueue

#NODE CLASS
class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.wall = False
        self.neighbors = []

    def __lt__(self, other):
        return False


#HEURISTICS
def manhattan(a, b):
    return abs(a.row - b.row) + abs(a.col - b.col)

def euclidean(a, b):
    return math.sqrt((a.row - b.row) ** 2 + (a.col - b.col) ** 2)


#MAIN APP
class PathfindingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinding Agent")
        self.root.geometry("1000x800")
        self.root.state("zoomed")  # Maximize on Windows

        self.rows = tk.IntVar(value=25)
        self.cols = tk.IntVar(value=25)
        self.algorithm = tk.StringVar(value="A*")
        self.heuristic = tk.StringVar(value="Manhattan")
        self.density = tk.DoubleVar(value=0.3)
        self.dynamic_mode = tk.BooleanVar(value=False)

        self.setup_ui()

    #UI
    def setup_ui(self):
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side="left", fill="y")

        ttk.Label(control_frame, text="Grid Rows").pack()
        ttk.Entry(control_frame, textvariable=self.rows).pack()

        ttk.Label(control_frame, text="Grid Columns").pack()
        ttk.Entry(control_frame, textvariable=self.cols).pack()

        ttk.Button(control_frame, text="Create Grid",
                   command=self.create_grid).pack(pady=5)

        ttk.Label(control_frame, text="Algorithm").pack()
        ttk.Combobox(control_frame,
                     textvariable=self.algorithm,
                     values=["A*", "Greedy Best First"]).pack()

        ttk.Label(control_frame, text="Heuristic").pack()
        ttk.Combobox(control_frame,
                     textvariable=self.heuristic,
                     values=["Manhattan", "Euclidean"]).pack()

        ttk.Label(control_frame, text="Obstacle Density").pack()
        ttk.Scale(control_frame,
                  from_=0, to=0.6,
                  variable=self.density,
                  orient="horizontal").pack()

        ttk.Button(control_frame, text="Random Maze",
                   command=self.random_maze).pack(pady=5)

        ttk.Checkbutton(control_frame,
                        text="Dynamic Mode",
                        variable=self.dynamic_mode).pack(pady=5)

        ttk.Button(control_frame, text="Run Search",
                   command=self.run_search).pack(pady=5)

        ttk.Button(control_frame, text="Reset",
                   command=self.reset_grid).pack(pady=5)

        # Metrics
        self.metrics = ttk.Label(control_frame, text="Metrics will appear here")
        self.metrics.pack(pady=20)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(side="right", expand=True, fill="both")

    #GRID
    def create_grid(self):
        self.grid = []
        self.canvas.delete("all")

        self.cell_size = min(700 // self.rows.get(),
                             700 // self.cols.get())

        for r in range(self.rows.get()):
            row = []
            for c in range(self.cols.get()):
                row.append(Node(r, c))
            self.grid.append(row)

        self.start = self.grid[0][0]
        self.goal = self.grid[self.rows.get()-1][self.cols.get()-1]

        self.draw_grid()

        self.canvas.bind("<Button-1>", self.place_wall)

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows.get()):
            for c in range(self.cols.get()):
                node = self.grid[r][c]
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "white"
                if node.wall:
                    color = "black"
                if node == self.start:
                    color = "purple"
                if node == self.goal:
                    color = "green"

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="gray")

    def place_wall(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < self.rows.get() and 0 <= col < self.cols.get():
            node = self.grid[row][col]
            if node not in [self.start, self.goal]:
                node.wall = not node.wall
                self.draw_grid()

    def random_maze(self):
        for row in self.grid:
            for node in row:
                if random.random() < self.density.get():
                    if node not in [self.start, self.goal]:
                        node.wall = True
        self.draw_grid()

    def reset_grid(self):
        for row in self.grid:
            for node in row:
                node.wall = False
        self.draw_grid()

    #SEARCH
    def update_neighbors(self):
        for row in self.grid:
            for node in row:
                node.neighbors = []
                for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                    r = node.row + dr
                    c = node.col + dc
                    if 0 <= r < self.rows.get() and 0 <= c < self.cols.get():
                        if not self.grid[r][c].wall:
                            node.neighbors.append(self.grid[r][c])

    def run_search(self):
        self.update_neighbors()

        heuristic_func = manhattan if self.heuristic.get() == "Manhattan" else euclidean
        algorithm = self.algorithm.get()

        start_time = time.time()

        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.start))

        came_from = {}
        g_score = {node: float("inf") for row in self.grid for node in row}
        g_score[self.start] = 0

        nodes_visited = 0

        while not open_set.empty():
            current = open_set.get()[2]

            if current == self.goal:
                break

            nodes_visited += 1

            for neighbor in current.neighbors:
                temp_g = g_score[current] + 1

                if temp_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g

                    if algorithm == "A*":
                        f = temp_g + heuristic_func(neighbor, self.goal)
                    else:
                        f = heuristic_func(neighbor, self.goal)

                    count += 1
                    open_set.put((f, count, neighbor))

        end_time = time.time()

        # Reconstruct path
        cost = 0
        current = self.goal
        while current in came_from:
            current = came_from[current]
            cost += 1
            x1 = current.col * self.cell_size
            y1 = current.row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         fill="blue", outline="gray")

        self.metrics.config(
            text=f"Nodes Visited: {nodes_visited}\n"
                 f"Path Cost: {cost}\n"
                 f"Execution Time: {(end_time-start_time)*1000:.2f} ms"
        )


#RUN
root = tk.Tk()
app = PathfindingApp(root)
root.mainloop()