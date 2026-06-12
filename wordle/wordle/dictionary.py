"""Word list loading from bundled data files."""

from pathlib import Path

from wordle.config import DATA_DIR, WORD_LENGTH


def _load_lines(path: Path) -> set[str]:
    words: set[str] = set()
    if not path.exists():
        return words
    for line in path.read_text(encoding="utf-8").splitlines():
        word = line.strip().lower()
        if len(word) == WORD_LENGTH and word.isalpha():
            words.add(word)
    return words


def load_word_lists() -> tuple[list[str], set[str]]:
    """Load answer words and the full valid-guess dictionary."""
    answers = sorted(_load_lines(DATA_DIR / "answers.txt"))
    valid = _load_lines(DATA_DIR / "valid_words.txt")
    valid.update(answers)
    if not answers:
        raise FileNotFoundError(f"No answer words found in {DATA_DIR / 'answers.txt'}")
    return answers, valid
