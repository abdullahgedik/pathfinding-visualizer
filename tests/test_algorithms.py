import pytest
from grid import Grid
from algorithms.bfs import bfs
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar
from algorithms.greedy import greedy
from algorithms.dfs import dfs

ALGORITHMS = [bfs, dijkstra, astar, greedy, dfs]


def run_to_completion(generator):
    for _ in generator:
        pass


def make_open_grid():
    grid = Grid(5, 5, 20)
    grid.start = grid.nodes[0][0]
    grid.start.state = "start"
    grid.end = grid.nodes[4][4]
    grid.end.state = "end"
    return grid


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_finds_a_path_on_an_open_grid(algorithm):
    grid = make_open_grid()

    run_to_completion(algorithm(grid))

    assert grid.end.came_from is not None


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_reports_no_path_when_fully_blocked(algorithm):
    grid = make_open_grid()
    for col in range(5):
        grid.nodes[2][col].state = "wall"

    run_to_completion(algorithm(grid))

    assert grid.end.came_from is None


def test_bfs_and_dijkstra_find_equal_length_paths_on_open_grid():
    grid_a = make_open_grid()
    run_to_completion(bfs(grid_a))
    bfs_length = sum(1 for row in grid_a.nodes for node in row if node.on_path)

    grid_b = make_open_grid()
    run_to_completion(dijkstra(grid_b))
    dijkstra_length = sum(1 for row in grid_b.nodes for node in row if node.on_path)

    assert bfs_length == dijkstra_length


def test_dijkstra_routes_around_expensive_terrain():
    grid = make_open_grid()
    for row in range(5):
        grid.nodes[row][2].state = "heavy"
        grid.nodes[row][2].weight = 20
    grid.nodes[0][2].state = "empty"
    grid.nodes[0][2].weight = 1

    run_to_completion(dijkstra(grid))

    path_nodes = [node for row in grid.nodes for node in row if node.on_path]
    assert all(node.weight == 1 for node in path_nodes)
