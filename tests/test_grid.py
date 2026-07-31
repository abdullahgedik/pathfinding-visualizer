from grid import Grid


def make_grid(rows=5, cols=5):
    return Grid(rows, cols, 20)


def test_get_neighbors_respects_bounds_and_walls():
    grid = make_grid()
    center = grid.nodes[2][2]
    grid.nodes[1][2].state = "wall"

    neighbors = grid.get_neighbors(center)

    assert grid.nodes[1][2] not in neighbors
    assert grid.nodes[3][2] in neighbors
    assert grid.nodes[2][1] in neighbors
    assert grid.nodes[2][3] in neighbors
    assert len(neighbors) == 3


def test_corner_node_has_fewer_neighbors():
    grid = make_grid()
    corner = grid.nodes[0][0]

    neighbors = grid.get_neighbors(corner)

    assert len(neighbors) == 2


def test_get_neighbors_includes_diagonals_when_enabled():
    grid = make_grid()
    grid.diagonal_enabled = True
    center = grid.nodes[2][2]

    neighbors = grid.get_neighbors(center)

    assert len(neighbors) == 8


def test_get_line_nodes_covers_every_cell_between_two_points():
    grid = make_grid()
    start = grid.nodes[0][0]
    end = grid.nodes[0][4]

    line = grid.get_line_nodes(start, end)

    assert [node.col for node in line] == [0, 1, 2, 3, 4]


def test_handle_left_click_sets_start_then_end_then_walls():
    grid = make_grid()
    a, b, c = grid.nodes[0][0], grid.nodes[0][1], grid.nodes[0][2]

    grid.handle_left_click(a)
    grid.handle_left_click(b)
    grid.handle_left_click(c)

    assert grid.start is a and a.state == "start"
    assert grid.end is b and b.state == "end"
    assert c.state == "wall"


def test_handle_left_click_light_terrain_sets_weight():
    grid = make_grid()
    grid.handle_left_click(grid.nodes[0][0])
    grid.handle_left_click(grid.nodes[0][1])
    node = grid.nodes[1][1]

    grid.handle_left_click(node, paint_mode="light")

    assert node.state == "light"
    assert node.weight > 1


def test_handle_left_click_heavy_terrain_costs_more_than_light():
    grid = make_grid()
    grid.handle_left_click(grid.nodes[0][0])
    grid.handle_left_click(grid.nodes[0][1])
    light_node = grid.nodes[1][1]
    heavy_node = grid.nodes[1][2]

    grid.handle_left_click(light_node, paint_mode="light")
    grid.handle_left_click(heavy_node, paint_mode="heavy")

    assert heavy_node.state == "heavy"
    assert heavy_node.weight > light_node.weight


def test_handle_right_click_erases_and_clears_start():
    grid = make_grid()
    node = grid.nodes[0][0]
    grid.handle_left_click(node)

    grid.handle_right_click(node)

    assert grid.start is None
    assert node.state == "empty"
