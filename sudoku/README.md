# Sudoku Master 🧩

A minimalist, aesthetically pleasing Sudoku game built with Python and Pygame.

## Features
- **3 Difficulty Levels**: Easy (40 clues), Medium (30 clues), and Hard (22 clues).
- **Minimalist UI**: Clean dark-mode design with subtle highlights.
- **Smart Hints**: Toggle hints to highlight errors in real-time.
- **Robust Engine**: Advanced backtracking algorithm for puzzle generation and solving.

## How to Play
1. **Selection**: Click on any cell to select it.
2. **Input**: Use number keys `1-9` to fill a cell.
3. **Delete**: Use `Backspace` or `0` to clear a cell.
4. **Difficulties**: Use the top menu to change levels (resets the board).
5. **Hint**: Click the **HINTS** button to toggle error highlighting.

## Installation
Ensure you have Python installed, then:
```bash
pip install -r requirements.txt
python main.py
```

## Structure
- `sudoku/engine.py`: The logic behind Sudoku solving and generation.
- `sudoku/gui.py`: The rendering engine using Pygame.
- `sudoku/controller.py`: Event handling and game state management.
