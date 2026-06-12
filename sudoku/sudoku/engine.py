import random
import copy

class SudokuEngine:
    def __init__(self):
        self.solution = [[0] * 9 for _ in range(9)]
        self.puzzle = [[0] * 9 for _ in range(9)]
        self.original = [[False] * 9 for _ in range(9)]

    def is_valid(self, board, row, col, num):
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False

        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def solve(self, board):
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(board, row, col, i):
                board[row][col] = i

                if self.solve(board):
                    return True

                board[row][col] = 0

        return False

    def generate_puzzle(self, clues):
        # 1. Start with an empty board
        board = [[0] * 9 for _ in range(9)]
        
        # 2. Fill the diagonal 3x3 boxes (they are independent)
        for i in range(0, 9, 3):
            self.fill_box(board, i, i)
        
        # 3. Fill the rest using recursion
        self.solve(board)
        self.solution = copy.deepcopy(board)
        
        # 4. Remove cells to create the puzzle
        self.puzzle = copy.deepcopy(board)
        attempts = 81 - clues
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while self.puzzle[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            
            backup = self.puzzle[row][col]
            self.puzzle[row][col] = 0
            
            # (Optional: Check for unique solution, but for a simple game, 
            # we just ensure it's solvable)
            attempts -= 1
        
        # 5. Mark original clues
        self.original = [[self.puzzle[r][c] != 0 for c in range(9)] for r in range(9)]
        return self.puzzle

    def fill_box(self, board, row, col):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[row + i][col + j] = nums.pop()

    def check_finished(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return False
                # Validate every cell
                val = board[r][c]
                board[r][c] = 0
                if not self.is_valid(board, r, c, val):
                    board[r][c] = val
                    return False
                board[r][c] = val
        return True
