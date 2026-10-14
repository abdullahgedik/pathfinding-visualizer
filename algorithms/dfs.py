def dfs(grid):
    # Nodes are marked visited when popped, not when pushed, so the search
    # really dives down one branch before backtracking
    stack = [(grid.start, None)]

    while stack:
        current, parent = stack.pop()

        if current.visited:
            continue

        current.visited = True
        current.came_from = parent

        if current is grid.end:
            grid.reconstruct_path(current)
            return

        for neighbor in grid.get_neighbors(current):
            if not neighbor.visited:
                stack.append((neighbor, current))

        yield
