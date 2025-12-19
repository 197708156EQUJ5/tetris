import pygame
from typing import List, Tuple

from color import Color
from tile import Tile
from utils import Utils


class MenuRenderer:
    FONT_PATH = Utils.resource_path("assets/fonts/ttf/JetBrainsMono-Regular.ttf")

    def __init__(self, size: Tuple[int, int]):
        self.size = size
        self.title_font = pygame.font.Font(self.FONT_PATH, 52)
        self.option_font = pygame.font.Font(self.FONT_PATH, 36)
        self.options = [
            "New Game",
            "Resume Game",
            "High Score",
            "Exit",
        ]

        self.tile_size = 32


    def draw(self, surface: pygame.Surface, cells: List[Tile], show_resume: bool):
        self._draw_background(surface, cells)

        labels = ["New Game"]
        if show_resume:
            labels.append("Resume Game")
        labels += ["High Score", "Exit"]

        # Build numbered strings with no gaps
        self.options = [f"{i + 1}.  {label}" for i, label in enumerate(labels)]
        self._draw_centered_text(surface)

    def _draw_background(self, surface: pygame.Surface, cells: List[Tile]):
        w, h = self.size
        cols = (w + self.tile_size - 1) // self.tile_size
        rows = (h + self.tile_size - 1) // self.tile_size

        # Tile the screen using colors from the provided grid cells (wrap if needed)
        total = len(cells) if cells else 1

        idx = 0
        for r in range(rows):
            for c in range(cols):
                tile = cells[idx % total] if cells else None
                idx += 1

                rect = pygame.Rect(c * self.tile_size, r * self.tile_size, self.tile_size, self.tile_size)

                # If the random grid has black cells, don’t leave holes—paint them “dim”
                color = tile.color if tile and tile.color != Color.BLACK else (15, 15, 15)

                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (0, 0, 0), rect, 1)

        # Subtle dark overlay so text pops
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

    def _draw_centered_text(self, surface: pygame.Surface):
        w, h = self.size

        title = self.title_font.render("TETRIS", True, Color.WHITE)
        title_rect = title.get_rect(center=(w // 2, h // 2 - 160))
        surface.blit(title, title_rect)

        rendered = [self.option_font.render(line, True, Color.WHITE) for line in self.options]
        if not rendered:
            return

        line_h = rendered[0].get_height()
        gap = 16
        
        max_w = max(s.get_width() for s in rendered)
        left_x = ((w - max_w) // 2) + 100
        
        block_h = (len(rendered) * line_h) + ((len(rendered) - 1) * gap)
        start_y = (h // 2) - (block_h // 2) + 20

        for i, surf in enumerate(rendered):
            rect = surf.get_rect()
            rect.centerx = left_x
            rect.y = start_y + i * (line_h + gap)
            surface.blit(surf, rect)

