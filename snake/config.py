"""Layout, theme, and difficulty settings."""

from enum import Enum

# Grid
COLS = 20
ROWS = 22
CELL = 22
HEADER_H = 56
PADDING = 16
PLAY_W = COLS * CELL
PLAY_H = ROWS * CELL
WIDTH = PLAY_W + PADDING * 2
HEIGHT = HEADER_H + PLAY_H + PADDING * 2

# Timing
FPS = 60

# Nokia-inspired palette (dark LCD, muted greens)
BG = (6, 10, 6)
HEADER_BG = (10, 16, 10)
PLAY_BG = (4, 8, 4)
BORDER = (42, 62, 42)
GRID = (14, 22, 14)
SNAKE_HEAD = (118, 210, 118)
SNAKE_BODY = (72, 158, 72)
SNAKE_BODY_DARK = (52, 118, 52)
FOOD = (228, 232, 196)
FOOD_GLOW = (180, 190, 140)
TEXT = (168, 208, 168)
TEXT_DIM = (90, 120, 90)
ACCENT = (130, 200, 130)
OVERLAY = (0, 0, 0, 170)
MENU_HOVER = (20, 32, 20)


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


DIFFICULTY_ORDER = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]

DIFFICULTY_LABELS = {
    Difficulty.EASY: "Easy",
    Difficulty.MEDIUM: "Medium",
    Difficulty.HARD: "Hard",
}

DIFFICULTY_SETTINGS = {
    Difficulty.EASY: {"base_ms": 165, "min_ms": 105, "speedup_ms": 2, "score_step": 10},
    Difficulty.MEDIUM: {"base_ms": 115, "min_ms": 65, "speedup_ms": 3, "score_step": 15},
    Difficulty.HARD: {"base_ms": 78, "min_ms": 42, "speedup_ms": 4, "score_step": 20},
}
