from collections import deque


def bfs(grid):
    queue = deque()
    queue.append(grid.start)
    grid.start.visited = True

    while queue:
        current = queue.popleft()

        if current is grid.end:
            grid.reconstruct_path(current)
            return

        for neighbor in grid.get_neighbors(current):
            if not neighbor.visited:
                neighbor.visited = True
                neighbor.came_from = current
                queue.append(neighbor)

        yield
