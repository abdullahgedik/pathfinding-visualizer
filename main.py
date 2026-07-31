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
PANEL_HEIGHT = 60
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
        relative_rect=pygame.Rect((10, GRID_SIZE + 15), (100, 30)),
        text="BFS",
        manager=manager,
    )
    dijkstra_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((120, GRID_SIZE + 15), (100, 30)),
        text="Dijkstra",
        manager=manager,
    )
    astar_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((230, GRID_SIZE + 15), (100, 30)),
        text="A*",
        manager=manager,
    )
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((GRID_SIZE - 220, GRID_SIZE + 15), (100, 30)),
        text="Reset",
        manager=manager,
    )
    clear_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((GRID_SIZE - 110, GRID_SIZE + 15), (100, 30)),
        text="Clear",
        manager=manager,
    )

    running = True
    left_held = False
    right_held = False
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
                    elif event.button == 3:
                        right_held = True
                        grid.handle_right_click(node)
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
                        if left_held:
                            grid.handle_left_click(node)
                        elif right_held:
                            grid.handle_right_click(node)
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element is bfs_button and grid.start and grid.end:
                    algorithm = bfs(grid)
                elif event.ui_element is dijkstra_button and grid.start and grid.end:
                    algorithm = dijkstra(grid)
                elif event.ui_element is astar_button and grid.start and grid.end:
                    algorithm = astar(grid)
                elif event.ui_element is reset_button:
                    grid.reset()
                    algorithm = None
                elif event.ui_element is clear_button:
                    grid.clear()
                    algorithm = None

            manager.process_events(event)

        if algorithm is not None:
            try:
                next(algorithm)
            except StopIteration:
                algorithm = None

        manager.update(time_delta)

        window.fill((255, 255, 255))
        grid.draw(window)
        manager.draw_ui(window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
