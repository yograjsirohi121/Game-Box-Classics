"""Keyboard input handling."""

import pygame

from tetris.game import TetrisGame
from tetris.models import GameStatus, RotationDir


def handle_keydown(game: TetrisGame, key: int) -> bool:
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

    if game.status == GameStatus.PLAYING:
        if key in (pygame.K_LEFT, pygame.K_a):
            game.move_left()
        elif key in (pygame.K_RIGHT, pygame.K_d):
            game.move_right()
        elif key in (pygame.K_DOWN, pygame.K_s):
            game.soft_drop()
        elif key in (pygame.K_UP, pygame.K_w):
            game.rotate(RotationDir.CW)
        elif key == pygame.K_z:
            game.rotate(RotationDir.CCW)
        elif key == pygame.K_SPACE:
            game.hard_drop()
        elif key == pygame.K_c:
            game.hold()

    if key == pygame.K_p:
        game.toggle_pause()
    elif key == pygame.K_r and game.status == GameStatus.GAME_OVER:
        game.reset()
    elif key == pygame.K_m and game.status in (GameStatus.GAME_OVER, GameStatus.PAUSED):
        game.return_to_menu()

    return True
