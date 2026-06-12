"""Application bootstrap and main game loop."""

import sys

import pygame

from wordle.config import FPS, HEIGHT, REVEAL_MS, WIDTH
from wordle.dictionary import load_word_lists
from wordle.input_handler import handle_click, handle_keydown
from wordle.models import Game
from wordle.renderer import Renderer


def _build_fonts() -> dict[str, pygame.font.Font]:
    return {
        "title": pygame.font.SysFont("arial", 28, bold=True),
        "tile": pygame.font.SysFont("arial", 32, bold=True),
        "key": pygame.font.SysFont("arial", 14, bold=True),
        "msg": pygame.font.SysFont("arial", 13, bold=True),
        "overlay": pygame.font.SysFont("arial", 36, bold=True),
        "hint": pygame.font.SysFont("arial", 18),
    }


class WordleApp:
    """Orchestrates pygame initialization, events, and rendering."""

    def __init__(self) -> None:
        answers, valid_words = load_word_lists()
        self.game = Game.new(answers, valid_words)
        self.renderer: Renderer | None = None
        self.screen: pygame.Surface | None = None
        self.clock = pygame.time.Clock()
        self.last_reveal = 0
        self.clickable: list[tuple[pygame.Rect, str]] = []

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("Wordle")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.renderer = Renderer(_build_fonts())

        running = True
        while running:
            now = pygame.time.get_ticks()
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = handle_keydown(self.game, event.key, now)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    handle_click(self.game, event.pos, self.clickable, now)

            if self.game.is_animating() and now - self.last_reveal >= REVEAL_MS:
                self.game.advance_reveal(now)
                self.last_reveal = now

            assert self.screen is not None and self.renderer is not None
            self.clickable = self.renderer.draw_frame(self.screen, self.game, now)
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main() -> None:
    WordleApp().run()
