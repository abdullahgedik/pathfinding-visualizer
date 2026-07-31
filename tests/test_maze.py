from grid import Grid
from maze import generate_maze


def run_to_completion(generator):
    for _ in generator:
        pass


def test_maze_generation_only_produces_wall_and_empty_states():
    grid = Grid(7, 7, 20)

    run_to_completion(generate_maze(grid))

    states = {node.state for row in grid.nodes for node in row}
    assert states <= {"wall", "empty"}


def test_maze_generation_resets_visited_flag_when_done():
    grid = Grid(7, 7, 20)

    run_to_completion(generate_maze(grid))

    assert all(not node.visited for row in grid.nodes for node in row)
