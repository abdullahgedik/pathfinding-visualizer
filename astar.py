import heapq
from itertools import count


def heuristic(node, end, diagonal=False):
    d_row = abs(node.row - end.row)
    d_col = abs(node.col - end.col)
    if diagonal:
        return max(d_row, d_col)
    return d_row + d_col


def astar(grid):
    counter = count()
    heap = []
    grid.start.distance = 0
    heapq.heappush(heap, (heuristic(grid.start, grid.end, grid.diagonal_enabled), next(counter), grid.start))

    while heap:
        _, _, current = heapq.heappop(heap)

        if current.visited:
            continue

        current.visited = True

        if current is grid.end:
            grid.reconstruct_path(current)
            return

        for neighbor in grid.get_neighbors(current):
            new_distance = current.distance + neighbor.weight
            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.came_from = current
                priority = new_distance + heuristic(neighbor, grid.end, grid.diagonal_enabled)
                heapq.heappush(heap, (priority, next(counter), neighbor))

        yield
