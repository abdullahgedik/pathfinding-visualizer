import ctypes
import pygame
import pygame_gui
from grid import Grid
from bfs import bfs
from dijkstra import dijkstra
from astar import astar
from greedy import greedy
from dfs import dfs
from maze import generate_maze

SAVE_FILE = "saved_layout.json"

ALGORITHMS = {
    "BFS": bfs,
    "Dijkstra": dijkstra,
    "A*": astar,
    "Greedy": greedy,
    "DFS": dfs,
}

SCALE = 1.3


def s(value):
    return round(value * SCALE)


def compute_stats_text(grid):
    visited_count = sum(1 for row in grid.nodes for node in row if node.visited)
    if grid.end.came_from is not None:
        path_length = (
            sum(1 for row in grid.nodes for node in row if node.on_path) + 2
        )
        return f"Visited: {visited_count}   Path length: {path_length}"
    return f"Visited: {visited_count}   No path found"


def draw_outline(window, rect):
    pygame.draw.rect(window, (50, 50, 50), rect, 3)


ROWS = 30
CELL_SIZE = s(20)
GRID_HEIGHT = CELL_SIZE * ROWS
TOP_BAR_HEIGHT = s(60)
PANEL_HEIGHT = s(50)
COLS = 60
GRID_WIDTH = COLS * CELL_SIZE
WINDOW_WIDTH = GRID_WIDTH
WINDOW_HEIGHT = TOP_BAR_HEIGHT + GRID_HEIGHT + PANEL_HEIGHT


