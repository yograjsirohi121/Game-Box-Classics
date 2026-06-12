"""Tests for core Wordle game logic."""

from wordle.evaluator import evaluate_guess


def test_all_correct():
    assert evaluate_guess("hello", "hello") == ["correct"] * 5


def test_all_absent():
    assert evaluate_guess("hello", "party") == ["absent"] * 5


def test_duplicate_letters_yellow_then_absent():
    # answer has one 'l'; guess has two — only one should be present
    assert evaluate_guess("hello", "llama") == [
        "present",
        "present",
        "absent",
        "absent",
        "absent",
    ]


def test_duplicate_letters_correct_and_present():
    assert evaluate_guess("speed", "edges") == [
        "present",
        "present",
        "absent",
        "correct",
        "present",
    ]


def test_mixed_result():
    assert evaluate_guess("crane", "crown") == [
        "correct",
        "correct",
        "absent",
        "absent",
        "present",
    ]
