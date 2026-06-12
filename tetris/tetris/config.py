"""Layout, theme, and difficulty settings."""

from enum import Enum

# Grid dimensions
COLS = 10
ROWS = 20
CELL = 28
HEADER_H = 56
PADDING = 16
SIDEBAR_W = 130

PLAY_W = COLS * CELL
PLAY_H = ROWS * CELL
WIDTH = PADDING + PLAY_W + PADDING + SIDEBAR_W + PADDING
HEIGHT = HEADER_H + PADDING + PLAY_H + PADDING

# Timing
FPS = 60

# ── Colour palette: deep-space / neon-minimal ──────────────────────
BG = (12, 12, 18)
HEADER_BG = (16, 16, 24)
PLAY_BG = (8, 8, 14)
BORDER = (40, 42, 56)
GRID_LINE = (18, 18, 28)
SIDEBAR_BG = (14, 14, 22)

TEXT = (200, 200, 220)
TEXT_DIM = (90, 92, 110)
ACCENT = (120, 180, 255)
OVERLAY = (0, 0, 0, 180)
MENU_HOVER = (18, 20, 30)

# Piece colours (vibrant neon-ish, readable on dark bg)
PIECE_COLOURS: dict[str, tuple[int, int, int]] = {
    "I": (0, 220, 220),   # Cyan
    "O": (220, 220, 0),   # Yellow
    "T": (180, 60, 220),  # Purple
    "S": (60, 220, 60),   # Green
    "Z": (220, 60, 60),   # Red
    "J": (60, 90, 220),   # Blue
    "L": (220, 140, 30),  # Orange
}

GHOST_ALPHA = 40


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

# base_ms  = initial drop interval
# min_ms   = fastest possible drop interval
# speedup  = ms reduction per level
# score_mult = multiplier for line-clear scoring
DIFFICULTY_SETTINGS = {
    Difficulty.EASY: {"base_ms": 800, "min_ms": 200, "speedup": 40, "score_mult": 1},
    Difficulty.MEDIUM: {"base_ms": 500, "min_ms": 100, "speedup": 35, "score_mult": 2},
    Difficulty.HARD: {"base_ms": 300, "min_ms": 50, "speedup": 30, "score_mult": 3},
}

# Line-clear base scores (single, double, triple, tetris)
LINE_SCORES = [0, 100, 300, 500, 800]
