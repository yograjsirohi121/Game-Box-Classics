# Tetris — Classic Style

A minimal, aesthetic Tetris game built with Python and pygame. Deep-space colour palette with vibrant neon pieces.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![pygame](https://img.shields.io/badge/pygame-2.5%2B-green)

## Features

- Classic grid-based Tetris gameplay
- 7-bag randomiser for fair piece distribution
- Ghost piece preview (see where your piece will land)
- Hold piece (swap current piece for later)
- Wall kicks for forgiving rotation
- DAS (Delayed Auto Shift) for smooth held-key movement
- Three difficulty levels (Easy, Medium, Hard)
- Speed increases as you level up
- Pause, restart, and menu navigation

## Requirements

- Python 3.10+
- pygame 2.5+

## Quick start

```bash
cd tetris

py -m pip install -e .

# Run (either command works)
py main.py
py -m tetris
```

## Controls

| Input | Action |
|-------|--------|
| `↑ ↓` or `W S` | Menu: choose difficulty |
| `1` `2` `3` | Menu: jump to Easy / Medium / Hard |
| `Enter` / `Space` | Menu: start game |
| `← →` or `A D` | Move piece left / right |
| `↓` or `S` | Soft drop |
| `Space` | Hard drop |
| `↑` or `W` | Rotate clockwise |
| `Z` | Rotate counter-clockwise |
| `C` | Hold piece |
| `P` | Pause / resume |
| `R` | Restart (after game over) |
| `M` | Return to menu (paused or game over) |
| `Esc` / `Q` | Quit |

## Difficulty

| Level | Speed | Score multiplier |
|-------|-------|------------------|
| Easy | Slow start, gentle ramp | 1× |
| Medium | Balanced | 2× |
| Hard | Fast start, steep ramp | 3× |

## Scoring

| Lines cleared | Base score |
|---------------|------------|
| 1 (Single) | 100 |
| 2 (Double) | 300 |
| 3 (Triple) | 500 |
| 4 (Tetris) | 800 |

Score = base × difficulty multiplier. Every 10 lines clears a level.

## Project structure

```
tetris/
├── main.py                 # Entry point
├── pyproject.toml
├── requirements.txt
├── README.md
├── .gitignore
├── tetris/                 # Application package
│   ├── app.py              # Game loop + DAS
│   ├── config.py           # Layout, colors, difficulty
│   ├── models.py           # Tetrominoes, GameStatus
│   ├── game.py             # Core logic (no pygame)
│   ├── renderer.py         # Drawing
│   └── input_handler.py    # Keyboard input
└── tests/
    └── test_game.py
```

## Run tests

```bash
py -m pip install pytest
py -m pytest tests/
```

## License

MIT — use freely for learning and personal projects.
