import heapq
from itertools import count
from astar import heuristic


def greedy(grid):
    counter = count()
    heap = []
    grid.start.visited = True
    heapq.heappush(heap, (heuristic(grid.start, grid.end, grid.diagonal_enabled), next(counter), grid.start))

    while heap:
        _, _, current = heapq.heappop(heap)

        if current is grid.end:
            grid.reconstruct_path(current)
            return

        for neighbor in grid.get_neighbors(current):
            if not neighbor.visited:
                neighbor.visited = True
                neighbor.came_from = current
                priority = heuristic(neighbor, grid.end, grid.diagonal_enabled)
                heapq.heappush(heap, (priority, next(counter), neighbor))

        yield
