#!/usr/bin/env python3

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import warnings
warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API",
    category=UserWarning,
)
import pygame

from board import Board
from direction import Direction
from heading import Heading
from utils import GameState
from utils import Utils

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

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tetris")
        app_icon = pygame.image.load(Utils.resource_path("assets/icons/app_icon.png")).convert_alpha()
        pygame.display.set_icon(app_icon)
        pygame.key.set_repeat(self.KEY_REPEAT_DELAY, self.KEY_REPEAT_INTERVAL)

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
            if self.board.game_state == GameState.PLAY and not self.board.is_game_over():
                self.time_accumulator += dt

                if self.time_accumulator >= self.board.get_level_speed():
                    self.display_time = int(self.elapsed_time)
                    self.time_accumulator = 0.0
                    can_move = self.board.move(Direction.DOWN)

                    if not can_move:
                        if not self.board.set_new_piece():
                            self.board.set_game_state(GameState.DONE)
                        self.board.remove_lines()
            else:
                self.time_accumulator = 0.0

            if self.board.game_state == GameState.PLAY:
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
        # Toggle pause/menu
        if event.key == pygame.K_p:
            if self.board.game_state == GameState.PLAY:
                self.board._is_paused_menu = True
                self.board.set_game_state(GameState.MENU)
            elif self.board.game_state == GameState.MENU and self.board.is_paused_menu:
                self.board._is_paused_menu = False
                self.board.set_game_state(GameState.PLAY)
            return

        # Menu hotkeys
        if self.board.game_state == GameState.MENU:
            if event.key == pygame.K_1:
                self.board._is_paused_menu = False
                self.board.new_game()
                return

            if self.board.is_paused_menu:
                # Paused menu: 2 = Resume, 4 = Exit
                if event.key == pygame.K_2:
                    self.board._is_paused_menu = False
                    self.board.set_game_state(GameState.PLAY)
                    return
                if event.key == pygame.K_4:
                    self.quit()
                    return
            else:
                # Start menu: 3 = Exit
                if event.key == pygame.K_3:
                    self.quit()
                    return

            return
        
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
            if not self.board.set_new_piece():
                self.board.set_game_state(GameState.DONE)
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
