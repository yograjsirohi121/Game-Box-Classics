"""Core Snake game logic (no pygame dependencies)."""

import random
from dataclasses import dataclass, field

from snake.config import (
    COLS,
    DIFFICULTY_ORDER,
    DIFFICULTY_SETTINGS,
    ROWS,
    Difficulty,
)
from snake.models import Direction, GameStatus


def _random_empty_cell(occupied: set[tuple[int, int]]) -> tuple[int, int]:
    free = [(c, r) for r in range(ROWS) for c in range(COLS) if (c, r) not in occupied]
    if not free:
        raise RuntimeError("Board is full")
    return random.choice(free)


@dataclass
class SnakeGame:
    difficulty: Difficulty = Difficulty.MEDIUM
    status: GameStatus = GameStatus.MENU
    snake: list[tuple[int, int]] = field(default_factory=list)
    direction: Direction = Direction.RIGHT
    queued_direction: Direction = Direction.RIGHT
    food: tuple[int, int] = (0, 0)
    score: int = 0
    foods_eaten: int = 0
    menu_index: int = 0

    def reset(self, difficulty: Difficulty | None = None) -> None:
        if difficulty is not None:
            self.difficulty = difficulty
        mid_r = ROWS // 2
        mid_c = COLS // 2
        self.snake = [(mid_c, mid_r), (mid_c - 1, mid_r), (mid_c - 2, mid_r)]
        self.direction = Direction.RIGHT
        self.queued_direction = Direction.RIGHT
        self.score = 0
        self.foods_eaten = 0
        self.status = GameStatus.PLAYING
        self.food = _random_empty_cell(set(self.snake))

    def start_from_menu(self) -> None:
        self.reset(DIFFICULTY_ORDER[self.menu_index])

    def menu_up(self) -> None:
        self.menu_index = (self.menu_index - 1) % len(DIFFICULTY_ORDER)

    def menu_down(self) -> None:
        self.menu_index = (self.menu_index + 1) % len(DIFFICULTY_ORDER)

    def tick_interval_ms(self) -> int:
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        reduction = self.foods_eaten * settings["speedup_ms"]
        return max(settings["min_ms"], settings["base_ms"] - reduction)

    def queue_direction(self, new_dir: Direction) -> None:
        if self.status != GameStatus.PLAYING:
            return
        active = self.queued_direction
        if new_dir.opposes(active):
            return
        if len(self.snake) > 1 and new_dir.opposes(self.direction):
            return
        self.queued_direction = new_dir

    def step(self) -> None:
        if self.status != GameStatus.PLAYING:
            return

        self.direction = self.queued_direction
        head_c, head_r = self.snake[0]
        new_head = (head_c + self.direction.dx, head_r + self.direction.dy)

        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            self.status = GameStatus.GAME_OVER
            return

        if new_head in self.snake[:-1]:
            self.status = GameStatus.GAME_OVER
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.foods_eaten += 1
            step = DIFFICULTY_SETTINGS[self.difficulty]["score_step"]
            self.score += step
            try:
                self.food = _random_empty_cell(set(self.snake))
            except RuntimeError:
                self.status = GameStatus.GAME_OVER
        else:
            self.snake.pop()

    def toggle_pause(self) -> None:
        if self.status == GameStatus.PLAYING:
            self.status = GameStatus.PAUSED
        elif self.status == GameStatus.PAUSED:
            self.status = GameStatus.PLAYING

    def return_to_menu(self) -> None:
        self.status = GameStatus.MENU
        self.score = 0
        self.foods_eaten = 0

    @property
    def length(self) -> int:
        return len(self.snake)

    @property
    def selected_difficulty(self) -> Difficulty:
        return DIFFICULTY_ORDER[self.menu_index]
