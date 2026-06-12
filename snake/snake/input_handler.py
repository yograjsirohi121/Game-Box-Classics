"""Keyboard input handling."""

import pygame

from snake.models import Direction, GameStatus
from snake.game import SnakeGame

DIRECTION_KEYS = {
    pygame.K_UP: Direction.UP,
    pygame.K_w: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_s: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_a: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
    pygame.K_d: Direction.RIGHT,
}


def handle_keydown(game: SnakeGame, key: int) -> bool:
    """Return False when the app should quit."""
    if key in (pygame.K_ESCAPE, pygame.K_q):
        return False

    if game.status == GameStatus.MENU:
        if key in (pygame.K_UP, pygame.K_w):
            game.menu_up()
        elif key in (pygame.K_DOWN, pygame.K_s):
            game.menu_down()
        elif key == pygame.K_1:
            game.menu_index = 0
        elif key == pygame.K_2:
            game.menu_index = 1
        elif key == pygame.K_3:
            game.menu_index = 2
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            game.start_from_menu()
        return True

    if key == pygame.K_p:
        game.toggle_pause()
    elif key == pygame.K_r and game.status == GameStatus.GAME_OVER:
        game.reset()
    elif key == pygame.K_m and game.status in (GameStatus.GAME_OVER, GameStatus.PAUSED):
        game.return_to_menu()
    elif key in DIRECTION_KEYS:
        game.queue_direction(DIRECTION_KEYS[key])

    return True
