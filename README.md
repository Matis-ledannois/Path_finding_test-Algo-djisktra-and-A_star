# 🧭 Pathfinding Visualizer – Dijkstra & A*

Interactive visualization of pathfinding algorithms built with **Python and Pygame**.

This project demonstrates how **Dijkstra** and **A\*** algorithms explore a grid to find the shortest path between two points while avoiding obstacles.

---
<img width="993" height="826" alt="Capture d&#39;écran 2026-02-15 140622" src="https://github.com/user-attachments/assets/e2eed027-dc0b-4e01-8b08-6e5edb71dc9c" />

## 🎯 Project Overview

This application allows you to:

- Visualize **Dijkstra’s Algorithm**
- Visualize **A\* (A Star) Algorithm**
- Generate random obstacle maps
- Compare exploration behaviors
- Observe shortest path reconstruction in real time

The goal is educational: understand how graph search algorithms work internally.

---

## 🛠️ Technologies Used

- **Python 3**
- **Pygame**
- Object-Oriented Programming
- Algorithmic Optimization Concepts
- Euclidean Heuristic (for A*)

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Matis-ledannois/pathfinding-visualizer.git
cd pathfinding-visualizer
```

### 2️⃣ Install dependencies

```bash
pip install pygame
```

### 3️⃣ Run the program

```bash
python pathfinding_python_Choix_coordonnées_algo_djikstra_A_star.py
```

---

## 🎮 Controls

| Key | Action |
|------|--------|
| `i` | Reset current algorithm |
| `n` | Generate a new random map |
| `s` | Switch between Dijkstra and A* |

---

## 🧠 Algorithms Implemented

### 🔵 Dijkstra

- Explores uniformly in all directions
- Guarantees shortest path
- No heuristic guidance
- Slower on large grids

### 🔴 A\* (A Star)

- Uses Euclidean distance heuristic
- Directed exploration toward goal
- Faster than Dijkstra in most cases
- Still guarantees optimal path (with admissible heuristic)

---

## 🗺️ Grid System

- Grid size: **50 x 40**
- Cell size: **20px**
- Random obstacle generation
- 8-direction movement allowed
- Diagonal cost slightly higher (1.5 vs 1)

---

## 🎨 Visual Legend

| Color | Meaning |
|--------|----------|
| 🔵 Blue | Start (D) |
| 🔴 Red | Goal (F) |
| ⚪ White | Wall |
| 🟡 Yellow | Final shortest path |
| 🔴 Small Red Squares | Explored nodes |

---

## 💡 What This Project Demonstrates

- Graph traversal algorithms
- Priority selection logic
- Heuristic optimization
- Path reconstruction via predecessors
- Real-time rendering loop with Pygame
- Clean object-oriented architecture

---

## 📚 Educational Purpose

This project is ideal for:

- Algorithm learning
- Computer science students
- Robotics & AI beginners
- Path planning fundamentals
- Comparing uninformed vs informed search

---

## 🚀 Possible Improvements

- Add BFS and DFS comparison
- Add adjustable grid size
- Add mouse-drawn obstacles
- Add performance metrics (execution time, nodes visited)
- Add weighted terrain
- Implement visualization speed control
- Add UI panel for algorithm statistics

---

## 🏷️ License

This project is open-source and intended for educational purposes.

---

## 👨‍💻 Author

Matis Ledannois  
Robotics & Software Engineering Student  
Passionate about AI, Algorithms, and Intelligent Systems
