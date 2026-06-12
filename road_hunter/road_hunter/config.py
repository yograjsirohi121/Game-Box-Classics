"""Layout, theme, and difficulty configurations for Road Hunter."""

from enum import Enum

# Screen & Layout
WIDTH = 480
HEIGHT = 640
HEADER_H = 60
PADDING = 20

# Play Area (Road Dimensions)
ROAD_L = 80
ROAD_R = 400
ROAD_WIDTH = ROAD_R - ROAD_L  # 320 px
ROAD_CENTER = (ROAD_L + ROAD_R) // 2  # 240 px

# Lanes for Spawning (Left, Middle, Right)
LANE_WIDTH = ROAD_WIDTH // 3  # ~106 px
LANE_CENTERS = [
    ROAD_L + LANE_WIDTH // 2,                # ~133 px
    ROAD_L + LANE_WIDTH + LANE_WIDTH // 2,   # ~240 px
    ROAD_L + LANE_WIDTH * 2 + LANE_WIDTH // 2 # ~346 px
]

# Cars & Entity Sizes
CAR_WIDTH = 26
CAR_HEIGHT = 48
FUEL_RADIUS = 10
OIL_RADIUS = 15

# Frame Timing
FPS = 60

# Neon Synthwave Palette
BG = (13, 2, 33)           # Deep purple
ROAD_BG = (22, 11, 46)     # Darker road purple
ROAD_BORDER = (0, 240, 255) # Glowing neon cyan
LANE_LINE = (0, 150, 255)   # Muted neon cyan/blue
TEXT = (255, 255, 255)     # Pure white
TEXT_DIM = (140, 130, 160) # Muted purple-grey
ACCENT = (255, 0, 127)     # Neon magenta / pink
ACCENT_GREEN = (57, 255, 20) # Glowing neon green
ACCENT_YELLOW = (255, 183, 3) # Neon yellow
ACCENT_PURPLE = (157, 0, 255) # Neon purple
OVERLAY = (13, 2, 33, 200) # Transparent screen dims
MENU_HOVER = (40, 20, 80)  # Dark purple hover highlight

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
    Difficulty.EASY: {
        "scroll_speed_min": 6.0,
        "scroll_speed_max": 12.0,
        "spawn_interval_ms": 1500,
        "fuel_decay_rate": 0.08,  # fuel points per frame
        "traffic_density": 0.4,   # probability of spawning car vs other
        "score_multiplier": 1.0,
    },
    Difficulty.MEDIUM: {
        "scroll_speed_min": 8.0,
        "scroll_speed_max": 16.0,
        "spawn_interval_ms": 1100,
        "fuel_decay_rate": 0.12,
        "traffic_density": 0.5,
        "score_multiplier": 2.0,
    },
    Difficulty.HARD: {
        "scroll_speed_min": 10.0,
        "scroll_speed_max": 20.0,
        "spawn_interval_ms": 800,
        "fuel_decay_rate": 0.16,
        "traffic_density": 0.6,
        "score_multiplier": 3.0,
    },
}
