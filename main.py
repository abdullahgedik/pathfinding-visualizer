import pygame
from grid import Grid

WINDOW_SIZE = 600
CELL_SIZE = 20
ROWS = WINDOW_SIZE // CELL_SIZE
COLS = WINDOW_SIZE // CELL_SIZE


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Pathfinding Visualizer")

    grid = Grid(ROWS, COLS, CELL_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill((255, 255, 255))
        grid.draw(window)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
