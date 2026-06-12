import pygame

# --- Display Settings ---
WIDTH, HEIGHT = 700, 800
GRID_SIZE = 600
CELL_SIZE = GRID_SIZE // 9
MARGIN = (WIDTH - GRID_SIZE) // 2
TOP_MARGIN = 120

# --- Colors (Minimalist Dark Mode) ---
BG_COLOR = (18, 18, 22)         # Deep charcoal
GRID_COLOR = (45, 45, 55)       # Muted gray
SUBGRID_COLOR = (80, 80, 100)   # Highlighted lines
TEXT_COLOR = (230, 230, 240)    # Soft white
FIXED_COLOR = (140, 140, 160)   # Dimmed gray for preset numbers
USER_COLOR = (100, 150, 255)    # Modern blue for user input
SELECT_COLOR = (50, 50, 75)     # Subtle background for selection
HIGHLIGHT_COLOR = (35, 35, 50)  # Row/Col highlight
HINT_WRONG = (255, 80, 80)      # Soft red for errors
HINT_CORRECT = (100, 210, 140)  # Mint green for successes

# --- Difficulty Levels ---
DIFFICULTIES = {
    "Easy": 40,
    "Medium": 30,
    "Hard": 22
}

# --- Fonts ---
pygame.font.init()
FONT_MAIN = "Verdana"
FONT_BOLD = "Verdana" # Will load with bold=True

# --- UI Elements ---
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 45
BUTTON_RADIUS = 8
