import pygame
import sys
from sudoku.engine import SudokuEngine
from sudoku.gui import SudokuGUI
from sudoku.constants import (
    WIDTH, HEIGHT, DIFFICULTIES, MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT
)

class SudokuController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku Master")
        
        self.engine = SudokuEngine()
        self.gui = SudokuGUI(self.screen)
        
        self.current_difficulty = "Medium"
        self.selected_cell = None
        self.hints_on = False
        self.status_msg = "Select a cell and press 1-9"
        
        self.reset_game()

    def reset_game(self):
        clues = DIFFICULTIES[self.current_difficulty]
        self.engine.generate_puzzle(clues)
        self.puzzle = [row[:] for row in self.engine.puzzle] # Current state
        self.selected_cell = None
        self.status_msg = f"{self.current_difficulty} Mode - Good Luck!"

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.gui.draw_bg()
            self.gui.draw_grid(self.selected_cell)
            self.gui.draw_numbers(self.puzzle, self.engine.original, self.hints_on, self.engine.solution)
            self.gui.draw_buttons(DIFFICULTIES.keys(), self.current_difficulty, self.hints_on)
            self.gui.draw_status(self.status_msg)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    # Check grid
                    cell = self.gui.get_cell_from_pos(pos)
                    if cell:
                        self.selected_cell = cell
                    
                    # Check Buttons (Simple hit detection)
                    y = 40
                    for i, diff in enumerate(DIFFICULTIES.keys()):
                        rect = pygame.Rect(MARGIN + i * (BUTTON_WIDTH + 20), y, BUTTON_WIDTH, BUTTON_HEIGHT)
                        if rect.collidepoint(pos):
                            self.current_difficulty = diff
                            self.reset_game()
                    
                    # Hint button
                    h_rect = pygame.Rect(WIDTH - MARGIN - BUTTON_WIDTH, y, BUTTON_WIDTH, BUTTON_HEIGHT)
                    if h_rect.collidepoint(pos):
                        self.hints_on = not self.hints_on

                if event.type == pygame.KEYDOWN:
                    if self.selected_cell:
                        r, c = self.selected_cell
                        if not self.engine.original[r][c]:
                            if event.key == pygame.K_1 or event.key == pygame.K_KP1: self.puzzle[r][c] = 1
                            elif event.key == pygame.K_2 or event.key == pygame.K_KP2: self.puzzle[r][c] = 2
                            elif event.key == pygame.K_3 or event.key == pygame.K_KP3: self.puzzle[r][c] = 3
                            elif event.key == pygame.K_4 or event.key == pygame.K_KP4: self.puzzle[r][c] = 4
                            elif event.key == pygame.K_5 or event.key == pygame.K_KP5: self.puzzle[r][c] = 5
                            elif event.key == pygame.K_6 or event.key == pygame.K_KP6: self.puzzle[r][c] = 6
                            elif event.key == pygame.K_7 or event.key == pygame.K_KP7: self.puzzle[r][c] = 7
                            elif event.key == pygame.K_8 or event.key == pygame.K_KP8: self.puzzle[r][c] = 8
                            elif event.key == pygame.K_9 or event.key == pygame.K_KP9: self.puzzle[r][c] = 9
                            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE or event.key == pygame.K_0:
                                self.puzzle[r][c] = 0
                            
                            if self.engine.check_finished(self.puzzle):
                                self.status_msg = "CONGRATULATIONS! You solved it!"

            pygame.display.flip()
            clock.tick(60)
