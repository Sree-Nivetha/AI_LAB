# AI LAB – Search Algorithms

## Introduction

This repository is developed as part of **AI Laboratory coursework** to demonstrate
fundamental **Artificial Intelligence search algorithms** through **interactive games
and visual simulations**.

Instead of limiting the work to theoretical implementations, this lab focuses on
**practical understanding** by allowing users to manually solve problems and then
compare their solutions with **AI-driven search algorithms** such as **Breadth-First
Search (BFS)** and **Depth-First Search (DFS)**.

## Objectives of the AI Lab

- Understand uninformed search algorithms (BFS & DFS)
- Compare optimal and non-optimal search strategies
- Analyze solution path length and efficiency
- Apply AI concepts to real-world problem solving
- Improve learning through visualization and gameplay

## Maze Game – BFS vs DFS

### File: `maze.py`

### Description
An interactive maze-solving game where the **user navigates the maze manually**.
After reaching the goal, the user's solution is compared with paths generated using
**BFS** and **DFS**.

### Features
- Main menu with BFS and DFS selection
- Keyboard-based movement
- Automatically computed BFS and DFS paths
- Comparison of:
  - User path length
  - BFS shortest path length
  - DFS path length
- Win screen with statistics
- Back-to-menu navigation

### 🔹 Controls
| Key | Action |
|----|--------|
| ↑ ↓ ← → | Move player |
| Mouse | Menu & button selection |

###  Algorithm Insight
- **BFS** guarantees the shortest path
- **DFS** explores depth-first and may generate longer paths

## 8-Puzzle Game – Interactive Search Comparison

### File: `number_puzzle.py`

###  Description
A playable **8-Puzzle (sliding tile puzzle)** where the user solves the puzzle manually.
Once solved, the game compares the user’s moves with **BFS** and **DFS** solutions.

###  Features
- Realistic 8-puzzle movement using arrow keys
- Guaranteed solvable shuffling
- Hard mode using deep shuffle
- BFS shortest solution computation
- DFS depth-limited solution
- User vs AI move comparison
- Clean menu and restart options

### 🔹 Controls
| Key | Action |
|----|--------|
| ↑ ↓ ← → | Slide tiles |
| Shuffle | Increase difficulty |

### Algorithm Insight
- **BFS** finds the optimal (minimum moves) solution
- **DFS** explores deeper paths and may not be optimal
- Puzzle shuffling is done using valid moves to ensure solvability

---

## 🛠 Requirements

- Python 3.9 or higher
- Pygame library

Install dependency:
pip install pygame
