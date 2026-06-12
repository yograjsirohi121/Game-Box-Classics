# Snake — Classic Nokia Style

A minimal, local Snake game inspired by the classic Nokia phone version. Built with Python and pygame.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![pygame](https://img.shields.io/badge/pygame-2.5%2B-green)

## Features

- Classic grid-based Snake gameplay
- Nokia-inspired dark green LCD aesthetic
- Three difficulty levels (Easy, Medium, Hard)
- Speed increases as you eat more food
- Pause, restart, and menu navigation

## Requirements

- Python 3.10+
- pygame 2.5+

## Quick start

```bash
cd snake

py -m pip install -e .

# Run (either command works)
py main.py
py -m snake
```

## Controls

| Input | Action |
|-------|--------|
| `↑ ↓` or `W S` | Menu: choose difficulty |
| `1` `2` `3` | Menu: jump to Easy / Medium / Hard |
| `Enter` / `Space` | Menu: start game |
| `↑ ↓ ← →` or `W A S D` | Move snake |
| `P` | Pause / resume |
| `R` | Restart (after game over) |
| `M` | Return to menu (paused or game over) |
| `Esc` / `Q` | Quit |

## Difficulty

| Level | Speed | Score per food |
|-------|-------|----------------|
| Easy | Slow start, gentle ramp | 10 |
| Medium | Balanced | 15 |
| Hard | Fast start, steep ramp | 20 |

## Project structure

```
snake/
├── main.py                 # Entry point
├── pyproject.toml
├── requirements.txt
├── README.md
├── .gitignore
├── snake/                  # Application package
│   ├── app.py              # Game loop
│   ├── config.py           # Layout, colors, difficulty
│   ├── models.py           # Direction, GameStatus
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

## Upload to GitHub

```bash
git init
git add .
git commit -m "Add Nokia-style Snake game"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/snake.git
git push -u origin main
```

## License

MIT — use freely for learning and personal projects.
