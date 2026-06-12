"""Tests for Tetris game logic."""

from tetris.config import COLS, ROWS, Difficulty
from tetris.game import TetrisGame
from tetris.models import GameStatus, RotationDir


def test_reset_clears_board_and_spawns_piece():
    game = TetrisGame()
    game.reset(Difficulty.EASY)
    assert game.status == GameStatus.PLAYING
    assert game.score == 0
    assert game.level == 1
    assert game.lines_cleared == 0
    assert len(game.board) == ROWS
    assert all(len(row) == COLS for row in game.board)
    # Board should be empty except where the active piece might be
    flat = [cell for row in game.board for cell in row]
    assert all(cell is None for cell in flat)


def test_move_left_and_right():
    game = TetrisGame()
    game.reset(Difficulty.MEDIUM)
    start_x = game.piece_x
    game.move_right()
    assert game.piece_x == start_x + 1
    game.move_left()
    assert game.piece_x == start_x


def test_soft_drop_moves_piece_down():
    game = TetrisGame()
    game.reset(Difficulty.EASY)
    start_y = game.piece_y
    game.soft_drop()
    assert game.piece_y == start_y + 1


def test_hard_drop_locks_piece():
    game = TetrisGame()
    game.reset(Difficulty.MEDIUM)
    game.hard_drop()
    # After hard-drop, a new piece should have spawned (piece_y near top)
    assert game.piece_y <= 1
    # At least some cells on the bottom rows should be filled
    bottom_row = game.board[ROWS - 1]
    assert any(cell is not None for cell in bottom_row)


def test_rotation():
    game = TetrisGame()
    game.reset(Difficulty.EASY)
    game.piece = "T"
    game.piece_x = COLS // 2 - 1
    game.piece_y = 2
    game.rotation = 0
    old_rot = game.rotation
    game.rotate(RotationDir.CW)
    assert game.rotation == (old_rot + 1) % 4


def test_line_clear_scoring():
    game = TetrisGame()
    game.reset(Difficulty.EASY)
    # Fill the bottom row completely
    for c in range(COLS):
        game.board[ROWS - 1][c] = "I"
    game._clear_lines()
    assert game.lines_cleared == 1
    assert game.score > 0
    # Bottom row should now be empty (shifted down)
    assert all(cell is None for cell in game.board[0])


def test_game_over_when_spawn_blocked():
    game = TetrisGame()
    game.reset(Difficulty.HARD)
    # Fill the top rows so spawning fails
    for r in range(4):
        for c in range(COLS):
            game.board[r][c] = "O"
    game._spawn_piece()
    assert game.status == GameStatus.GAME_OVER


def test_hold_swaps_piece():
    game = TetrisGame()
    game.reset(Difficulty.EASY)
    first = game.piece
    game.hold()
    assert game.held_piece == first
    assert game.hold_used is True


def test_hold_cannot_be_used_twice():
    game = TetrisGame()
    game.reset(Difficulty.EASY)
    game.hold()
    held_after_first = game.held_piece
    game.hold()  # Should be no-op
    assert game.held_piece == held_after_first


def test_ghost_y_at_bottom():
    game = TetrisGame()
    game.reset(Difficulty.EASY)
    gy = game.ghost_y()
    assert gy >= game.piece_y
    assert gy < ROWS


def test_wall_prevents_left_move():
    game = TetrisGame()
    game.reset(Difficulty.EASY)
    game.piece = "O"
    game.rotation = 0
    game.piece_x = -1  # far left
    # The O-piece cells are at (1,0),(2,0),(1,1),(2,1) relative
    # Set piece_x to 0 so leftmost cell is at col 0
    game.piece_x = 0
    game.piece_y = 5
    result = game.move_left()
    # Should fail because O-piece would go to (-1 + 1) = col 0 for the leftmost cell
    # Actually O has offset (1,0) so at piece_x=-1, the leftmost would be col 0
    # Let's just check it returns False when against wall
    game.piece_x = -1
    result = game.move_left()
    assert result is False


def test_hard_is_faster_than_easy():
    easy = TetrisGame()
    easy.reset(Difficulty.EASY)
    hard = TetrisGame()
    hard.reset(Difficulty.HARD)
    assert hard.tick_interval_ms() < easy.tick_interval_ms()


def test_speed_increases_with_level():
    game = TetrisGame()
    game.reset(Difficulty.MEDIUM)
    start = game.tick_interval_ms()
    game.level = 5
    assert game.tick_interval_ms() < start


def test_toggle_pause():
    game = TetrisGame()
    game.reset(Difficulty.EASY)
    assert game.status == GameStatus.PLAYING
    game.toggle_pause()
    assert game.status == GameStatus.PAUSED
    game.toggle_pause()
    assert game.status == GameStatus.PLAYING


def test_return_to_menu():
    game = TetrisGame()
    game.reset(Difficulty.MEDIUM)
    game.score = 500
    game.return_to_menu()
    assert game.status == GameStatus.MENU
    assert game.score == 0
