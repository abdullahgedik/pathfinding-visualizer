from node import Node
import pygame


class Grid:
    def __init__(self, row, cols, cell_size):
        self.rows = row
        self.cols = cols
        self.cell_size = cell_size
        self.nodes = self.make_nodes()

    def make_nodes(self):
        nodes = []
        for row in range(self.rows):
            row_nodes = []
            for col in range(self.cols):
                row_nodes.append(Node(row, col, self.cell_size))
            nodes.append(row_nodes)
        return nodes

    def draw(self, window):
        for row in self.nodes:
            for node in row:
                node.draw(window)
        self.draw_grid_lines(window)

    def draw_grid_lines(self, window):
        width = self.cols * self.cell_size
        height = self.rows * self.cell_size
        gray = (128, 128, 128)
        for row in range(self.rows):
            y = row * self.cell_size
            pygame.draw.line(window, gray, (0, y), (width, y))
        for col in range(self.cols):
            x = col * self.cell_size
            pygame.draw.line(window, gray, (x, 0), (x, height))
