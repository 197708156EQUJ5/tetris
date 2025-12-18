#!/usr/bin/env python3

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

from board import Board
from direction import Direction
from heading import Heading

class App:
    # Class-level constants, no globals
    WIDTH = 640
    HEIGHT = 736
    BG_COLOR = (0, 0, 0)
    FPS = 60
    KEY_REPEAT_DELAY = 400      # ms
    KEY_REPEAT_INTERVAL = 50    # ms

    def __init__(self):
        pygame.init()

        pygame.key.set_repeat(
            self.KEY_REPEAT_DELAY,
            self.KEY_REPEAT_INTERVAL
        )

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tetris")

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.elapsed_time = 0.0
        self.display_time = 0.0
        self.time_accumulator = 0.0

        self.board = Board((self.WIDTH, self.HEIGHT))

    def run(self):
        while self.is_running:
            dt = self.clock.tick(self.FPS) / 1000.0
            self.elapsed_time += dt
            self.time_accumulator += dt

            if self.time_accumulator >= self.board.get_level_speed():
                self.display_time = int(self.elapsed_time)
                self.time_accumulator = 0.0
                can_move = self.board.move(Direction.DOWN)

                if not can_move:
                    self.board.set_new_piece()
                    self.board.remove_lines()
            self.board.find_shadow_pos()
            
            self.handle_events()
            self.draw()
        pygame.quit()

    def quit(self):
        self.is_running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                # ESC quits for now
                if event.key == pygame.K_ESCAPE:
                    self.quit()

                self.handle_key_down(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)

    def handle_key_down(self, event: pygame.event.Event):
        can_move = True
        if event.key == pygame.K_LEFT:
            self.board.move(Direction.LEFT)
        elif event.key == pygame.K_RIGHT:
            self.board.move(Direction.RIGHT)
        elif event.key == pygame.K_DOWN:
            can_move = self.board.move(Direction.DOWN_WK)
        elif event.key == pygame.K_a:
            self.board.rotate(Heading.CCW)
        elif event.key == pygame.K_s:
            self.board.rotate(Heading.CW)
        elif event.key == pygame.K_g:
            self.board.toggle_shadow()

        if not can_move:
            self.board.set_new_piece()
            self.board.remove_lines()

    def handle_mouse_down(self, event: pygame.event.Event):
        # Shell: editor/app mouse handling goes here
        # event.pos, event.button, etc.
        pass

    def update(self, dt: float):
        pass

    def draw(self):
        # Fill screen with background 0,0,0
        self.screen.fill(self.BG_COLOR)

        # Draw UI
        self.board.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    app = App()
    app.run()
