# Pyasteroids

A classic Asteroids arcade game built in Python with Pygame, developed as part of the [Boot.dev](https://boot.dev) curriculum.

## Installation

```bash
# Clone the repo and navigate to the project
cd pyasteroids

# Install dependencies
pip install -r requirements.txt
```

Or with uv:
```bash
uv sync
```

## Running the Game

```bash
python main.py
# or
uv run main.py
```

## How to Play

### Controls
| Key | Action |
|-----|--------|
| `W` | Thrust forward |
| `S` | Reverse thrust |
| `A/D` | Rotate left/right |
| `SPACE` | Shoot |
| `SHIFT` | Warp (hold to charge, release to teleport) |
| `1` | Fire homing rockets |
| `2` | Deploy mine |
| `ESC` | Pause / Menu |

### Objective
Destroy asteroids to score points. Collect power-ups for shields, speed boosts, and weapons. Survive as long as you can!

### Power-ups
- **Shield** (blue) - Absorbs one hit
- **Speed** (green) - Temporary speed boost
- **Rockets** (orange) - Homing missiles
- **Mines** (red) - Proximity explosives