def main():
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer")
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

    grid = Grid(ROWS, COLS, CELL_SIZE)
    algorithm = None

    # Top bar: speed control, editing tools, and side-by-side comparison setup
    speed_font = pygame.font.SysFont("segoeui", s(22), bold=True)
    speed_text = speed_font.render("Speed", True, (0, 0, 0))
    stats_font = pygame.font.SysFont("segoeui", s(17), bold=True)
    stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
    speed_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((s(80), s(15)), (s(280), s(30))),
        start_value=30,
        value_range=(1, 800),
        manager=manager,
    )
    maze_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(370), s(15)), (s(100), s(30))),
        text="Maze",
        manager=manager,
    )
    mode_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(480), s(15)), (s(130), s(30))),
        text="Wall Mode",
        manager=manager,
    )
    diagonal_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(620), s(15)), (s(140), s(30))),
        text="Diagonal: Off",
        manager=manager,
    )
    algorithm_names = list(ALGORITHMS.keys())
    left_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=algorithm_names,
        starting_option="BFS",
        relative_rect=pygame.Rect((s(796), s(15)), (s(120), s(30))),
        manager=manager,
    )
    right_dropdown = pygame_gui.elements.UIDropDownMenu(
        options_list=algorithm_names,
        starting_option="A*",
        relative_rect=pygame.Rect((s(926), s(15)), (s(120), s(30))),
        manager=manager,
    )
    compare_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(1056), s(15)), (s(130), s(30))),
        text="Compare",
        manager=manager,
    )

    # Bottom bar: run an algorithm, or reset/clear/save/load the layout
    bottom_bar_y = TOP_BAR_HEIGHT + GRID_HEIGHT
    bfs_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(10), bottom_bar_y + s(10)), (s(95), s(30))),
        text="BFS",
        manager=manager,
    )
    dijkstra_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(113), bottom_bar_y + s(10)), (s(95), s(30))),
        text="Dijkstra",
        manager=manager,
    )
    astar_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(216), bottom_bar_y + s(10)), (s(95), s(30))),
        text="A*",
        manager=manager,
    )
    greedy_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(319), bottom_bar_y + s(10)), (s(95), s(30))),
        text="Greedy",
        manager=manager,
    )
    dfs_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(422), bottom_bar_y + s(10)), (s(95), s(30))),
        text="DFS",
        manager=manager,
    )
    action_button_width = s(85)
    action_button_gap = s(8)
    action_margin_right = s(15)
    load_x = WINDOW_WIDTH - action_margin_right - action_button_width
    save_x = load_x - action_button_gap - action_button_width
    clear_x = save_x - action_button_gap - action_button_width
    reset_x = clear_x - action_button_gap - action_button_width
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (reset_x, bottom_bar_y + s(10)), (action_button_width, s(30))
        ),
        text="Reset",
        manager=manager,
    )
    clear_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (clear_x, bottom_bar_y + s(10)), (action_button_width, s(30))
        ),
        text="Clear",
        manager=manager,
    )
    save_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (save_x, bottom_bar_y + s(10)), (action_button_width, s(30))
        ),
        text="Save",
        manager=manager,
    )
    load_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (load_x, bottom_bar_y + s(10)), (action_button_width, s(30))
        ),
        text="Load",
        manager=manager,
    )

    running = True
    left_held = False
    right_held = False
    last_paint_node = None
    paint_mode = "wall"
    step_accumulator = 0.0
    is_search_run = False
    compare_mode = False
    left_choice = "BFS"
    right_choice = "A*"
    grid_left = None
    grid_right = None
    algorithm_left = None
    algorithm_right = None
    stats_left_text = None
    stats_right_text = None
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not compare_mode:
                pos = pygame.mouse.get_pos()
                if pos[0] < GRID_WIDTH and TOP_BAR_HEIGHT <= pos[1] < TOP_BAR_HEIGHT + GRID_HEIGHT:
                    node = grid.get_node_from_pos((pos[0], pos[1] - TOP_BAR_HEIGHT))
                    if event.button == 1:
                        left_held = True
                        grid.handle_left_click(node, paint_mode)
                        last_paint_node = node
                    elif event.button == 3:
                        right_held = True
                        grid.handle_right_click(node)
                        last_paint_node = node
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    left_held = False
                elif event.button == 3:
                    right_held = False
            elif event.type == pygame.MOUSEMOTION and not compare_mode:
                if left_held or right_held:
                    pos = pygame.mouse.get_pos()
                    if pos[0] < GRID_WIDTH and TOP_BAR_HEIGHT <= pos[1] < TOP_BAR_HEIGHT + GRID_HEIGHT:
                        node = grid.get_node_from_pos((pos[0], pos[1] - TOP_BAR_HEIGHT))
                        if last_paint_node is not None:
                            line_nodes = grid.get_line_nodes(last_paint_node, node)
                        else:
                            line_nodes = [node]
                        for line_node in line_nodes:
                            if left_held:
                                grid.handle_left_click(line_node, paint_mode)
                            elif right_held:
                                grid.handle_right_click(line_node)
                        last_paint_node = node
            elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element is left_dropdown:
                    left_choice = event.text
                elif event.ui_element is right_dropdown:
                    right_choice = event.text
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if compare_mode:
                    if event.ui_element is compare_button:
                        compare_mode = False
                        compare_button.set_text("Compare")
                elif event.ui_element is bfs_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = bfs(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
                elif event.ui_element is dijkstra_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = dijkstra(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
                elif event.ui_element is astar_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = astar(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
                elif event.ui_element is greedy_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = greedy(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
                elif event.ui_element is dfs_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = dfs(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
                elif event.ui_element is mode_button:
                    if paint_mode == "wall":
                        paint_mode = "light"
                        mode_button.set_text("Light Terrain")
                    elif paint_mode == "light":
                        paint_mode = "heavy"
                        mode_button.set_text("Heavy Terrain")
                    else:
                        paint_mode = "wall"
                        mode_button.set_text("Wall Mode")
                elif event.ui_element is diagonal_button:
                    grid.diagonal_enabled = not grid.diagonal_enabled
                    if grid.diagonal_enabled:
                        diagonal_button.set_text("Diagonal: On")
                    else:
                        diagonal_button.set_text("Diagonal: Off")
                elif event.ui_element is maze_button:
                    algorithm = generate_maze(grid)
                    grid.start = None
                    grid.end = None
                    step_accumulator = 0.0
                    is_search_run = False
                    stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
                elif event.ui_element is reset_button:
                    grid.reset()
                    algorithm = None
                    stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
                elif event.ui_element is clear_button:
                    grid.clear()
                    algorithm = None
                    stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
                elif event.ui_element is save_button:
                    grid.save_to_file(SAVE_FILE)
                elif event.ui_element is load_button:
                    try:
                        grid.load_from_file(SAVE_FILE)
                        algorithm = None
                        is_search_run = False
                        stats_text = stats_font.render("Visited: 0   No path yet", True, (0, 0, 0))
                    except (FileNotFoundError, ValueError) as error:
                        print(f"Could not load layout: {error}")
                elif event.ui_element is compare_button and grid.start and grid.end:
                    half_cell_size = max(1, (GRID_WIDTH // 2) // COLS)
                    layout = grid.to_dict()
                    grid_left = Grid(ROWS, COLS, half_cell_size)
                    grid_left.load_from_dict(layout)
                    grid_right = Grid(ROWS, COLS, half_cell_size)
                    grid_right.load_from_dict(layout)
                    algorithm_left = ALGORITHMS[left_choice](grid_left)
                    algorithm_right = ALGORITHMS[right_choice](grid_right)
                    stats_left_text = None
                    stats_right_text = None
                    algorithm = None
                    step_accumulator = 0.0
                    compare_mode = True
                    compare_button.set_text("Back to Editor")

            manager.process_events(event)

        if compare_mode:
            steps_per_second = speed_slider.get_current_value()
            step_accumulator += steps_per_second * time_delta
            while step_accumulator >= 1:
                step_accumulator -= 1
                if algorithm_left is not None:
                    try:
                        next(algorithm_left)
                    except StopIteration:
                        algorithm_left = None
                        stats_left_text = stats_font.render(
                            compute_stats_text(grid_left), True, (0, 0, 0)
                        )
                if algorithm_right is not None:
                    try:
                        next(algorithm_right)
                    except StopIteration:
                        algorithm_right = None
                        stats_right_text = stats_font.render(
                            compute_stats_text(grid_right), True, (0, 0, 0)
                        )
                if algorithm_left is None and algorithm_right is None:
                    step_accumulator = 0.0
                    break
        elif algorithm is not None:
            steps_per_second = speed_slider.get_current_value()
            step_accumulator += steps_per_second * time_delta
            while step_accumulator >= 1:
                step_accumulator -= 1
                try:
                    next(algorithm)
                except StopIteration:
                    algorithm = None
                    step_accumulator = 0.0
                    if is_search_run:
                        stats_text = stats_font.render(
                            compute_stats_text(grid), True, (0, 0, 0)
                        )
                    break

        manager.update(time_delta)

        window.fill((255, 255, 255))
        if compare_mode:
            half_width = GRID_WIDTH // 2
            mini_grid_height = grid_left.rows * grid_left.cell_size
            left_surface = window.subsurface(
                (0, TOP_BAR_HEIGHT, half_width, mini_grid_height)
            )
            right_surface = window.subsurface(
                (half_width, TOP_BAR_HEIGHT, half_width, mini_grid_height)
            )
            grid_left.draw(left_surface)
            grid_right.draw(right_surface)
            draw_outline(window, (0, TOP_BAR_HEIGHT, half_width, mini_grid_height))
            draw_outline(
                window, (half_width, TOP_BAR_HEIGHT, half_width, mini_grid_height)
            )

            left_display = stats_left_text or stats_font.render(
                f"{left_choice} (running)", True, (0, 0, 0)
            )
            right_display = stats_right_text or stats_font.render(
                f"{right_choice} (running)", True, (0, 0, 0)
            )
            label_y = TOP_BAR_HEIGHT + mini_grid_height + s(10)
            window.blit(left_display, (s(10), label_y))
            window.blit(right_display, (half_width + s(10), label_y))
        else:
            grid_surface = window.subsurface(
                (0, TOP_BAR_HEIGHT, GRID_WIDTH, GRID_HEIGHT)
            )
            grid.draw(grid_surface)
            draw_outline(window, (0, TOP_BAR_HEIGHT, GRID_WIDTH, GRID_HEIGHT))

        stats_separator_x = dfs_button.rect.right + s(15)
        pygame.draw.line(
            window,
            (150, 150, 150),
            (stats_separator_x, dfs_button.rect.top),
            (stats_separator_x, dfs_button.rect.bottom),
            2,
        )
        actions_separator_x = reset_button.rect.left - s(15)
        pygame.draw.line(
            window,
            (150, 150, 150),
            (actions_separator_x, reset_button.rect.top),
            (actions_separator_x, reset_button.rect.bottom),
            2,
        )
        row2_separator_x = (diagonal_button.rect.right + left_dropdown.rect.left) // 2
        pygame.draw.line(
            window,
            (150, 150, 150),
            (row2_separator_x, diagonal_button.rect.top),
            (row2_separator_x, diagonal_button.rect.bottom),
            2,
        )

        window.blit(speed_text, (s(10), s(12)))
        window.blit(stats_text, (dfs_button.rect.right + s(30), bottom_bar_y + s(12)))
        manager.draw_ui(window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
