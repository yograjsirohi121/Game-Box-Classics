"""Keyboard and mouse input handling."""

import pygame

from wordle.models import Game


def handle_keydown(game: Game, key: int, now: int) -> bool:
    """Process a key press. Returns False when the app should quit."""
    if key in (pygame.K_ESCAPE, pygame.K_q):
        return False
    if key == pygame.K_n:
        game.start_round()
        return True
    if key == pygame.K_RETURN:
        game.submit(now)
    elif key == pygame.K_BACKSPACE:
        game.delete_letter()
    elif pygame.K_a <= key <= pygame.K_z:
        game.type_letter(chr(key))
    return True


def handle_click(
    game: Game,
    pos: tuple[int, int],
    clickable: list[tuple[pygame.Rect, str]],
    now: int,
) -> None:
    for rect, key in clickable:
        if rect.collidepoint(pos):
            if key == "enter":
                game.submit(now)
            elif key == "back":
                game.delete_letter()
            else:
                game.type_letter(key)
            break
