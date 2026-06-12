"""Application bootstrap and main loop."""

import sys

import pygame

from snake.config import FPS, HEIGHT, WIDTH
from snake.game import SnakeGame
from snake.input_handler import handle_keydown
from snake.models import GameStatus
from snake.renderer import Renderer


def _build_fonts() -> dict[str, pygame.font.Font]:
    return {
        "title": pygame.font.SysFont("consolas", 22, bold=True),
        "score": pygame.font.SysFont("consolas", 20, bold=True),
        "menu": pygame.font.SysFont("consolas", 24),
        "banner": pygame.font.SysFont("consolas", 28, bold=True),
        "small": pygame.font.SysFont("consolas", 14),
    }


class SnakeApp:
    def __init__(self) -> None:
        self.game = SnakeGame()
        self.renderer: Renderer | None = None
        self.screen: pygame.Surface | None = None
        self.clock = pygame.time.Clock()
        self.last_step = 0
        self.frame = 0

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("Snake")
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
    SnakeApp().run()
