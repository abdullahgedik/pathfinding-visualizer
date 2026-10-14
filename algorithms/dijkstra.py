import heapq
from itertools import count

def dijkstra(grid):
    counter = count()
    heap = []
    grid.start.distance = 0
    heapq.heappush(heap, (0, next(counter), grid.start))

    while heap:
        current_distance, _, current = heapq.heappop(heap)

        if current.visited:
            continue

        current.visited = True

        if current is grid.end:
            grid.reconstruct_path(current)
            return

        for neighbor in grid.get_neighbors(current):
            new_distance = current_distance + grid.move_cost(current, neighbor)
            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.came_from = current
                heapq.heappush(heap, (new_distance, next(counter), neighbor))

        yield
