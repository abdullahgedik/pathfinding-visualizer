import pytest
from grid import Grid


def test_save_and_load_round_trip(tmp_path):
    grid = Grid(5, 5, 20)
    grid.handle_left_click(grid.nodes[0][0])
    grid.handle_left_click(grid.nodes[4][4])
    grid.handle_left_click(grid.nodes[2][2])
    grid.handle_left_click(grid.nodes[1][1], paint_mode="heavy")
    grid.diagonal_enabled = True

    path = tmp_path / "layout.json"
    grid.save_to_file(path)

    loaded = Grid(5, 5, 20)
    loaded.load_from_file(path)

    assert loaded.start is loaded.nodes[0][0]
    assert loaded.end is loaded.nodes[4][4]
    assert loaded.nodes[2][2].state == "wall"
    assert loaded.nodes[1][1].state == "heavy"
    assert loaded.nodes[1][1].weight == grid.nodes[1][1].weight
    assert loaded.diagonal_enabled is True


def test_load_rejects_mismatched_dimensions(tmp_path):
    grid = Grid(5, 5, 20)
    path = tmp_path / "layout.json"
    grid.save_to_file(path)

    mismatched = Grid(6, 6, 20)
    with pytest.raises(ValueError):
        mismatched.load_from_file(path)


def test_grids_cloned_via_dict_are_independent():
    original = Grid(5, 5, 20)
    original.handle_left_click(original.nodes[0][0])
    original.handle_left_click(original.nodes[4][4])
    layout = original.to_dict()

    clone_a = Grid(5, 5, 20)
    clone_a.load_from_dict(layout)
    clone_b = Grid(5, 5, 20)
    clone_b.load_from_dict(layout)

    clone_a.nodes[2][2].visited = True

    assert clone_a.nodes[2][2] is not clone_b.nodes[2][2]
    assert clone_b.nodes[2][2].visited is False
