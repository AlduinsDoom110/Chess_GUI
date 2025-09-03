# Chess GUI

A simple chess graphical user interface built with [pygame](https://www.pygame.org/) and [python-chess](https://python-chess.readthedocs.io/).

## Setup
```
pip install -r requirements.txt
```

## Usage
```
python chess_gui.py
```

### Controls
- Left click a piece then a destination square to move.
- Press **N** to start a new game.
- Press **U** to undo the last move.
- Close the window to quit.

The game logic is provided by `python-chess` which ensures all chess rules are enforced including check, checkmate and stalemate.
