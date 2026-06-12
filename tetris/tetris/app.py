"""Application bootstrap and main loop."""

import sys

import pygame

from tetris.config import FPS, HEIGHT, WIDTH
from tetris.game import TetrisGame
from tetris.input_handler import handle_keydown
from tetris.models import GameStatus
from tetris.renderer import Renderer


def _build_fonts() -> dict[str, pygame.font.Font]:
    return {
        "title": pygame.font.SysFont("consolas", 22, bold=True),
        "score": pygame.font.SysFont("consolas", 20, bold=True),
        "menu": pygame.font.SysFont("consolas", 24),
        "banner": pygame.font.SysFont("consolas", 28, bold=True),
        "small": pygame.font.SysFont("consolas", 14),
    }


class TetrisApp:
    def __init__(self) -> None:
        self.game = TetrisGame()
        self.renderer: Renderer | None = None
        self.screen: pygame.Surface | None = None
        self.clock = pygame.time.Clock()
        self.last_step = 0
        self.frame = 0

        # DAS (Delayed Auto Shift) for horizontal movement
        self.das_key: int | None = None
        self.das_start: int = 0
        self.das_delay_ms: int = 170
        self.das_repeat_ms: int = 50
        self.das_last_repeat: int = 0

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.renderer = Renderer(_build_fonts())

        running = True
        while running:
            now = pygame.time.get_ticks()
            self.clock.tick(FPS)
            self.frame += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = handle_keydown(self.game, event.key)
                    # Track DAS for left/right
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.das_key = event.key
                        self.das_start = now
                        self.das_last_repeat = now
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.das_key = event.key
                        self.das_start = now
                        self.das_last_repeat = now
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.das_key = event.key
                        self.das_start = now
                        self.das_last_repeat = now
                elif event.type == pygame.KEYUP:
                    if event.key == self.das_key:
                        self.das_key = None

            # DAS auto-repeat
            if (
                self.das_key is not None
                and self.game.status == GameStatus.PLAYING
                and now - self.das_start >= self.das_delay_ms
                and now - self.das_last_repeat >= self.das_repeat_ms
            ):
                if self.das_key in (pygame.K_LEFT, pygame.K_a):
                    self.game.move_left()
                elif self.das_key in (pygame.K_RIGHT, pygame.K_d):
                    self.game.move_right()
                elif self.das_key in (pygame.K_DOWN, pygame.K_s):
                    self.game.soft_drop()
                self.das_last_repeat = now

            # Gravity tick
            if self.game.status == GameStatus.PLAYING:
                interval = self.game.tick_interval_ms()
                if now - self.last_step >= interval:
                    self.game.step()
                    self.last_step = now

            assert self.screen is not None and self.renderer is not None
            self.renderer.draw_frame(self.screen, self.game, self.frame)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main() -> None:
    TetrisApp().run()
