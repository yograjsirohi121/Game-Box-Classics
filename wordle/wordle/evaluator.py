"""Guess evaluation logic (Wordle scoring rules)."""

from wordle.config import WORD_LENGTH


def evaluate_guess(answer: str, guess: str) -> list[str]:
    """Return per-letter states: 'correct', 'present', or 'absent'."""
    result = ["absent"] * WORD_LENGTH
    remaining = list(answer)

    for i, letter in enumerate(guess):
        if letter == answer[i]:
            result[i] = "correct"
            remaining[i] = ""

    for i, letter in enumerate(guess):
        if result[i] == "correct":
            continue
        if letter in remaining:
            result[i] = "present"
            remaining[remaining.index(letter)] = ""

    return result
