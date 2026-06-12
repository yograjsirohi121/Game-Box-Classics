"""Minimal, aesthetic pygame rendering for Tetris."""

import pygame

from tetris.config import (
    ACCENT,
    BG,
    BORDER,
    CELL,
    COLS,
    DIFFICULTY_LABELS,
    DIFFICULTY_ORDER,
    GHOST_ALPHA,
    GRID_LINE,
    HEADER_BG,
    HEADER_H,
    HEIGHT,
    MENU_HOVER,
    OVERLAY,
    PADDING,
    PIECE_COLOURS,
    PLAY_BG,
    PLAY_H,
    PLAY_W,
    ROWS,
    SIDEBAR_BG,
    SIDEBAR_W,
    TEXT,
    TEXT_DIM,
    WIDTH,
)
from tetris.game import TetrisGame
from tetris.models import GameStatus, TETROMINOES


def _play_origin() -> tuple[int, int]:
    return PADDING, HEADER_H + PADDING


def _cell_rect(col: int, row: int, ox: int, oy: int) -> pygame.Rect:
    return pygame.Rect(ox + col * CELL, oy + row * CELL, CELL, CELL)


def _darken(colour: tuple[int, int, int], factor: float = 0.55) -> tuple[int, int, int]:
    return (int(colour[0] * factor), int(colour[1] * factor), int(colour[2] * factor))


def _lighten(colour: tuple[int, int, int], amount: int = 40) -> tuple[int, int, int]:
    return (
        min(255, colour[0] + amount),
        min(255, colour[1] + amount),
        min(255, colour[2] + amount),
    )


