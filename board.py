import pygame
from typing import List

from color import Color
from direction import Direction
from game_stats import GameStats
from grid import Grid
from heading import Heading
from piece import Piece
from piece_bag import PieceBag
from renderer import BoardRenderer
from shapes import Shape
from tile import Tile

class Board():

    LEVEL_SPEED: List[float] = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.075, 0.05, 0.025]

    def __init__(self, size: tuple):
        self.game_stats = GameStats()
        self.grid = Grid()
        self.menu_grid = Grid(True)
        self.renderer = BoardRenderer(size=size, cols=self.grid.cols, rows=self.grid.rows)
        self._is_game_over = False

        self.bag: PieceBag = PieceBag()
        self._create_new_shape()
    
    def is_game_over(self):
        return self._is_game_over
        
    def set_game_over(self, value=True):
        self._is_game_over = value

    def get_level_speed(self):
        return self.LEVEL_SPEED[self.game_stats.level]

    def set_new_piece(self):
        color = self.active_piece.shape.color
        x, y = self.active_piece.origin
        for cell in self.active_piece.shape.get_shape(self.active_piece.orientation):
            col = (cell % 4) + x
            row = (cell // 4) + y
            self.grid.set_cell_color(col, row, color)

        self._create_new_shape()
        
        if not self._can_place(self.active_piece.shape, (x, y), self.active_piece.orientation):
            return False

        return True

    def _create_new_shape(self):
        shape: Shape = self.bag.next()
        self.active_piece = Piece(shape)
        self.shadow_shape = shape.clone()
        self.shadow_piece = Piece(self.shadow_shape, (3, self.grid.rows - 2), 0)

    def toggle_shadow(self):
        self.renderer.toggle_shadow()

    def move(self, direction: Direction = Direction.DOWN) -> bool:
        x, y = self.active_piece.origin
        if direction == Direction.LEFT:
            x -= 1
        elif direction == Direction.RIGHT:
            x += 1
        elif direction == Direction.DOWN or direction == Direction.DOWN_WK:
            y += 1

        candidate_piece_origin = (x, y)
        if not self._can_place(self.active_piece.shape, (x, y), self.active_piece.orientation):
            return False

        self.active_piece.origin = candidate_piece_origin
        return True

    def find_shadow_pos(self):
        x, y = self.active_piece.origin
        
        while self._can_place(self.shadow_piece.shape, (x, y), self.shadow_piece.orientation):
            y += 1
       
        self.shadow_piece.origin = (x, y - 1)

    def rotate(self, heading: Heading = Heading.CW):
        orientation = self.active_piece.orientation
        if heading == Heading.CCW:
            orientation = (orientation + 1) % 4
        elif heading == Heading.CW:
            orientation = (orientation - 1) % 4

        x, y = self.active_piece.origin
        
        if not self._can_place(self.active_piece.shape, (x, y), orientation):
            return False

        self.active_piece.orientation = orientation
        self.shadow_piece.orientation = orientation
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
        grid = self.grid
        if self._is_game_over:
            grid = self.menu_grid
            self.renderer.set_game_over()
        self.renderer.draw(surface, cells=grid.cells, active_piece=self.active_piece, shadow_piece=self.shadow_piece, 
            next_piece=self.bag.peek(), stats=self.game_stats)

