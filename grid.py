from typing import List

from color import Color
from tile import Tile

class Grid:
    def __init__(self, cols: int, rows: int):
        self.cols = cols
        self.rows = rows
        self._cells = [Tile(aid=i) for i in range(cols * rows)]

    def index(self, col: int, row: int) -> int:
        return row * self.cols + col

    def in_bounds(self, col: int, row: int) -> bool:
        return 0 <= col < self.cols and 0 <= row < self.rows

    def is_empty(self, col: int, row: int) -> bool:
        return self.cells[self.index(col, row)].is_empty()

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value):
        self._cells = value

    def set_cell_color(self, col: int, row: int, color: Color):
        self._cells[row * self.cols + col].color = color
    
