"""Game constants, layout, and theme settings."""

from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Rules
WORD_LENGTH = 5
MAX_GUESSES = 6

# Timing
FPS = 60
REVEAL_MS = 180

# Layout
TILE = 62
TILE_GAP = 5
PADDING = 24
KEY_H = 58
KEY_GAP = 6

BOARD_W = WORD_LENGTH * TILE + (WORD_LENGTH - 1) * TILE_GAP
WIDTH = max(BOARD_W + PADDING * 2, 520)
HEIGHT = 720

# Colors (Wordle-inspired)
BG = (18, 18, 19)
TEXT = (255, 255, 255)
TEXT_ABSENT = (168, 170, 172)
MUTED = (120, 124, 126)
BORDER_EMPTY = (58, 58, 60)
TILE_ACTIVE = (86, 87, 88)
CORRECT = (83, 141, 78)
CORRECT_LIGHT = (106, 165, 100)
CORRECT_DARK = (62, 112, 58)
PRESENT = (181, 159, 59)
PRESENT_LIGHT = (201, 180, 86)
PRESENT_DARK = (148, 128, 46)
ABSENT = (58, 58, 60)
ABSENT_LIGHT = (78, 78, 80)
ABSENT_DARK = (38, 38, 40)
KEY_BG = (129, 131, 132)
KEY_BG_LIGHT = (151, 153, 155)
KEY_BG_DARK = (102, 104, 106)
KEY_ABSENT_LIGHT = (72, 72, 74)
KEY_ABSENT_DARK = (44, 44, 46)
KEY_TEXT = (255, 255, 255)

STATE_COLORS = {
    "correct": CORRECT,
    "present": PRESENT,
    "absent": ABSENT,
}

STATE_GRADIENTS = {
    "correct": (CORRECT_LIGHT, CORRECT_DARK),
    "present": (PRESENT_LIGHT, PRESENT_DARK),
    "absent": (ABSENT_LIGHT, ABSENT_DARK),
}

TILE_GRADIENTS = {
    "active": (TILE_ACTIVE, (68, 69, 70)),
    "empty": (BORDER_EMPTY, (42, 42, 44)),
}

KEYBOARD_ROWS = [
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
]
