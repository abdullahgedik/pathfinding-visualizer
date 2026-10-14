import json
from node import Node
import pygame

TERRAIN_COSTS = {
    "light": 3,
    "heavy": 8,
}

CELL_STATES = {"empty", "wall", "start", "end", "light", "heavy"}


class Grid:
    def __init__(self, row, cols, cell_size):
        self.rows = row
        self.cols = cols
        self.cell_size = cell_size
        self.nodes = self.make_nodes()
        self.start = None
        self.end = None
        self.diagonal_enabled = False

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

    def get_node_from_pos(self, pos):
        x, y = pos
        row = y // self.cell_size
        col = x // self.cell_size
        row = max(0, min(row, self.rows - 1))
        col = max(0, min(col, self.cols - 1))
        return self.nodes[row][col]

    def handle_left_click(self, node, paint_mode="wall"):
        if self.start is None and node is not self.end:
            self.start = node
            node.state = "start"
            node.weight = 1
        elif self.end is None and node is not self.start:
            self.end = node
            node.state = "end"
            node.weight = 1
        elif node is not self.start and node is not self.end:
            if paint_mode in TERRAIN_COSTS:
                node.state = paint_mode
                node.weight = TERRAIN_COSTS[paint_mode]
            else:
                node.state = "wall"
                node.weight = 1
        else:
            return
        node.on_path = False

    def handle_right_click(self, node):
        if node is self.start:
            self.start = None
        elif node is self.end:
            self.end = None
        node.state = "empty"
        node.weight = 1
        node.on_path = False

    def get_line_nodes(self, start_node, end_node):
        r0, c0 = start_node.row, start_node.col
        r1, c1 = end_node.row, end_node.col
        steps = max(abs(r1 - r0), abs(c1 - c0))
        if steps == 0:
            return [end_node]

        nodes = []
        for i in range(steps + 1):
            t = i / steps
            row = round(r0 + (r1 - r0) * t)
            col = round(c0 + (c1 - c0) * t)
            nodes.append(self.nodes[row][col])
        return nodes

    def get_neighbors(self, node):
        neighbors = []
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if self.diagonal_enabled:
            deltas += [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d_row, d_col in deltas:
            new_row = node.row + d_row
            new_col = node.col + d_col
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                neighbor = self.nodes[new_row][new_col]
                if neighbor.state != "wall":
                    neighbors.append(neighbor)
        return neighbors

    def get_maze_neighbors(self, node):
        neighbors = []
        deltas = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for d_row, d_col in deltas:
            new_row = node.row + d_row
            new_col = node.col + d_col
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                neighbor = self.nodes[new_row][new_col]
                if not neighbor.visited:
                    wall_row = node.row + d_row // 2
                    wall_col = node.col + d_col // 2
                    wall_node = self.nodes[wall_row][wall_col]
                    neighbors.append((neighbor, wall_node))
        return neighbors

    def reconstruct_path(self, end):
        current = end.came_from
        while current is not None and current is not self.start:
            current.on_path = True
            current = current.came_from

    def clear(self):
        self.nodes = self.make_nodes()
        self.start = None
        self.end = None

    def reset(self):
        for row in self.nodes:
            for node in row:
                node.visited = False
                node.came_from = None
                node.distance = float("inf")
                node.on_path = False

    def to_dict(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "cell_size": self.cell_size,
            "diagonal_enabled": self.diagonal_enabled,
            "cells": [
                [{"state": node.state, "weight": node.weight} for node in row]
                for row in self.nodes
            ],
        }

    def load_from_dict(self, data):
        try:
            if data["rows"] != self.rows or data["cols"] != self.cols:
                raise ValueError("Saved layout size does not match the current grid size")

            # Build into fresh nodes so a malformed file leaves the current grid untouched
            nodes = self.make_nodes()
            start = None
            end = None
            for row_index, row in enumerate(data["cells"]):
                for col_index, cell in enumerate(row):
                    node = nodes[row_index][col_index]
                    if cell["state"] not in CELL_STATES:
                        raise ValueError(f"Unknown cell state: {cell['state']}")
                    node.state = cell["state"]
                    node.weight = cell["weight"]
                    if node.state == "start":
                        start = node
                    elif node.state == "end":
                        end = node
        except (KeyError, TypeError, IndexError) as error:
            raise ValueError("Saved layout file is malformed") from error

        self.nodes = nodes
        self.start = start
        self.end = end
        self.diagonal_enabled = data.get("diagonal_enabled", False)

    def save_to_file(self, path):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f)

    def load_from_file(self, path):
        with open(path) as f:
            data = json.load(f)
        self.load_from_dict(data)
