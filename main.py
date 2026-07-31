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

SCALE = 1.3


def s(value):
    return round(value * SCALE)


ROWS = 30
COLS = 30
CELL_SIZE = s(20)
GRID_SIZE = CELL_SIZE * ROWS
PANEL_HEIGHT = s(170)
WINDOW_WIDTH = GRID_SIZE
WINDOW_HEIGHT = GRID_SIZE + PANEL_HEIGHT


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

    bfs_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(10), GRID_SIZE + s(10)), (s(110), s(30))),
        text="BFS",
        manager=manager,
    )
    dijkstra_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(126), GRID_SIZE + s(10)), (s(110), s(30))),
        text="Dijkstra",
        manager=manager,
    )
    astar_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(242), GRID_SIZE + s(10)), (s(110), s(30))),
        text="A*",
        manager=manager,
    )
    greedy_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(358), GRID_SIZE + s(10)), (s(110), s(30))),
        text="Greedy",
        manager=manager,
    )
    dfs_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(474), GRID_SIZE + s(10)), (s(110), s(30))),
        text="DFS",
        manager=manager,
    )
    maze_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(10), GRID_SIZE + s(50)), (s(90), s(30))),
        text="Maze",
        manager=manager,
    )
    mode_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(110), GRID_SIZE + s(50)), (s(130), s(30))),
        text="Wall Mode",
        manager=manager,
    )
    diagonal_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((s(250), GRID_SIZE + s(50)), (s(140), s(30))),
        text="Diagonal: Off",
        manager=manager,
    )
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((GRID_SIZE - s(190), GRID_SIZE + s(50)), (s(90), s(30))),
        text="Reset",
        manager=manager,
    )
    clear_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((GRID_SIZE - s(100), GRID_SIZE + s(50)), (s(90), s(30))),
        text="Clear",
        manager=manager,
    )
    speed_font = pygame.font.SysFont("segoeui", s(22), bold=True)
    speed_text = speed_font.render("Speed", True, (0, 0, 0))
    stats_font = pygame.font.SysFont("segoeui", s(20), bold=True)
    stats_text = None
    speed_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((s(100), GRID_SIZE + s(95)), (GRID_SIZE - s(110), s(30))),
        start_value=30,
        value_range=(1, 800),
        manager=manager,
    )

    running = True
    left_held = False
    right_held = False
    last_paint_node = None
    paint_mode = "wall"
    step_accumulator = 0.0
    is_search_run = False
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] < GRID_SIZE:
                    node = grid.get_node_from_pos(pos)
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
            elif event.type == pygame.MOUSEMOTION:
                if left_held or right_held:
                    pos = pygame.mouse.get_pos()
                    if pos[1] < GRID_SIZE:
                        node = grid.get_node_from_pos(pos)
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
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element is bfs_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = bfs(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = None
                elif event.ui_element is dijkstra_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = dijkstra(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = None
                elif event.ui_element is astar_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = astar(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = None
                elif event.ui_element is greedy_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = greedy(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = None
                elif event.ui_element is dfs_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = dfs(grid)
                    step_accumulator = 0.0
                    is_search_run = True
                    stats_text = None
                elif event.ui_element is mode_button:
                    if paint_mode == "wall":
                        paint_mode = "weight"
                        mode_button.set_text("Weight Mode")
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
                    stats_text = None
                elif event.ui_element is reset_button:
                    grid.reset()
                    algorithm = None
                    stats_text = None
                elif event.ui_element is clear_button:
                    grid.clear()
                    algorithm = None
                    stats_text = None

            manager.process_events(event)

        if algorithm is not None:
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
                        visited_count = sum(
                            1 for row in grid.nodes for node in row if node.visited
                        )
                        if grid.end.came_from is not None:
                            path_length = (
                                sum(
                                    1
                                    for row in grid.nodes
                                    for node in row
                                    if node.on_path
                                )
                                + 2
                            )
                            text = (
                                f"Visited: {visited_count}   Path length: {path_length}"
                            )
                        else:
                            text = f"Visited: {visited_count}   No path found"
                        stats_text = stats_font.render(text, True, (0, 0, 0))
                    break

        manager.update(time_delta)

        window.fill((255, 255, 255))
        grid.draw(window)
        separator_x = (diagonal_button.rect.right + reset_button.rect.left) // 2
        pygame.draw.line(
            window,
            (150, 150, 150),
            (separator_x, diagonal_button.rect.top),
            (separator_x, diagonal_button.rect.bottom),
            2,
        )
        window.blit(speed_text, (s(18), GRID_SIZE + s(92)))
        if stats_text is not None:
            window.blit(stats_text, (s(18), GRID_SIZE + s(127)))
        manager.draw_ui(window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
