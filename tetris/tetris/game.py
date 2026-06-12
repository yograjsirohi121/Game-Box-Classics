"""Core Tetris game logic (no pygame dependencies)."""

import random
from dataclasses import dataclass, field

from tetris.config import (
    COLS,
    DIFFICULTY_ORDER,
    DIFFICULTY_SETTINGS,
    LINE_SCORES,
    ROWS,
    Difficulty,
)
from tetris.models import (
    GameStatus,
    PIECE_NAMES,
    RotationDir,
    TETROMINOES,
)


def _generate_bag() -> list[str]:
    """Return a shuffled bag of all 7 pieces (7-bag randomiser)."""
    bag = list(PIECE_NAMES)
    random.shuffle(bag)
    return bag


@dataclass
class TetrisGame:
    difficulty: Difficulty = Difficulty.MEDIUM
    status: GameStatus = GameStatus.MENU
    menu_index: int = 0

    # Board: rows × cols, None = empty, str = piece name (for colour lookup)
    board: list[list[str | None]] = field(default_factory=list)

    # Active piece state
    piece: str = "T"
    rotation: int = 0
    piece_x: int = 0
    piece_y: int = 0

    # Preview / hold
    bag: list[str] = field(default_factory=list)
    next_piece: str = "T"
    held_piece: str | None = None
    hold_used: bool = False

    # Scoring
    score: int = 0
    level: int = 1
    lines_cleared: int = 0

    # Lock-delay tracking
    lock_timer: int = 0
    lock_delay_ms: int = 500

    def reset(self, difficulty: Difficulty | None = None) -> None:
        if difficulty is not None:
            self.difficulty = difficulty

        self.board = [[None] * COLS for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.held_piece = None
        self.hold_used = False
        self.lock_timer = 0

        self.bag = _generate_bag()
        self.next_piece = self.bag.pop()
        self._spawn_piece()
        self.status = GameStatus.PLAYING

    def start_from_menu(self) -> None:
        self.reset(DIFFICULTY_ORDER[self.menu_index])

    def menu_up(self) -> None:
        self.menu_index = (self.menu_index - 1) % len(DIFFICULTY_ORDER)

    def menu_down(self) -> None:
        self.menu_index = (self.menu_index + 1) % len(DIFFICULTY_ORDER)

    # ── Piece management ──────────────────────────────────────────

    def _spawn_piece(self) -> None:
        self.piece = self.next_piece
        if not self.bag:
            self.bag = _generate_bag()
        self.next_piece = self.bag.pop()
        self.rotation = 0
        self.piece_x = COLS // 2 - 2
        self.piece_y = 0
        self.lock_timer = 0

        if self._collides(self.piece, self.rotation, self.piece_x, self.piece_y):
            self.status = GameStatus.GAME_OVER

    def _cells(
        self,
        piece: str | None = None,
        rotation: int | None = None,
        px: int | None = None,
        py: int | None = None,
    ) -> list[tuple[int, int]]:
        """Return absolute board positions of piece cells."""
        p = piece if piece is not None else self.piece
        r = rotation if rotation is not None else self.rotation
        ox = px if px is not None else self.piece_x
        oy = py if py is not None else self.piece_y
        return [(ox + cx, oy + cy) for cx, cy in TETROMINOES[p][r % 4]]

    def _collides(
        self,
        piece: str,
        rotation: int,
        px: int,
        py: int,
    ) -> bool:
        for x, y in self._cells(piece, rotation, px, py):
            if x < 0 or x >= COLS or y >= ROWS:
                return True
            if y >= 0 and self.board[y][x] is not None:
                return True
        return False

    # ── Movement ──────────────────────────────────────────────────

    def move_left(self) -> bool:
        if self.status != GameStatus.PLAYING:
            return False
        if not self._collides(self.piece, self.rotation, self.piece_x - 1, self.piece_y):
            self.piece_x -= 1
            self.lock_timer = 0
            return True
        return False

    def move_right(self) -> bool:
        if self.status != GameStatus.PLAYING:
            return False
        if not self._collides(self.piece, self.rotation, self.piece_x + 1, self.piece_y):
            self.piece_x += 1
            self.lock_timer = 0
            return True
        return False

    def soft_drop(self) -> bool:
        if self.status != GameStatus.PLAYING:
            return False
        if not self._collides(self.piece, self.rotation, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
            self.lock_timer = 0
            return True
        return False

    def hard_drop(self) -> None:
        if self.status != GameStatus.PLAYING:
            return
        while not self._collides(self.piece, self.rotation, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        self._lock_piece()

    def rotate(self, direction: RotationDir = RotationDir.CW) -> bool:
        if self.status != GameStatus.PLAYING:
            return False
        new_rot = (self.rotation + direction.value) % 4
        # Wall-kick offsets to try
        kicks = [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1), (-2, 0), (2, 0)]
        for dx, dy in kicks:
            if not self._collides(self.piece, new_rot, self.piece_x + dx, self.piece_y + dy):
                self.piece_x += dx
                self.piece_y += dy
                self.rotation = new_rot
                self.lock_timer = 0
                return True
        return False

    def hold(self) -> None:
        if self.status != GameStatus.PLAYING or self.hold_used:
            return
        self.hold_used = True
        if self.held_piece is None:
            self.held_piece = self.piece
            self._spawn_piece()
        else:
            self.held_piece, self.piece = self.piece, self.held_piece
            self.rotation = 0
            self.piece_x = COLS // 2 - 2
            self.piece_y = 0
            self.lock_timer = 0
            if self._collides(self.piece, self.rotation, self.piece_x, self.piece_y):
                self.status = GameStatus.GAME_OVER

    # ── Ghost (preview drop position) ─────────────────────────────

    def ghost_y(self) -> int:
        gy = self.piece_y
        while not self._collides(self.piece, self.rotation, self.piece_x, gy + 1):
            gy += 1
        return gy

    # ── Gravity / step ────────────────────────────────────────────

    def tick_interval_ms(self) -> int:
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        reduction = (self.level - 1) * settings["speedup"]
        return max(settings["min_ms"], settings["base_ms"] - reduction)

    def step(self) -> None:
        """Called on each gravity tick — moves piece down or locks it."""
        if self.status != GameStatus.PLAYING:
            return
        if not self._collides(self.piece, self.rotation, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
            self.lock_timer = 0
        else:
            self._lock_piece()

    def _lock_piece(self) -> None:
        for x, y in self._cells():
            if 0 <= y < ROWS and 0 <= x < COLS:
                self.board[y][x] = self.piece
        self._clear_lines()
        self.hold_used = False
        self._spawn_piece()

    def _clear_lines(self) -> None:
        cleared = [r for r in range(ROWS) if all(cell is not None for cell in self.board[r])]
        if not cleared:
            return
        count = len(cleared)
        mult = DIFFICULTY_SETTINGS[self.difficulty]["score_mult"]
        self.score += LINE_SCORES[min(count, 4)] * mult
        self.lines_cleared += count
        self.level = self.lines_cleared // 10 + 1

        for r in sorted(cleared, reverse=True):
            del self.board[r]
        for _ in range(count):
            self.board.insert(0, [None] * COLS)

    # ── Pause / menu ─────────────────────────────────────────────

    def toggle_pause(self) -> None:
        if self.status == GameStatus.PLAYING:
            self.status = GameStatus.PAUSED
        elif self.status == GameStatus.PAUSED:
            self.status = GameStatus.PLAYING

    def return_to_menu(self) -> None:
        self.status = GameStatus.MENU
        self.score = 0
        self.lines_cleared = 0
        self.level = 1

    @property
    def selected_difficulty(self) -> Difficulty:
        return DIFFICULTY_ORDER[self.menu_index]
