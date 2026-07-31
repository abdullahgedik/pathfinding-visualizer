# Pathfinding Visualizer

An interactive Python/Pygame app that visualizes pathfinding algorithms exploring a grid step by step — watch the search frontier expand in real time, then see the shortest path highlighted once it's found.

## Features

- **5 algorithms**: BFS, Dijkstra, A*, Greedy Best-First, and DFS — run them on the same layout to compare how each one explores and whether it finds the shortest path
- **Step-by-step visualization** with an adjustable speed slider, from a slow crawl to near-instant
- **Maze generation** via randomized recursive backtracking
- **Weighted terrain** — costly cells that Dijkstra/A* route around, but that BFS/DFS/Greedy can't account for (a deliberate way to see the difference)
- **Diagonal movement toggle**
- **Stats readout** — nodes explored and path length after each run

## Controls

| Action | Effect |
|---|---|
| Left-click / drag | Place start, then end, then walls (or weighted terrain in Weight Mode) |
| Right-click / drag | Erase a cell back to empty |
| **Wall Mode / Weight Mode** | Toggle what left-click paints |
| **Diagonal: On/Off** | Allow diagonal moves |
| **Maze** | Generate a random maze (clears the grid first) |
| **Reset** | Clear search results, keep walls/start/end |
| **Clear** | Wipe the entire grid |
| Speed slider | Control how fast the algorithm animates |

## Setup

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Run

```bash
venv\Scripts\python main.py
```

## Tech Stack

- Python 3
- [pygame-ce](https://pyga.me/) for rendering and input
- [pygame_gui](https://pygame-gui.readthedocs.io/) for the UI panel (buttons, slider)
