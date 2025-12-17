import pygame
import random
from typing import List

from color import Color
from direction import Direction
from dog_leg_lf import DogLegLf
from dog_leg_rt import DogLegRt
from ess import Ess
from heading import Heading
from i_beam import IBeam
from game_stats import GameStats
from shape import Shape
from square import Square
from tee import Tee
from tile import Tile
from zee import Zee
from grid import Grid

class Board():

    BG_COLOR = (10, 10, 200)
    INSET = 30
    LEVEL_SPEED: List[float] = [0.8, 0.7, 0.6, 0.5]
    GRID = (10, 22)
    TILE_SIZE = 32
    TILE_PREVIEW_SIZE = 24
    BAG: List[Shape] = [DogLegRt(), DogLegLf(), Square(), Zee(), Tee(), Ess(), IBeam()]

    def __init__(self, size: tuple, font):
        self.size = size
        self.font = font
        self.grid_origin = (self.INSET, 0 - self.TILE_SIZE)
        self.border_coords = (self.INSET - 3, self.INSET, 326, 645)
        self.preview_coords = ((2 * size[0] // 3) + self.INSET, self.INSET, 125, 125)
        self.level_label_coords = ((2 * size[0] // 3) + self.INSET, self.INSET + 125 + 10)
        self.lines_cleared_label_coords = ((2 * size[0] // 3) + self.INSET, self.INSET + 125 + 30)
        self.score_label_coords = ((2 * size[0] // 3) + self.INSET, self.INSET + 125 + 50)
        self.border_rect = pygame.Rect(self.border_coords)
        self.preview_rect = pygame.Rect(self.preview_coords)
        self.game_stats = GameStats()
        self.show_grid_lines = False
        self.cols, self.rows = self.GRID
        self.grid = Grid(self.cols, self.rows)

        self.active_orientation = 0
        self.active_origin: tuple[int, int] = (3, 0)
        self.preview_origin = (14, 3)
        self.pieces: List[Shape] = []
        self._load_pieces()
        self.active_piece = self.pieces.pop(0)

    def _load_pieces(self):
        random.shuffle(self.BAG)
        for shape in self.BAG:
            self.pieces.append(shape)

    def set_new_piece(self):
        color = self.active_piece.color
        x = self.active_origin[0]
        y = self.active_origin[1]
        for cell in self.active_piece.get_shape(self.active_orientation):
            col = (cell % 4) + x
            row = (int(cell / 4)) + y
            self.grid.set_cell_color(col, row, color)

        if len(self.pieces) < 2:
            self._load_pieces()

        self.active_piece = self.pieces.pop(0)
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
            row = int(i / 10)
            if not row in delete_rows:
                temp_grid.append(cell)

        for _ in range(0, len(delete_rows) * 10):
            temp_grid.insert(0, Tile())

        self.grid.cells = temp_grid

    def draw(self, surface: pygame.Surface):
        self._draw_cells(surface)

        pygame.draw.rect(surface, self.BG_COLOR, self.border_rect, 2, border_radius=1)
        pygame.draw.rect(surface, self.BG_COLOR, self.preview_rect, 2, border_radius=1)

        self._draw_piece(surface)
        self._draw_preview(surface)
        self._draw_game_stats(surface)

    def _draw_cells(self, surface: pygame.Surface):
        i: int = 0
        for tile in self.grid.cells:
            x = (i % self.cols) * self.TILE_SIZE + self.INSET
            y = ((i // self.cols) * self.TILE_SIZE) - self.TILE_SIZE
            tile_count = int(i / self.cols)
            rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
            if tile.color is not Color.BLACK:
                color = pygame.Color(int(tile.color[0] * 0.5), int(tile.color[1] * 0.5), int(tile.color[2] * 0.5))
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, tile.color, rect, 2, border_radius=2)
            if self.show_grid_lines:
                pygame.draw.rect(surface, Color.WHITE, rect, 1, border_radius=1)

            i += 1

    def _draw_piece(self, surface: pygame.Surface):
        for cell in range(0, 15):
            if cell in self.active_piece.get_shape(self.active_orientation):
                grid_col = self.active_origin[0] + int((cell % 4))
                grid_row = self.active_origin[1] + int((cell / 4))
                x = (grid_col * self.TILE_SIZE) + self.grid_origin[0]
                y = (grid_row * self.TILE_SIZE) + self.grid_origin[1]
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                piece_color = self.active_piece.color
                color = pygame.Color(int(piece_color[0] * 0.5), int(piece_color[1] * 0.5), int(piece_color[2] * 0.5))
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, self.active_piece.color, rect, 2, border_radius=2)

    def _draw_preview(self, surface: pygame.Surface):
        preview_piece = self.pieces[0]
        for cell in range(0, 15):
            if cell in preview_piece.get_shape(0):
                grid_col = self.preview_origin[0] + int((cell % 4))
                grid_row = self.preview_origin[1] + int((cell / 4))
                x = (grid_col * self.TILE_PREVIEW_SIZE) + self.grid_origin[0]
                y = (grid_row * self.TILE_PREVIEW_SIZE) + self.grid_origin[1]
                rect = pygame.Rect(x + 125, y + 15, self.TILE_PREVIEW_SIZE, self.TILE_PREVIEW_SIZE)
                piece_color = preview_piece.color
                color = pygame.Color(int(piece_color[0] * 0.5), int(piece_color[1] * 0.5), int(piece_color[2] * 0.5))
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, piece_color, rect, 2, border_radius=2)

    def _draw_game_stats(self, surface: pygame.Surface):
        level_label_text = self.font.render("Level:", True, Color.GREEN)
        level_text = self.font.render(str(self.game_stats.level), True, Color.WHITE)
        rect = surface.blit(level_label_text, self.level_label_coords)
        surface.blit(level_text, (rect.x + rect.width + 5, rect.y))

        lines_cleared_label_text = self.font.render("Lines Cleared:", True, Color.GREEN)
        lines_cleared_text = self.font.render(str(self.game_stats.lines_cleared), True, Color.WHITE)
        rect = surface.blit(lines_cleared_label_text, self.lines_cleared_label_coords)
        surface.blit(lines_cleared_text, (rect.x + rect.width + 5, rect.y))

        score_label_text = self.font.render("Score:", True, Color.GREEN)
        score_text = self.font.render(str(self.game_stats.score), True, Color.WHITE)
        rect = surface.blit(score_label_text, self.score_label_coords)
        surface.blit(score_text, (rect.x + rect.width + 5, rect.y))

