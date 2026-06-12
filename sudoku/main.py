import os
import sys

# Add the current directory to sys.path to ensure 'sudoku' package is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sudoku.controller import SudokuController

def main():
    game = SudokuController()
    game.run()

if __name__ == "__main__":
    main()
