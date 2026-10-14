import random
import pytest
from grid import Grid, TERRAIN_COSTS
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


@pytest.mark.parametrize("algorithm", ALGORITHMS)
@pytest.mark.parametrize("diagonal", [False, True])
def test_path_is_a_chain_of_legal_moves(algorithm, diagonal):
    grid = make_open_grid()
    grid.diagonal_enabled = diagonal
    grid.nodes[1][1].state = "wall"
    grid.nodes[3][2].state = "wall"

    run_to_completion(algorithm(grid))

    path = grid.get_path()
    assert path[0] is grid.start and path[-1] is grid.end
    for from_node, to_node in zip(path, path[1:]):
        assert to_node in grid.get_neighbors(from_node)


def test_dijkstra_uses_diagonal_cost_on_an_open_grid():
    grid = make_open_grid()
    grid.diagonal_enabled = True

    run_to_completion(dijkstra(grid))

    path = grid.get_path()
    assert len(path) == 5
    assert grid.path_cost(path) == pytest.approx(4 * 2 ** 0.5)


@pytest.mark.parametrize("seed", range(20))
@pytest.mark.parametrize("diagonal", [False, True])
def test_astar_finds_the_same_cost_as_dijkstra(seed, diagonal):
    rng = random.Random(seed)
    layout = []
    for _ in range(12):
        layout.append([rng.choice(["empty"] * 5 + ["wall", "light", "heavy"]) for _ in range(12)])

    def build():
        grid = Grid(12, 12, 20)
        grid.diagonal_enabled = diagonal
        for row in range(12):
            for col in range(12):
                state = layout[row][col]
                grid.nodes[row][col].state = state
                grid.nodes[row][col].weight = TERRAIN_COSTS.get(state, 1)
        grid.start, grid.end = grid.nodes[0][0], grid.nodes[11][11]
        for node in (grid.start, grid.end):
            node.state, node.weight = "start" if node is grid.start else "end", 1
        return grid

    dijkstra_grid = build()
    run_to_completion(dijkstra(dijkstra_grid))
    astar_grid = build()
    run_to_completion(astar(astar_grid))

    dijkstra_path = dijkstra_grid.get_path()
    astar_path = astar_grid.get_path()
    assert bool(dijkstra_path) == bool(astar_path)
    if dijkstra_path:
        assert astar_grid.path_cost(astar_path) == pytest.approx(
            dijkstra_grid.path_cost(dijkstra_path)
        )
