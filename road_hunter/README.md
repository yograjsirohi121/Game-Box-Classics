# Road Hunter — Neon Vertical Racing

A classy, aesthetic, and minimalistic vertical road racing game built with Python and pygame. Inspired by retro classics like *Road Fighter* and *Spy Hunter*, featuring a neon synthwave palette and smooth arcade driving controls.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![pygame](https://img.shields.io/badge/pygame-2.5%2B-green)

## Features

- **Smooth Driving Physics:** Horizontal inertia and speed-sensitive steering make weaving through traffic feel highly fluid.
- **Neon Synthwave Aesthetic:** Glowing vector outline designs, scroll speed effects, and clean typography.
- **Fuel Management:** Collect emerald fuel canisters to keep your engine running. Accelerating faster scores points quicker but consumes fuel at an increased rate!
- **Dynamic Obstacles:** Dodge slower passive cars, erratic lane-changing opponent cars, and slippery oil slicks that cause spin-outs.
- **Three Difficulty Levels:** Choose from Easy, Medium, and Hard, each scaling spawning speeds, traffic density, and fuel decay.

## Requirements

- Python 3.10+
- pygame 2.5+

## Quick start

```bash
cd road_hunter

py -m pip install -e .

# Run (either command works)
py main.py
py -m road_hunter
```

## Controls

| Input | Action |
|-------|--------|
| `↑ ↓` or `W S` | Menu: choose difficulty |
| `1` `2` `3` | Menu: jump to Easy / Medium / Hard |
| `Enter` / `Space` | Menu: start game |
| `← →` or `A D` | Steer left / right |
| `↑` or `W` | Accelerate / Speed boost (burns more fuel, increases score rate) |
| `↓` or `S` | Brake |
| `P` | Pause / resume |
| `R` | Restart (after game over) |
| `M` | Return to menu (paused or game over) |
| `Esc` / `Q` | Quit |

## Difficulty

| Level | Base speed | Spawn density | Fuel decay rate |
|-------|------------|---------------|-----------------|
| Easy | Slow | Low | Low |
| Medium | Medium | Medium | Medium |
| Hard | Fast | High | High |

## Project structure

```
road_hunter/
├── main.py                 # Entry point
├── pyproject.toml
├── requirements.txt
├── README.md
├── .gitignore
├── road_hunter/            # Application package
│   ├── app.py              # Game loop
│   ├── config.py           # Colors, viewport metrics, speeds
│   ├── models.py           # GameStatus, Car, Obstacle, Fuel
│   ├── game.py             # Pure game state and simulation (no pygame)
│   ├── renderer.py         # Pygame neon drawing routines
│   └── input_handler.py    # Keyboard inputs
└── tests/
    └── test_game.py        # Automated logic checks
```

## Run tests

```bash
py -m pip install pytest
py -m pytest tests/
```

## License

MIT — use freely for learning and personal projects.
