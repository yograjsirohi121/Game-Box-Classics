"""Pygame rendering for the Wordle board and keyboard."""

import pygame

from wordle.config import (
    BG,
    BOARD_W,
    BORDER_EMPTY,
    HEIGHT,
    KEY_ABSENT_DARK,
    KEY_ABSENT_LIGHT,
    KEY_BG_DARK,
    KEY_BG_LIGHT,
    KEY_GAP,
    KEY_H,
    KEY_TEXT,
    KEYBOARD_ROWS,
    MAX_GUESSES,
    MUTED,
    STATE_GRADIENTS,
    TEXT,
    TEXT_ABSENT,
    TILE,
    TILE_GAP,
    TILE_GRADIENTS,
    WIDTH,
    WORD_LENGTH,
)
from wordle.models import Game, GameStatus, KeyState


def _lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def _lerp_color(
    top: tuple[int, int, int],
    bottom: tuple[int, int, int],
    t: float,
) -> tuple[int, int, int]:
    return (_lerp(top[0], bottom[0], t), _lerp(top[1], bottom[1], t), _lerp(top[2], bottom[2], t))


def _draw_gradient_rect(
    surface: pygame.Surface,
    rect: pygame.Rect,
    top_color: tuple[int, int, int],
    bottom_color: tuple[int, int, int],
    border_radius: int = 4,
) -> None:
    if rect.height <= 0 or rect.width <= 0:
        return

    gradient = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    for y in range(rect.height):
        color = _lerp_color(top_color, bottom_color, y / max(rect.height - 1, 1))
        pygame.draw.line(gradient, (*color, 255), (0, y), (rect.width, y))

    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), mask.get_rect(), border_radius=border_radius)
    gradient.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surface.blit(gradient, rect.topleft)


def _tile_rect(row: int, col: int, board_x: int, board_y: int) -> pygame.Rect:
    x = board_x + col * (TILE + TILE_GAP)
    y = board_y + row * (TILE + TILE_GAP)
    return pygame.Rect(x, y, TILE, TILE)


def _draw_tile(
    surface: pygame.Surface,
    rect: pygame.Rect,
    letter: str,
    state: str | None,
    fonts: dict[str, pygame.font.Font],
) -> None:
    if state and state in STATE_GRADIENTS:
        top, bottom = STATE_GRADIENTS[state]
        _draw_gradient_rect(surface, rect, top, bottom)
        border = bottom
        text_color = TEXT_ABSENT if state == "absent" else TEXT
    elif letter:
        top, bottom = TILE_GRADIENTS["active"]
        _draw_gradient_rect(surface, rect, top, bottom)
        border = BORDER_EMPTY
        text_color = TEXT
    else:
        top, bottom = TILE_GRADIENTS["empty"]
        _draw_gradient_rect(surface, rect, top, bottom, border_radius=4)
        pygame.draw.rect(surface, BORDER_EMPTY, rect, 2, border_radius=4)
        return

    pygame.draw.rect(surface, border, rect, 2, border_radius=4)

    if letter:
        text = fonts["tile"].render(letter.upper(), True, text_color)
        surface.blit(text, text.get_rect(center=rect.center))


def _key_gradient(state: KeyState) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    if state == KeyState.CORRECT:
        return STATE_GRADIENTS["correct"]
    if state == KeyState.PRESENT:
        return STATE_GRADIENTS["present"]
    if state == KeyState.ABSENT:
        return KEY_ABSENT_LIGHT, KEY_ABSENT_DARK
    return KEY_BG_LIGHT, KEY_BG_DARK


def _key_text_color(state: KeyState) -> tuple[int, int, int]:
    if state == KeyState.ABSENT:
        return TEXT_ABSENT
    return KEY_TEXT


