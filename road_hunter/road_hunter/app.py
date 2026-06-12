"""Application bootstrap and main loop for Road Hunter."""

import sys
import pygame
from road_hunter.config import FPS, HEIGHT, WIDTH
from road_hunter.game import RoadHunterGame
from road_hunter.input_handler import handle_keydown, handle_keyup
from road_hunter.models import GameStatus
from road_hunter.renderer import Renderer

def _build_fonts() -> dict[str, pygame.font.Font]:
    return {
        "title": pygame.font.SysFont("consolas", 22, bold=True),
        "score": pygame.font.SysFont("consolas", 20, bold=True),
        "menu": pygame.font.SysFont("consolas", 24),
        "banner": pygame.font.SysFont("consolas", 28, bold=True),
        "small": pygame.font.SysFont("consolas", 14),
    }

class RoadHunterApp:
    def __init__(self) -> None:
        self.game = RoadHunterGame()
        self.renderer: Renderer | None = None
        self.screen: pygame.Surface | None = None
        self.clock = pygame.time.Clock()
        self.frame = 0

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("Road Hunter")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.renderer = Renderer(_build_fonts())

        running = True
        while running:
            self.clock.tick(FPS)
            self.frame += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = handle_keydown(self.game, event.key)
                elif event.type == pygame.KEYUP:
                    handle_keyup(self.game, event.key)

            # Update game logic at 60 FPS
            if self.game.status == GameStatus.PLAYING:
                self.game.step()

            assert self.screen is not None and self.renderer is not None
            self.renderer.draw_frame(self.screen, self.game, self.frame)
            pygame.display.flip()

        pygame.quit()
        sys.exit()

def main() -> None:
    RoadHunterApp().run()
