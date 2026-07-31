import pygame


class Node:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.x = col * size
        self.y = row * size
        self.state = "empty"
        self.visited = False
        self.came_from = None
        self.distance = float("inf")
        self.weight = 1
        self.on_path = False

    def draw(self, window):
        colors = {
            "empty": (255, 255, 255),
            "wall": (0, 0, 0),
            "start": (255, 165, 0),
            "end": (64, 224, 208),
            "weight": (139, 69, 19),
        }
        if self.state in ("start", "end"):
            color = colors[self.state]
        elif self.on_path:
            color = (255, 255, 0)
        elif self.state == "empty" and self.visited:
            color = (175, 216, 248)
        else:
            color = colors[self.state]
        pygame.draw.rect(window, color, (self.x, self.y, self.size, self.size))