class Renderer:
    """Draws all game UI elements onto a pygame surface."""

    def __init__(self, fonts: dict[str, pygame.font.Font]) -> None:
        self.fonts = fonts

    def draw_frame(self, surface: pygame.Surface, game: Game, now: int) -> list[tuple[pygame.Rect, str]]:
        surface.fill(BG)
        self.draw_header(surface, game, now)
        board_y = self.draw_board(surface, game)
        clickable = self.draw_keyboard(surface, game, board_y)
        self.draw_overlay(surface, game)
        return clickable

    def draw_header(self, surface: pygame.Surface, game: Game, now: int) -> None:
        title = self.fonts["title"].render("WORDLE", True, TEXT)
        surface.blit(title, title.get_rect(centerx=WIDTH // 2, top=24))

        if game.message and now < game.message_until:
            msg = self.fonts["msg"].render(game.message, True, TEXT)
            bg = pygame.Rect(0, 0, msg.get_width() + 24, msg.get_height() + 12)
            bg.center = (WIDTH // 2, 62)
            pygame.draw.rect(surface, TEXT, bg, border_radius=4)
            surface.blit(msg, msg.get_rect(center=bg.center))

    def draw_board(self, surface: pygame.Surface, game: Game) -> int:
        board_x = (WIDTH - BOARD_W) // 2
        board_y = 90

        for row in range(MAX_GUESSES):
            for col in range(WORD_LENGTH):
                rect = _tile_rect(row, col, board_x, board_y)
                letter = game.tile_letter(row, col)
                state = game.tile_state(row, col)
                _draw_tile(surface, rect, letter, state, self.fonts)

        return board_y

    def draw_keyboard(
        self,
        surface: pygame.Surface,
        game: Game,
        board_y: int,
    ) -> list[tuple[pygame.Rect, str]]:
        start_y = board_y + MAX_GUESSES * (TILE + TILE_GAP) + 36
        clickable: list[tuple[pygame.Rect, str]] = []
        key_font = self.fonts["key"]

        for row_idx, row in enumerate(KEYBOARD_ROWS):
            keys = ["enter"] + list(row) + ["back"] if row_idx == 2 else list(row)
            key_w = 43
            key_ws = [66] + [43] * len(row) + [66] if row_idx == 2 else [key_w] * len(keys)
            total_w = sum(key_ws) + KEY_GAP * (len(keys) - 1)

            x = (WIDTH - total_w) // 2
            y = start_y + row_idx * (KEY_H + KEY_GAP)

            for i, key in enumerate(keys):
                w = key_ws[i]
                rect = pygame.Rect(x, y, w, KEY_H)
                state = game.key_states.get(key, KeyState.UNUSED) if len(key) == 1 else KeyState.UNUSED
                top, bottom = _key_gradient(state)
                _draw_gradient_rect(surface, rect, top, bottom)
                pygame.draw.rect(surface, bottom, rect, 1, border_radius=4)

                text_color = _key_text_color(state)
                if key == "enter":
                    text = key_font.render("ENTER", True, text_color)
                elif key == "back":
                    text = key_font.render("⌫", True, text_color)
                else:
                    text = key_font.render(key.upper(), True, text_color)
                surface.blit(text, text.get_rect(center=rect.center))

                clickable.append((rect, key))
                x += w + KEY_GAP

        return clickable

    def draw_overlay(self, surface: pygame.Surface, game: Game) -> None:
        if game.status == GameStatus.PLAYING:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        if game.status == GameStatus.WON:
            headline = "You Win!"
            sub = f"The word was {game.answer.upper()}"
        else:
            headline = "Game Over"
            sub = f"Answer: {game.answer.upper()}"

        main = self.fonts["overlay"].render(headline, True, TEXT)
        hint = self.fonts["hint"].render(sub, True, MUTED)
        restart = self.fonts["hint"].render("Press N for a new game", True, TEXT)

        cy = HEIGHT // 2
        surface.blit(main, main.get_rect(center=(WIDTH // 2, cy - 30)))
        surface.blit(hint, hint.get_rect(center=(WIDTH // 2, cy + 10)))
        surface.blit(restart, restart.get_rect(center=(WIDTH // 2, cy + 50)))
