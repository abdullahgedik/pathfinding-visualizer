import random


def generate_maze(grid):
    for row in grid.nodes:
        for node in row:
            node.state = "wall"
            node.visited = False

    start_cell = grid.nodes[0][0]
    start_cell.state = "empty"
    start_cell.visited = True
    stack = [start_cell]

    while stack:
        current = stack[-1]
        neighbors = grid.get_maze_neighbors(current)

        if neighbors:
            next_cell, wall_cell = random.choice(neighbors)
            wall_cell.state = "empty"
            next_cell.state = "empty"
            next_cell.visited = True
            stack.append(next_cell)
        else:
            stack.pop()

        yield

    for row in grid.nodes:
        for node in row:
            node.visited = False
