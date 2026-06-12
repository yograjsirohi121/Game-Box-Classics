"""Tests for word list loading."""

from wordle.config import WORD_LENGTH
from wordle.dictionary import load_word_lists


def test_word_lists_load():
    answers, valid = load_word_lists()
    assert len(answers) > 0
    assert len(valid) >= len(answers)
    assert all(len(word) == WORD_LENGTH for word in answers)
    assert all(word.isalpha() for word in answers)
