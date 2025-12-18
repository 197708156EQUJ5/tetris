import pygame
from typing import List

from color import Color
from direction import Direction
from game_stats import GameStats
from grid import Grid
from heading import Heading
from piece_bag import PieceBag
from renderer import BoardRenderer
from shapes import Shape
from tile import Tile

class Board():

    LEVEL_SPEED: List[float] = [0.8, 0.7, 0.6, 0.5]
    GRID = (10, 22)

    def __init__(self, size: tuple):
        self.size = size
        self.game_stats = GameStats()
        self.cols, self.rows = self.GRID

        self.renderer = BoardRenderer(size=self.size, cols=self.cols, rows=self.rows)
        
        self.show_grid_lines = False
        self.grid = Grid(self.cols, self.rows)

        self.active_orientation = 0
        self.active_origin: tuple[int, int] = (3, 0)
        self.bag: PieceBag = PieceBag()
        self.active_piece = self.bag.next()

    def set_new_piece(self):
        color = self.active_piece.color
        x = self.active_origin[0]
        y = self.active_origin[1]
        for cell in self.active_piece.get_shape(self.active_orientation):
            col = (cell % 4) + x
            row = (cell // 4) + y
            self.grid.set_cell_color(col, row, color)

        self.active_piece = self.bag.next()
        self.active_origin = (3, 0)

    def toggle_grid_lines(self):
        self.show_grid_lines = not self.show_grid_lines

    def move(self, direction: Direction = Direction.DOWN) -> bool:
        x = self.active_origin[0]
        y = self.active_origin[1]
        if direction == Direction.LEFT:
            x -= 1
        elif direction == Direction.RIGHT:
            x += 1
        elif direction == Direction.DOWN or direction == Direction.DOWN_WK:
            y += 1

        candidate_piece_origin = (x, y)
        if not self._can_place(self.active_piece, (x, y), self.active_orientation):
            return False

        self.active_origin = candidate_piece_origin
        return True

    def rotate(self, heading: Heading = Heading.CW):
        orientation = self.active_orientation
        if heading == Heading.CCW:
            orientation = (orientation + 1) % 4
        elif heading == Heading.CW:
            orientation = (orientation - 1) % 4

        x, y = self.active_origin
        
        if not self._can_place(self.active_piece, (x, y), orientation):
            return False

        self.active_orientation = orientation
        return True

    def _can_place(self, shape: Shape, origin: tuple[int, int], orientation: int) -> bool:
        ox, oy = origin
        for cell in shape.get_shape(orientation):
            col = ox + (cell % 4)
            row = oy + (cell // 4)
            if not self.grid.in_bounds(col, row):
                return False
            if not self.grid.is_empty(col, row):
                return False
        return True

    def remove_lines(self):
        delete_rows: List[int] = []
        col_counter = 0

        for i, cell in enumerate(self.grid.cells):
            col = i % 10
            row = i // 10

            if col == 0:
                col_counter = 0
            if cell.color != Color.BLACK:
                col_counter += 1
            if col == 9:
                if col_counter == 10:
                    delete_rows.append(row)

        temp_grid: List[Tile] = []
        for i, cell in enumerate(self.grid.cells):
            row = i // 10
            if not row in delete_rows:
                temp_grid.append(cell)

        for _ in range(0, len(delete_rows) * 10):
            temp_grid.insert(0, Tile())

        self.grid.cells = temp_grid
        self.game_stats.on_lines_cleared(len(delete_rows))

    def draw(self, surface: pygame.Surface):
        self.renderer.draw(surface, cells=self.grid.cells, active_piece=self.active_piece, active_origin=self.active_origin,
            active_orientation=self.active_orientation, next_piece=self.bag.peek(), show_grid_lines=self.show_grid_lines,
            stats=self.game_stats)

