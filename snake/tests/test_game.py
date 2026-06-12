"""Tests for Snake game logic."""

from snake.config import COLS, ROWS, Difficulty
from snake.game import SnakeGame
from snake.models import Direction, GameStatus


def test_reset_places_snake_and_food():
    game = SnakeGame()
    game.reset(Difficulty.EASY)
    assert game.status == GameStatus.PLAYING
    assert len(game.snake) == 3
    assert game.food not in game.snake
    assert 0 <= game.food[0] < COLS
    assert 0 <= game.food[1] < ROWS


def test_eating_food_grows_snake():
    game = SnakeGame()
    game.reset(Difficulty.EASY)
    head_c, head_r = game.snake[0]
    game.food = (head_c + 1, head_r)
    game.direction = Direction.RIGHT
    game.queued_direction = Direction.RIGHT
    length_before = len(game.snake)
    game.step()
    assert len(game.snake) == length_before + 1
    assert game.score > 0
    assert game.foods_eaten == 1


def test_wall_collision_ends_game():
    game = SnakeGame()
    game.reset(Difficulty.HARD)
    game.snake = [(COLS - 1, 0)]
    game.direction = Direction.RIGHT
    game.queued_direction = Direction.RIGHT
    game.step()
    assert game.status == GameStatus.GAME_OVER


def test_self_collision_ends_game():
    game = SnakeGame()
    game.reset(Difficulty.MEDIUM)
    game.snake = [(5, 5), (4, 5), (4, 6), (5, 6), (6, 6), (6, 5), (6, 4), (5, 4)]
    game.direction = Direction.DOWN
    game.queued_direction = Direction.DOWN
    game.step()
    assert game.status == GameStatus.GAME_OVER


def test_cannot_reverse_into_self():
    game = SnakeGame()
    game.reset(Difficulty.EASY)
    game.direction = Direction.RIGHT
    game.queued_direction = Direction.RIGHT
    game.queue_direction(Direction.LEFT)
    assert game.queued_direction == Direction.RIGHT


def test_hard_is_faster_than_easy():
    easy = SnakeGame()
    easy.reset(Difficulty.EASY)
    hard = SnakeGame()
    hard.reset(Difficulty.HARD)
    assert hard.tick_interval_ms() < easy.tick_interval_ms()


def test_speed_increases_after_food():
    game = SnakeGame()
    game.reset(Difficulty.MEDIUM)
    start = game.tick_interval_ms()
    game.foods_eaten = 5
    assert game.tick_interval_ms() < start
