import heapq
from itertools import count


def heuristic(node, end):
    return abs(node.row - end.row) + abs(node.col - end.col)


def astar(grid):
    counter = count()
    heap = []
    grid.start.distance = 0
    heapq.heappush(heap, (heuristic(grid.start, grid.end), next(counter), grid.start))

    while heap:
        _, _, current = heapq.heappop(heap)

        if current.visited:
            continue

        current.visited = True

        if current is grid.end:
            grid.reconstruct_path(current)
            return

        for neighbor in grid.get_neighbors(current):
            new_distance = current.distance + 1
            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.came_from = current
                priority = new_distance + heuristic(neighbor, grid.end)
                heapq.heappush(heap, (priority, next(counter), neighbor))

        yield
