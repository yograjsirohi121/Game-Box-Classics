import pygame
from sudoku.constants import (
    BG_COLOR, GRID_COLOR, SUBGRID_COLOR, TEXT_COLOR, 
    FIXED_COLOR, USER_COLOR, SELECT_COLOR, HIGHLIGHT_COLOR, 
    HINT_WRONG, HINT_CORRECT, MARGIN, TOP_MARGIN, 
    GRID_SIZE, CELL_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT, 
    BUTTON_RADIUS, FONT_MAIN, WIDTH, HEIGHT
)

class SudokuGUI:
    def __init__(self, screen):
        self.screen = screen
        self.fonts = {
            "title": pygame.font.SysFont(FONT_MAIN, 48, bold=True),
            "cell": pygame.font.SysFont(FONT_MAIN, 32),
            "cell_bold": pygame.font.SysFont(FONT_MAIN, 32, bold=True),
            "btn": pygame.font.SysFont(FONT_MAIN, 16, bold=True),
            "hint": pygame.font.SysFont(FONT_MAIN, 14, italic=True)
        }

    def draw_bg(self):
        self.screen.fill(BG_COLOR)

    def draw_grid(self, selected_cell=None):
        # Draw selected cell highlight
        if selected_cell:
            r, c = selected_cell
            rect = pygame.Rect(MARGIN + c * CELL_SIZE, TOP_MARGIN + r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, SELECT_COLOR, rect)
            
            # Row/Col highlights - using alpha blending for better aesthetics
            s = pygame.Surface((GRID_SIZE, CELL_SIZE), pygame.SRCALPHA)
            s.fill((*HIGHLIGHT_COLOR, 100))
            self.screen.blit(s, (MARGIN, TOP_MARGIN + r * CELL_SIZE))
            
            s2 = pygame.Surface((CELL_SIZE, GRID_SIZE), pygame.SRCALPHA)
            s2.fill((*HIGHLIGHT_COLOR, 100))
            self.screen.blit(s2, (MARGIN + c * CELL_SIZE, TOP_MARGIN))

        # Draw cells
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            color = SUBGRID_COLOR if i % 3 == 0 else GRID_COLOR
            # Vertical
            pygame.draw.line(self.screen, color, 
                             (MARGIN + i * CELL_SIZE, TOP_MARGIN), 
                             (MARGIN + i * CELL_SIZE, TOP_MARGIN + GRID_SIZE), thickness)
            # Horizontal
            pygame.draw.line(self.screen, color, 
                             (MARGIN, TOP_MARGIN + i * CELL_SIZE), 
                             (MARGIN + GRID_SIZE, TOP_MARGIN + i * CELL_SIZE), thickness)

    def draw_numbers(self, puzzle, original, hints_on=False, solution=None):
        for r in range(9):
            for c in range(9):
                val = puzzle[r][c]
                is_original = original[r][c]
                
                if val != 0:
                    color = FIXED_COLOR if is_original else USER_COLOR
                    # Check if hint/validation is on and it's wrong
                    if hints_on and not is_original and val != solution[r][c]:
                        color = HINT_WRONG
                    
                    font = self.fonts["cell_bold"] if is_original else self.fonts["cell"]
                    text = font.render(str(val), True, color)
                    rect = text.get_rect(center=(MARGIN + c * CELL_SIZE + CELL_SIZE // 2, 
                                                TOP_MARGIN + r * CELL_SIZE + CELL_SIZE // 2))
                    self.screen.blit(text, rect)

    def draw_buttons(self, difficulties, current_diff, hints_on):
        # Difficulty Buttons
        y = 40
        x_start = MARGIN
        for i, diff in enumerate(difficulties):
            color = USER_COLOR if diff == current_diff else GRID_COLOR
            rect = pygame.Rect(x_start + i * (BUTTON_WIDTH + 20), y, BUTTON_WIDTH, BUTTON_HEIGHT)
            pygame.draw.rect(self.screen, color, rect, border_radius=BUTTON_RADIUS)
            
            text = self.fonts["btn"].render(diff.upper(), True, TEXT_COLOR)
            self.screen.blit(text, text.get_rect(center=rect.center))

        # Hint Toggle
        h_color = HINT_CORRECT if hints_on else GRID_COLOR
        h_rect = pygame.Rect(WIDTH - MARGIN - BUTTON_WIDTH, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(self.screen, h_color, h_rect, border_radius=BUTTON_RADIUS)
        h_text = self.fonts["btn"].render("HINTS: " + ("ON" if hints_on else "OFF"), True, TEXT_COLOR)
        self.screen.blit(h_text, h_text.get_rect(center=h_rect.center))

    def draw_status(self, message):
        text = self.fonts["btn"].render(message, True, TEXT_COLOR)
        self.screen.blit(text, (MARGIN, HEIGHT - 40))

    def get_cell_from_pos(self, pos):
        x, y = pos
        if MARGIN <= x <= MARGIN + GRID_SIZE and TOP_MARGIN <= y <= TOP_MARGIN + GRID_SIZE:
            return (y - TOP_MARGIN) // CELL_SIZE, (x - MARGIN) // CELL_SIZE
        return None
