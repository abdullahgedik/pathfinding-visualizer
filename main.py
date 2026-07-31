import pygame
from grid import Grid
from bfs import bfs

WINDOW_SIZE = 600
CELL_SIZE = 20
ROWS = WINDOW_SIZE // CELL_SIZE
COLS = WINDOW_SIZE // CELL_SIZE


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Pathfinding Visualizer")

    grid = Grid(ROWS, COLS, CELL_SIZE)
    algorithm = None

    running = True
    left_held = False
    right_held = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and grid.start and grid.end:
                    algorithm = bfs(grid)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
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
                    node = grid.get_node_from_pos(pos)
                    if left_held:
                        grid.handle_left_click(node)
                    elif right_held:
                        grid.handle_right_click(node)

        if algorithm is not None:
            try:
                next(algorithm)
            except StopIteration:
                algorithm = None

        window.fill((255, 255, 255))
        grid.draw(window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
