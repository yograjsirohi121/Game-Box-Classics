"""Minimal Nokia-inspired pygame rendering."""

import pygame

from snake.config import (
    ACCENT,
    BG,
    BORDER,
    CELL,
    COLS,
    DIFFICULTY_LABELS,
    DIFFICULTY_ORDER,
    FOOD,
    FOOD_GLOW,
    GRID,
    HEADER_BG,
    HEADER_H,
    HEIGHT,
    MENU_HOVER,
    OVERLAY,
    PADDING,
    PLAY_BG,
    PLAY_H,
    PLAY_W,
    ROWS,
    SNAKE_BODY,
    SNAKE_BODY_DARK,
    SNAKE_HEAD,
    TEXT,
    TEXT_DIM,
    WIDTH,
)
from snake.game import SnakeGame
from snake.models import GameStatus


def _play_origin() -> tuple[int, int]:
    x = PADDING
    y = HEADER_H + PADDING
    return x, y


def _cell_rect(col: int, row: int, ox: int, oy: int) -> pygame.Rect:
    return pygame.Rect(ox + col * CELL, oy + row * CELL, CELL, CELL)


class Renderer:
    def __init__(self, fonts: dict[str, pygame.font.Font]) -> None:
        self.fonts = fonts

    def draw_frame(self, surface: pygame.Surface, game: SnakeGame, tick: int) -> None:
        surface.fill(BG)
        self._draw_header(surface, game)

        ox, oy = _play_origin()
        self._draw_playfield(surface, ox, oy)

        if game.status == GameStatus.MENU:
            self._draw_menu(surface, game)
        else:
            self._draw_food(surface, game, ox, oy, tick)
            self._draw_snake(surface, game, ox, oy)
            if game.status == GameStatus.PAUSED:
                self._draw_banner(surface, "PAUSED", "Press P to resume")
            elif game.status == GameStatus.GAME_OVER:
                self._draw_banner(
                    surface,
                    "GAME OVER",
                    f"Score {game.score}  ·  Press R to retry",
                )

    def _draw_header(self, surface: pygame.Surface, game: SnakeGame) -> None:
        header = pygame.Rect(0, 0, WIDTH, HEADER_H)
        pygame.draw.rect(surface, HEADER_BG, header)
        pygame.draw.line(surface, BORDER, (0, HEADER_H - 1), (WIDTH, HEADER_H - 1))

        title = self.fonts["title"].render("SNAKE", True, ACCENT)
        surface.blit(title, (PADDING, (HEADER_H - title.get_height()) // 2))

        if game.status != GameStatus.MENU:
            info = f"{DIFFICULTY_LABELS[game.difficulty]}  ·  {game.length}"
            score = f"{game.score:04d}"
            info_s = self.fonts["small"].render(info, True, TEXT_DIM)
            score_s = self.fonts["score"].render(score, True, TEXT)
            surface.blit(info_s, (WIDTH - PADDING - info_s.get_width(), 10))
            surface.blit(score_s, (WIDTH - PADDING - score_s.get_width(), 28))

    def _draw_playfield(self, surface: pygame.Surface, ox: int, oy: int) -> None:
        field = pygame.Rect(ox - 2, oy - 2, PLAY_W + 4, PLAY_H + 4)
        pygame.draw.rect(surface, PLAY_BG, (ox, oy, PLAY_W, PLAY_H))
        pygame.draw.rect(surface, BORDER, field, 2)

        for c in range(COLS + 1):
            x = ox + c * CELL
            pygame.draw.line(surface, GRID, (x, oy), (x, oy + PLAY_H))
        for r in range(ROWS + 1):
            y = oy + r * CELL
            pygame.draw.line(surface, GRID, (ox, y), (ox + PLAY_W, y))

    def _draw_snake(self, surface: pygame.Surface, game: SnakeGame, ox: int, oy: int) -> None:
        for i, (col, row) in enumerate(game.snake):
            rect = _cell_rect(col, row, ox, oy).inflate(-2, -2)
            if i == 0:
                pygame.draw.rect(surface, SNAKE_HEAD, rect, border_radius=3)
                eye = max(2, CELL // 8)
                ex = rect.right - eye * 2
                ey = rect.top + eye * 2
                pygame.draw.rect(surface, PLAY_BG, (ex, ey, eye, eye))
            else:
                shade = SNAKE_BODY if i % 2 == 0 else SNAKE_BODY_DARK
                pygame.draw.rect(surface, shade, rect, border_radius=2)

    def _draw_food(
        self,
        surface: pygame.Surface,
        game: SnakeGame,
        ox: int,
        oy: int,
        tick: int,
    ) -> None:
        col, row = game.food
        rect = _cell_rect(col, row, ox, oy)
        center = rect.center
        pulse = 4 + (tick // 8) % 2
        pygame.draw.circle(surface, FOOD_GLOW, center, CELL // 2 - 2)
        pygame.draw.circle(surface, FOOD, center, CELL // 2 - pulse)

    def _draw_menu(self, surface: pygame.Surface, game: SnakeGame) -> None:
        ox, oy = _play_origin()
        overlay = pygame.Surface((PLAY_W, PLAY_H), pygame.SRCALPHA)
        overlay.fill(MENU_HOVER)
        surface.blit(overlay, (ox, oy))

        cx = WIDTH // 2
        y = oy + 36

        prompt = self.fonts["small"].render("Select difficulty", True, TEXT_DIM)
        surface.blit(prompt, prompt.get_rect(centerx=cx, top=y))
        y += 40

        for i, difficulty in enumerate(DIFFICULTY_ORDER):
            selected = i == game.menu_index
            label = DIFFICULTY_LABELS[difficulty]
            prefix = "▸ " if selected else "  "
            color = ACCENT if selected else TEXT
            text = self.fonts["menu"].render(f"{prefix}{label}", True, color)
            surface.blit(text, text.get_rect(centerx=cx, top=y))
            y += 36

        y = oy + PLAY_H - 72
        hints = ["↑ ↓  choose", "Enter  start", "Esc  quit"]
        for hint in hints:
            line = self.fonts["small"].render(hint, True, TEXT_DIM)
            surface.blit(line, line.get_rect(centerx=cx, top=y))
            y += 22

    def _draw_banner(self, surface: pygame.Surface, title: str, subtitle: str) -> None:
        ox, oy = _play_origin()
        overlay = pygame.Surface((PLAY_W, PLAY_H), pygame.SRCALPHA)
        overlay.fill(OVERLAY)
        surface.blit(overlay, (ox, oy))

        cx = WIDTH // 2
        cy = oy + PLAY_H // 2
        main = self.fonts["banner"].render(title, True, TEXT)
        sub = self.fonts["small"].render(subtitle, True, TEXT_DIM)
        surface.blit(main, main.get_rect(center=(cx, cy - 16)))
        surface.blit(sub, sub.get_rect(center=(cx, cy + 18)))
