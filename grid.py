import random
from typing import List

from color import Color
from tile import Tile

class Grid:

    GRID = (10, 22)

    def __init__(self, fill_random=False):
        self._cols, self._rows = self.GRID
        self._cells: List[Tile] = []
        color_list = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.ORANGE, Color.LT_BLUE, Color.PURPLE]
        for i in range(self._cols * self._rows):
            if fill_random:
                color = random.choice(color_list[1:])
            else:
                color = Color.BLACK
            self._cells.append(Tile(color=color, aid=1))

    def index(self, col: int, row: int) -> int:
        return row * self._cols + col

    def in_bounds(self, col: int, row: int) -> bool:
        return 0 <= col < self._cols and 0 <= row < self._rows

    def is_empty(self, col: int, row: int) -> bool:
        return self.cells[self.index(col, row)].is_empty()

    @property
    def cols(self):
        return self._cols

    @property
    def rows(self):
        return self._rows

    @property
    def cells(self):
        return self._cells

    @cells.setter
    def cells(self, value):
        self._cells = value

    def set_cell_color(self, col: int, row: int, color: Color):
        self._cells[row * self._cols + col].color = color
    
