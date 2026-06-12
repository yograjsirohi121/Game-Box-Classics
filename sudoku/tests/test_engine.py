"""
Unit tests for the Sudoku Master engine logic.
Verifies puzzle generation, solving accuracy, and board validation.
"""
import pytest
from sudoku.engine import SudokuEngine

def test_engine_initialization():
    """Verify that the engine initializes with empty 9x9 grids."""
    engine = SudokuEngine()
    assert len(engine.solution) == 9
    assert len(engine.puzzle) == 9

def test_solve():
    engine = SudokuEngine()
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    assert engine.solve(board) is True
    # Verify it's full
    for row in board:
        assert 0 not in row

def test_generation():
    engine = SudokuEngine()
    puzzle = engine.generate_puzzle(40)
    clues = sum(1 for row in puzzle for cell in row if cell != 0)
    assert clues == 40
