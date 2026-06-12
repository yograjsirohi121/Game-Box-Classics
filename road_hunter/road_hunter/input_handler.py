"""Keyboard input handling for Road Hunter."""

import pygame
from road_hunter.models import GameStatus
from road_hunter.game import RoadHunterGame

def handle_keydown(game: RoadHunterGame, key: int) -> bool:
    """Return False if the app should quit."""
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

    # Gameplay general keys
    if key == pygame.K_p:
        game.toggle_pause()
    elif key == pygame.K_r and game.status == GameStatus.GAME_OVER:
        game.reset()
    elif key == pygame.K_m and game.status in (GameStatus.GAME_OVER, GameStatus.PAUSED):
        game.return_to_menu()
        
    # Playing steering/acceleration keys
    if game.status == GameStatus.PLAYING:
        if key in (pygame.K_LEFT, pygame.K_a):
            game.input_left = True
        elif key in (pygame.K_RIGHT, pygame.K_d):
            game.input_right = True
        elif key in (pygame.K_UP, pygame.K_w):
            game.input_accel = True
        elif key in (pygame.K_DOWN, pygame.K_s):
            game.input_brake = True

    return True

def handle_keyup(game: RoadHunterGame, key: int) -> None:
    """Handle key release events for smooth analog-like driving controls."""
    if game.status == GameStatus.PLAYING:
        if key in (pygame.K_LEFT, pygame.K_a):
            game.input_left = False
        elif key in (pygame.K_RIGHT, pygame.K_d):
            game.input_right = False
        elif key in (pygame.K_UP, pygame.K_w):
            game.input_accel = False
        elif key in (pygame.K_DOWN, pygame.K_s):
            game.input_brake = False
