# Dynamic Pathfinding Agent 🧭

A GUI-based Dynamic Pathfinding Agent implemented in Python using Tkinter.  
This project demonstrates Informed Search Algorithms (A* and Greedy Best-First Search) in a dynamic grid environment with real-time obstacle spawning and re-planning.

---

## 📌 Project Overview

This application allows users to:

- Define custom grid dimensions (Rows × Columns)
- Generate random obstacle maps with adjustable density
- Manually place/remove obstacles using mouse clicks
- Select between:
  - A* Search
  - Greedy Best-First Search (GBFS)
- Choose heuristic:
  - Manhattan Distance
  - Euclidean Distance
- Enable Dynamic Mode (real-time obstacle spawning)
- View real-time metrics:
  - Nodes Visited
  - Path Cost
  - Execution Time (ms)

The system visually demonstrates algorithm behavior under both static and dynamic conditions.

---

## 🧠 Algorithms Implemented

### 1️⃣ Greedy Best-First Search (GBFS)

**Evaluation Function:**
f(n) = h(n)


- Uses heuristic only
- Fast in simple environments
- Does NOT guarantee optimal path

---

### 2️⃣ A* Search

**Evaluation Function:**

f(n) = g(n) + h(n)


Where:
- g(n) = path cost from start
- h(n) = estimated cost to goal

- Guaranteed optimal (with admissible heuristic)
- More stable in complex environments
- Slightly higher memory usage

---

## 📐 Heuristics

### Manhattan Distance

|x1 - x2| + |y1 - y2|

Best suited for 4-direction grid movement.

### Euclidean Distance

sqrt((x1 - x2)^2 + (y1 - y2)^2)

Represents straight-line distance.

---

## 🖥 GUI Features

- Resizable MS-style window
- Interactive grid editing
- Control panel with:
  - Grid size inputs
  - Algorithm selector
  - Heuristic selector
  - Obstacle density slider
  - Dynamic mode toggle
  - Run / Reset buttons
- Visual representation:
  - Start Node → Purple
  - Goal Node → Green
  - Walls → Black
  - Final Path → Blue

---

## 📊 Dynamic Mode

When enabled:

- Obstacles spawn randomly at each time step.
- If a new obstacle blocks the current path:
  - The algorithm automatically re-plans.
- If the obstacle does not affect the path:
  - No unnecessary recalculation occurs.

This simulates real-world navigation uncertainty.
