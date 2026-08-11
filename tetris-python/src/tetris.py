"""Main entrypoint and game loop for Tetris Terminal using raw terminal I/O."""

import sys
import os
import time
from typing import Optional

# Ensure src module can be resolved when running tetris.py directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.board import Board
from src.render import Renderer

# Platform-specific non-blocking input setup
if os.name != "nt":
    import select
    import termios
    import tty


class TerminalController:
    """Manages raw terminal I/O mode and key reading."""

    def __init__(self):
        self.is_posix = os.name != "nt"
        self.old_settings = None

    def __enter__(self):
        if self.is_posix:
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setraw(sys.stdin.fileno())
        Renderer.hide_cursor()
        Renderer.clear()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_posix and self.old_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
        Renderer.show_cursor()

    def get_key(self) -> Optional[str]:
        """Reads a single key or escape sequence without blocking."""
        if not self.is_posix:
            return None

        rlist, _, _ = select.select([sys.stdin], [], [], 0)
        if not rlist:
            return None

        char = sys.stdin.read(1)
        if char == "\x1b":  # Handle escape sequences for arrow keys
            rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
            if rlist:
                char += sys.stdin.read(2)
        return char


def get_drop_interval(level: int) -> float:
        """Calculates gravity drop speed based on current game level."""
        return max(0.05, 0.5 - (level * 0.04))


def run_game() -> None:
    board = Board()
    last_drop_time = time.time()

    with TerminalController() as term:
        while True:
            current_time = time.time()
            drop_interval = get_drop_interval(board.level)

            # Render current state
            frame = Renderer.render(board)
            sys.stdout.write(frame)
            sys.stdout.flush()

            # Handle user input
            key = term.get_key()
            if key in ["q", "Q", "\x03"]:  # 'q', 'Q', or Ctrl+C
                break

            if not board.game_over:
                if key in ["\x1b[D", "a", "A"]:  # Left arrow or 'a'
                    board.move_left()
                elif key in ["\x1b[C", "d", "D"]:  # Right arrow or 'd'
                    board.move_right()
                elif key in ["\x1b[B", "s", "S"]:  # Down arrow or 's'
                    board.move_down()
                elif key in ["\x1b[A", "w", "W"]:  # Up arrow or 'w'
                    board.rotate_piece()
                elif key in [" ", "\r", "\n"]:     # Space or Enter
                    board.hard_drop()

            # Gravity drop tick
            if not board.game_over and (current_time - last_drop_time >= drop_interval):
                board.move_down()
                last_drop_time = current_time

            time.sleep(0.02)


def main() -> None:
    try:
        run_game()
    except KeyboardInterrupt:
        pass
    finally:
        Renderer.show_cursor()
        print("\nThanks for playing Tetris!")


if __name__ == "__main__":
    main()
