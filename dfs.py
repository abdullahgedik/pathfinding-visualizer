def dfs(grid):
    stack = [grid.start]
    grid.start.visited = True

    while stack:
        current = stack.pop()

        if current is grid.end:
            grid.reconstruct_path(current)
            return

        for neighbor in grid.get_neighbors(current):
            if not neighbor.visited:
                neighbor.visited = True
                neighbor.came_from = current
                stack.append(neighbor)

        yield
