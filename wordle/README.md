# Wordle Clone

A local Wordle-style word game built with Python and pygame. Guess the hidden 5-letter word in six tries.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![pygame](https://img.shields.io/badge/pygame-2.5%2B-green)

## Features

- Classic Wordle rules (green = correct spot, yellow = wrong spot, gray = not in word)
- Physical keyboard and on-screen keyboard support
- Tile reveal animation after each guess
- Word validation against a built-in dictionary
- Random answer each round
- Win/lose screen with quick restart

## Requirements

- Python 3.10 or newer
- pygame 2.5+

## Quick start

```bash
cd wordle

# Install dependencies (editable install recommended)
py -m pip install -e .

# Run the game (either command works)
py main.py
py -m wordle
```

On macOS/Linux, use `python3` instead of `py` if needed.

## Controls

| Input | Action |
|-------|--------|
| `A`–`Z` | Type letters |
| `Enter` | Submit guess |
| `Backspace` | Delete letter |
| `N` | New game |
| `Esc` / `Q` | Quit |

You can also click the on-screen keyboard.

## Project structure

```
wordle/
├── main.py                 # Entry point
├── pyproject.toml          # Package metadata and dependencies
├── requirements.txt        # Pip-compatible dependency list
├── README.md
├── .gitignore
├── data/                   # Static game data (not code)
│   ├── answers.txt         # Words used as answers
│   └── valid_words.txt     # All acceptable guesses
├── wordle/                 # Application package
│   ├── __init__.py
│   ├── __main__.py         # Enables `python -m wordle`
│   ├── app.py              # Game loop and bootstrap
│   ├── config.py           # Constants, colors, layout
│   ├── models.py           # Game state and rules
│   ├── dictionary.py       # Word list loading
│   ├── evaluator.py        # Guess scoring logic
│   ├── renderer.py         # Pygame drawing
│   └── input_handler.py    # Keyboard and mouse input
└── tests/                  # Unit tests for core logic
    ├── test_evaluator.py
    └── test_dictionary.py
```

### Module responsibilities

| Module | Responsibility |
|--------|----------------|
| `config.py` | Tunable settings — no game logic |
| `models.py` | Pure game state; no pygame imports |
| `evaluator.py` | Wordle letter-matching algorithm |
| `dictionary.py` | Reads word lists from `data/` |
| `renderer.py` | All visual output |
| `input_handler.py` | Maps input events to game actions |
| `app.py` | Wires everything together |

## Run tests

```bash
py -m pip install -e ".[dev]"   # optional if you add dev deps
py -m pytest tests/
```

Install pytest first if needed: `py -m pip install pytest`

## Upload to GitHub

```bash
git init
git add .
git commit -m "Add Wordle clone game"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/wordle.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Customization

- **Add words:** Edit files in `data/` (one 5-letter word per line, lowercase).
- **Change difficulty:** Adjust `MAX_GUESSES` in `wordle/config.py`.
- **Reveal speed:** Change `REVEAL_MS` in `wordle/config.py`.
- **Theme:** Edit color constants in `wordle/config.py`.

## License

MIT — use freely for learning and personal projects.
