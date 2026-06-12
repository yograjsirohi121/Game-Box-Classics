"""Game state and core business logic (no pygame dependencies)."""

import random
from dataclasses import dataclass, field
from enum import Enum

from wordle.config import KEYBOARD_ROWS, MAX_GUESSES, WORD_LENGTH
from wordle.evaluator import evaluate_guess


class GameStatus(Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class KeyState(Enum):
    UNUSED = 0
    ABSENT = 1
    PRESENT = 2
    CORRECT = 3


@dataclass
class Game:
    answers: list[str]
    valid_words: set[str]
    answer: str = ""
    guesses: list[str] = field(default_factory=list)
    guess_results: list[list[str]] = field(default_factory=list)
    current: str = ""
    status: GameStatus = GameStatus.PLAYING
    message: str = ""
    message_until: int = 0
    reveal_row: int = -1
    reveal_index: int = -1
    reveal_results: list[str] = field(default_factory=list)
    key_states: dict[str, KeyState] = field(default_factory=dict)

    @classmethod
    def new(cls, answers: list[str], valid_words: set[str]) -> "Game":
        game = cls(answers=answers, valid_words=valid_words)
        game.start_round()
        return game

    def start_round(self) -> None:
        self.answer = random.choice(self.answers)
        self.guesses = []
        self.guess_results = []
        self.current = ""
        self.status = GameStatus.PLAYING
        self.message = ""
        self.message_until = 0
        self.reveal_row = -1
        self.reveal_index = -1
        self.reveal_results = []
        self.key_states = {ch: KeyState.UNUSED for row in KEYBOARD_ROWS for ch in row}

    def set_message(self, text: str, now: int, duration_ms: int = 1500) -> None:
        self.message = text
        self.message_until = now + duration_ms

    def is_animating(self) -> bool:
        return self.reveal_row >= 0

    def submit(self, now: int) -> None:
        if self.status != GameStatus.PLAYING or self.is_animating():
            return
        if len(self.current) < WORD_LENGTH:
            self.set_message("Not enough letters", now)
            return
        word = self.current.lower()
        if word not in self.valid_words:
            self.set_message("Not in word list", now)
            return

        self.guesses.append(word)
        self.reveal_results = evaluate_guess(self.answer, word)
        self.reveal_row = len(self.guesses) - 1
        self.reveal_index = 0
        self.current = ""

    def advance_reveal(self, now: int) -> None:
        if not self.is_animating():
            return

        guess = self.guesses[self.reveal_row]
        letter = guess[self.reveal_index]
        state = self.reveal_results[self.reveal_index]
        self._update_key(letter, state)

        if self.reveal_index >= WORD_LENGTH - 1:
            self.guess_results.append(self.reveal_results.copy())
            self.reveal_row = -1
            self.reveal_index = -1
            self.reveal_results = []

            if guess == self.answer:
                self.status = GameStatus.WON
                tries = len(self.guesses)
                msg = f"Genius in {tries}!" if tries <= 2 else f"You got it in {tries}!"
                self.set_message(msg, now, 3000)
            elif len(self.guesses) >= MAX_GUESSES:
                self.status = GameStatus.LOST
                self.set_message(f"The word was {self.answer.upper()}", now, 4000)
        else:
            self.reveal_index += 1

    def _update_key(self, letter: str, state: str) -> None:
        rank = {"unused": 0, "absent": 1, "present": 2, "correct": 3}
        mapping = {
            "absent": KeyState.ABSENT,
            "present": KeyState.PRESENT,
            "correct": KeyState.CORRECT,
        }
        current = self.key_states.get(letter, KeyState.UNUSED)
        current_rank = rank.get(current.name.lower(), 0)
        if rank[state] > current_rank:
            self.key_states[letter] = mapping[state]

    def type_letter(self, letter: str) -> None:
        if self.status != GameStatus.PLAYING or self.is_animating():
            return
        if len(self.current) < WORD_LENGTH:
            self.current += letter.lower()

    def delete_letter(self) -> None:
        if self.status != GameStatus.PLAYING or self.is_animating():
            return
        self.current = self.current[:-1]

    def tile_state(self, row: int, col: int) -> str | None:
        """Return the display state for a board tile, or None if not yet revealed."""
        if row < len(self.guess_results):
            return self.guess_results[row][col]
        if row == self.reveal_row and col <= self.reveal_index:
            return self.reveal_results[col]
        return None

    def tile_letter(self, row: int, col: int) -> str:
        if row < len(self.guesses):
            return self.guesses[row][col]
        if row == len(self.guesses) and col < len(self.current):
            return self.current[col]
        return ""
