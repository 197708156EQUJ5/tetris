import pygame
from typing import List, Tuple

from color import Color
from game_stats import GameStats
from piece import Piece
from shapes import Shape
from tile import Tile

class BoardRenderer:

    BG_COLOR = (10, 10, 200)
    INSET = 30
    TILE_SIZE = 32
    PREVIEW_TILE_SIZE = 24
    PREVIEW_ORIGIN = (1, 1)

    def __init__(self, size: tuple, cols: int, rows: int):
        self.font = pygame.font.SysFont("monospace", 16)
        self.cols = cols
        self.rows = rows
        self._show_shadow = True
        self.border_coords = (self.INSET - 3, self.INSET, 326, 645)
        self.border_rect = pygame.Rect(self.border_coords)
        self.preview_coords = ((2 * size[0] // 3) + self.INSET, self.INSET, 125, 125)
        self.preview_rect = pygame.Rect(self.preview_coords)
        self.level_label_pos = ((2 * size[0] // 3) + self.INSET, self.INSET + 125 + 10)
        self.lines_cleared_label_pos = ((2 * size[0] // 3) + self.INSET, self.INSET + 125 + 30)
        self.score_label_pos = ((2 * size[0] // 3) + self.INSET, self.INSET + 125 + 50)

        # Layout / rects (you can pass these in instead if you prefer)
        self.grid_origin_px = (self.INSET, 0 - self.TILE_SIZE)

    def toggle_shadow(self):
        self._show_shadow = not self._show_shadow

    def draw(self, surface: pygame.Surface, cells: List[Tile], active_piece: Piece, shadow_piece: Piece, 
        next_piece: Shape, stats: GameStats):
        self._draw_cells(surface, cells)
        pygame.draw.rect(surface, self.BG_COLOR, self.border_rect, 2, border_radius=1)
        pygame.draw.rect(surface, self.BG_COLOR, self.preview_rect, 2, border_radius=1)

        if self._show_shadow:
            self._draw_shadow_piece(surface, shadow_piece)
        self._draw_active_piece(surface, active_piece)
        self._draw_preview(surface, next_piece)
        self._draw_stats(surface, stats)

    def _shade(self, rgb, factor: float = 0.5) -> pygame.Color:
        return pygame.Color(int(rgb[0] * factor), int(rgb[1] * factor), int(rgb[2] * factor))

    def _draw_cells(self, surface: pygame.Surface, cells: List[Tile]):
        for idx, tile in enumerate(cells):
            col = idx % self.cols
            row = idx // self.cols

            x = col * self.TILE_SIZE + self.INSET
            y = (row * self.TILE_SIZE) - self.TILE_SIZE
            rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)

            if tile.color is not Color.BLACK:
                fill = self._shade(tile.color, 0.5)
                pygame.draw.rect(surface, fill, rect)
                pygame.draw.rect(surface, tile.color, rect, 2, border_radius=2)

    def _draw_shadow_piece(self, surface: pygame.Surface, piece: Shape):
        ox, oy = piece.origin
        for cell in range(16):
            if cell in piece.shape.get_shape(piece.orientation):
                col = ox + (cell % 4)
                row = oy + (cell // 4)

                x = (col * self.TILE_SIZE) + self.grid_origin_px[0]
                y = (row * self.TILE_SIZE) + self.grid_origin_px[1]
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)

                fill = self._shade(piece.shape.color, 0.35)
                pygame.draw.rect(surface, fill, rect)
                pygame.draw.rect(surface, piece.shape.color, rect, 2, border_radius=2)

    def _draw_active_piece(self, surface: pygame.Surface, piece: Piece):
        ox, oy = piece.origin
        for cell in range(16):
            if cell in piece.shape.get_shape(piece.orientation):
                col = ox + (cell % 4)
                row = oy + (cell // 4)

                x = (col * self.TILE_SIZE) + self.grid_origin_px[0]
                y = (row * self.TILE_SIZE) + self.grid_origin_px[1]
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)

                fill = self._shade(piece.shape.color, 0.5)
                pygame.draw.rect(surface, fill, rect)
                pygame.draw.rect(surface, piece.shape.color, rect, 2, border_radius=2)

    def _draw_preview(self, surface: pygame.Surface, shape: Shape):
        ox, oy = self.PREVIEW_ORIGIN

        # center inside preview_rect (simple version)
        base_x = self.preview_rect.x + 10
        base_y = self.preview_rect.y + 10

        for cell in range(16):
            if cell in shape.get_shape(0):
                col = ox + (cell % 4)
                row = oy + (cell // 4)

                x = base_x + (col * self.PREVIEW_TILE_SIZE)
                y = base_y + (row * self.PREVIEW_TILE_SIZE)
                rect = pygame.Rect(x, y, self.PREVIEW_TILE_SIZE, self.PREVIEW_TILE_SIZE)

                fill = self._shade(shape.color, 0.5)
                pygame.draw.rect(surface, fill, rect)
                pygame.draw.rect(surface, shape.color, rect, 2, border_radius=2)

    def _draw_stats(self, surface: pygame.Surface, stats):
        level_label = self.font.render("Level:", True, Color.GREEN)
        level_value = self.font.render(str(stats.level), True, Color.WHITE)
        rect = surface.blit(level_label, self.level_label_pos)
        surface.blit(level_value, (rect.x + rect.width + 5, rect.y))

        lines_label = self.font.render("Lines:", True, Color.GREEN)
        lines_value = self.font.render(str(stats.lines_cleared), True, Color.WHITE)
        rect = surface.blit(lines_label, self.lines_cleared_label_pos)
        surface.blit(lines_value, (rect.x + rect.width + 5, rect.y))

        score_label = self.font.render("Score:", True, Color.GREEN)
        score_value = self.font.render(str(stats.score), True, Color.WHITE)
        rect = surface.blit(score_label, self.score_label_pos)
        surface.blit(score_value, (rect.x + rect.width + 5, rect.y))

