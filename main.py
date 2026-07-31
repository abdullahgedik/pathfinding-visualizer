import pygame
import pygame_gui
from grid import Grid
from bfs import bfs
from dijkstra import dijkstra
from astar import astar

GRID_SIZE = 600
CELL_SIZE = 20
ROWS = GRID_SIZE // CELL_SIZE
COLS = GRID_SIZE // CELL_SIZE
PANEL_HEIGHT = 100
WINDOW_WIDTH = GRID_SIZE
WINDOW_HEIGHT = GRID_SIZE + PANEL_HEIGHT


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pathfinding Visualizer")
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))

    grid = Grid(ROWS, COLS, CELL_SIZE)
    algorithm = None

    bfs_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((10, GRID_SIZE + 10), (100, 30)),
        text="BFS",
        manager=manager,
    )
    dijkstra_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((120, GRID_SIZE + 10), (100, 30)),
        text="Dijkstra",
        manager=manager,
    )
    astar_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((230, GRID_SIZE + 10), (100, 30)),
        text="A*",
        manager=manager,
    )
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((GRID_SIZE - 220, GRID_SIZE + 10), (100, 30)),
        text="Reset",
        manager=manager,
    )
    clear_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((GRID_SIZE - 110, GRID_SIZE + 10), (100, 30)),
        text="Clear",
        manager=manager,
    )
    speed_font = pygame.font.SysFont(None, 28)
    speed_text = speed_font.render("Speed", True, (0, 0, 0))
    speed_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((100, GRID_SIZE + 55), (GRID_SIZE - 110, 30)),
        start_value=30,
        value_range=(1, 800),
        manager=manager,
    )

    running = True
    left_held = False
    right_held = False
    last_paint_node = None
    step_accumulator = 0.0
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
                        grid.handle_left_click(node)
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
                                grid.handle_left_click(line_node)
                            elif right_held:
                                grid.handle_right_click(line_node)
                        last_paint_node = node
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element is bfs_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = bfs(grid)
                    step_accumulator = 0.0
                elif event.ui_element is dijkstra_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = dijkstra(grid)
                    step_accumulator = 0.0
                elif event.ui_element is astar_button and grid.start and grid.end:
                    grid.reset()
                    algorithm = astar(grid)
                    step_accumulator = 0.0
                elif event.ui_element is reset_button:
                    grid.reset()
                    algorithm = None
                elif event.ui_element is clear_button:
                    grid.clear()
                    algorithm = None

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
                    break

        manager.update(time_delta)

        window.fill((255, 255, 255))
        grid.draw(window)
        window.blit(speed_text, (20, GRID_SIZE + 62))
        manager.draw_ui(window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
