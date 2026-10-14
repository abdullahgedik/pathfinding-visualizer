from grid import Grid
from algorithms.maze import generate_maze


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


def test_maze_generation_wipes_previous_terrain_and_search_results():
    grid = Grid(7, 7, 20)
    grid.handle_left_click(grid.nodes[0][0])
    grid.handle_left_click(grid.nodes[6][6])
    grid.handle_left_click(grid.nodes[2][2], paint_mode="heavy")
    grid.nodes[3][3].on_path = True

    run_to_completion(generate_maze(grid))

    assert grid.start is None and grid.end is None
    assert all(node.weight == 1 for row in grid.nodes for node in row)
    assert not any(node.on_path for row in grid.nodes for node in row)