class Renderer:
    def __init__(self, fonts: dict[str, pygame.font.Font]) -> None:
        self.fonts = fonts

    def draw_frame(self, surface: pygame.Surface, game: TetrisGame, tick: int) -> None:
        surface.fill(BG)
        self._draw_header(surface, game)

        ox, oy = _play_origin()
        self._draw_playfield(surface, ox, oy)

        if game.status == GameStatus.MENU:
            self._draw_menu(surface, game)
        else:
            self._draw_locked_blocks(surface, game, ox, oy)
            self._draw_ghost(surface, game, ox, oy)
            self._draw_active_piece(surface, game, ox, oy)
            self._draw_sidebar(surface, game, ox, oy)

            if game.status == GameStatus.PAUSED:
                self._draw_banner(surface, "PAUSED", "Press P to resume")
            elif game.status == GameStatus.GAME_OVER:
                self._draw_banner(
                    surface,
                    "GAME OVER",
                    f"Score {game.score}  ·  Press R to retry",
                )

    # ── Header ────────────────────────────────────────────────────

    def _draw_header(self, surface: pygame.Surface, game: TetrisGame) -> None:
        header = pygame.Rect(0, 0, WIDTH, HEADER_H)
        pygame.draw.rect(surface, HEADER_BG, header)
        pygame.draw.line(surface, BORDER, (0, HEADER_H - 1), (WIDTH, HEADER_H - 1))

        title = self.fonts["title"].render("TETRIS", True, ACCENT)
        surface.blit(title, (PADDING, (HEADER_H - title.get_height()) // 2))

        if game.status != GameStatus.MENU:
            info = f"{DIFFICULTY_LABELS[game.difficulty]}  ·  Lv {game.level}"
            score = f"{game.score:05d}"
            info_s = self.fonts["small"].render(info, True, TEXT_DIM)
            score_s = self.fonts["score"].render(score, True, TEXT)
            surface.blit(info_s, (WIDTH - PADDING - info_s.get_width(), 10))
            surface.blit(score_s, (WIDTH - PADDING - score_s.get_width(), 28))

    # ── Playfield ─────────────────────────────────────────────────

    def _draw_playfield(self, surface: pygame.Surface, ox: int, oy: int) -> None:
        field = pygame.Rect(ox - 2, oy - 2, PLAY_W + 4, PLAY_H + 4)
        pygame.draw.rect(surface, PLAY_BG, (ox, oy, PLAY_W, PLAY_H))
        pygame.draw.rect(surface, BORDER, field, 2)

        for c in range(COLS + 1):
            x = ox + c * CELL
            pygame.draw.line(surface, GRID_LINE, (x, oy), (x, oy + PLAY_H))
        for r in range(ROWS + 1):
            y = oy + r * CELL
            pygame.draw.line(surface, GRID_LINE, (ox, y), (ox + PLAY_W, y))

    # ── Locked blocks ─────────────────────────────────────────────

    def _draw_locked_blocks(
        self, surface: pygame.Surface, game: TetrisGame, ox: int, oy: int
    ) -> None:
        for r in range(ROWS):
            for c in range(COLS):
                cell = game.board[r][c]
                if cell is not None:
                    self._draw_block(surface, c, r, ox, oy, PIECE_COLOURS[cell])

    # ── Active piece + ghost ──────────────────────────────────────

    def _draw_active_piece(
        self, surface: pygame.Surface, game: TetrisGame, ox: int, oy: int
    ) -> None:
        colour = PIECE_COLOURS[game.piece]
        for x, y in game._cells():
            if y >= 0:
                self._draw_block(surface, x, y, ox, oy, colour)

    def _draw_ghost(
        self, surface: pygame.Surface, game: TetrisGame, ox: int, oy: int
    ) -> None:
        gy = game.ghost_y()
        if gy == game.piece_y:
            return
        colour = PIECE_COLOURS[game.piece]
        ghost_surface = pygame.Surface((CELL - 2, CELL - 2), pygame.SRCALPHA)
        ghost_surface.fill((*colour, GHOST_ALPHA))
        for cx, cy in TETROMINOES[game.piece][game.rotation % 4]:
            bx = game.piece_x + cx
            by = gy + cy
            if by >= 0:
                rect = _cell_rect(bx, by, ox, oy).inflate(-2, -2)
                surface.blit(ghost_surface, rect.topleft)

    def _draw_block(
        self,
        surface: pygame.Surface,
        col: int,
        row: int,
        ox: int,
        oy: int,
        colour: tuple[int, int, int],
    ) -> None:
        rect = _cell_rect(col, row, ox, oy).inflate(-2, -2)
        pygame.draw.rect(surface, colour, rect, border_radius=3)
        # Top-left highlight
        highlight = pygame.Rect(rect.x + 1, rect.y + 1, rect.width - 2, 3)
        pygame.draw.rect(surface, _lighten(colour, 50), highlight, border_radius=1)
        # Bottom-right shadow
        shadow = pygame.Rect(rect.x + 1, rect.bottom - 4, rect.width - 2, 3)
        pygame.draw.rect(surface, _darken(colour, 0.6), shadow, border_radius=1)

    # ── Sidebar (next, hold, lines) ───────────────────────────────

    def _draw_sidebar(
        self, surface: pygame.Surface, game: TetrisGame, ox: int, oy: int
    ) -> None:
        sx = ox + PLAY_W + PADDING
        sy = oy

        # Background panel
        panel = pygame.Rect(sx - 4, sy - 4, SIDEBAR_W + 8, PLAY_H + 8)
        pygame.draw.rect(surface, SIDEBAR_BG, panel, border_radius=4)
        pygame.draw.rect(surface, BORDER, panel, 1, border_radius=4)

        # Next piece
        label = self.fonts["small"].render("NEXT", True, TEXT_DIM)
        surface.blit(label, (sx + 8, sy + 8))
        self._draw_mini_piece(surface, game.next_piece, sx + 12, sy + 30)

        # Hold piece
        label = self.fonts["small"].render("HOLD", True, TEXT_DIM)
        surface.blit(label, (sx + 8, sy + 115))
        if game.held_piece is not None:
            alpha = 120 if game.hold_used else 255
            self._draw_mini_piece(surface, game.held_piece, sx + 12, sy + 137, alpha)

        # Stats
        stats_y = sy + 230
        for lbl, val in [("LINES", str(game.lines_cleared)), ("LEVEL", str(game.level))]:
            label = self.fonts["small"].render(lbl, True, TEXT_DIM)
            surface.blit(label, (sx + 8, stats_y))
            value = self.fonts["score"].render(val, True, TEXT)
            surface.blit(value, (sx + 8, stats_y + 18))
            stats_y += 56

    def _draw_mini_piece(
        self,
        surface: pygame.Surface,
        piece: str,
        x: int,
        y: int,
        alpha: int = 255,
    ) -> None:
        mini = 18
        colour = PIECE_COLOURS[piece]
        for cx, cy in TETROMINOES[piece][0]:
            rect = pygame.Rect(x + cx * mini, y + cy * mini, mini - 2, mini - 2)
            if alpha < 255:
                s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                s.fill((*colour, alpha))
                surface.blit(s, rect.topleft)
            else:
                pygame.draw.rect(surface, colour, rect, border_radius=2)

    # ── Menu ──────────────────────────────────────────────────────

    def _draw_menu(self, surface: pygame.Surface, game: TetrisGame) -> None:
        ox, oy = _play_origin()
        overlay = pygame.Surface((PLAY_W, PLAY_H), pygame.SRCALPHA)
        overlay.fill(MENU_HOVER)
        surface.blit(overlay, (ox, oy))

        cx = ox + PLAY_W // 2
        y = oy + 50

        prompt = self.fonts["small"].render("Select difficulty", True, TEXT_DIM)
        surface.blit(prompt, prompt.get_rect(centerx=cx, top=y))
        y += 44

        for i, difficulty in enumerate(DIFFICULTY_ORDER):
            selected = i == game.menu_index
            label = DIFFICULTY_LABELS[difficulty]
            prefix = "▸ " if selected else "  "
            color = ACCENT if selected else TEXT
            text = self.fonts["menu"].render(f"{prefix}{label}", True, color)
            surface.blit(text, text.get_rect(centerx=cx, top=y))
            y += 40

        y = oy + PLAY_H - 100
        hints = [
            "↑ ↓  choose",
            "Enter  start",
            "Esc  quit",
        ]
        for hint in hints:
            line = self.fonts["small"].render(hint, True, TEXT_DIM)
            surface.blit(line, line.get_rect(centerx=cx, top=y))
            y += 22

    # ── Overlay banners ───────────────────────────────────────────

    def _draw_banner(self, surface: pygame.Surface, title: str, subtitle: str) -> None:
        ox, oy = _play_origin()
        overlay = pygame.Surface((PLAY_W, PLAY_H), pygame.SRCALPHA)
        overlay.fill(OVERLAY)
        surface.blit(overlay, (ox, oy))

        cx = ox + PLAY_W // 2
        cy = oy + PLAY_H // 2
        main = self.fonts["banner"].render(title, True, TEXT)
        sub = self.fonts["small"].render(subtitle, True, TEXT_DIM)
        surface.blit(main, main.get_rect(center=(cx, cy - 16)))
        surface.blit(sub, sub.get_rect(center=(cx, cy + 18)))
