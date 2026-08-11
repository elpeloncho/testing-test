"""Tetrimino definitions, shapes, rotations, and color styling."""

from dataclasses import dataclass
from enum import Enum, auto
import random
from typing import List, Tuple

# ANSI Color codes for terminal rendering
COLOR_CYAN = "\033[36m"
COLOR_BLUE = "\033[34m"
COLOR_ORANGE = "\033[38;5;208m"
COLOR_YELLOW = "\033[33m"
COLOR_GREEN = "\033[32m"
COLOR_PURPLE = "\033[35m"
COLOR_RED = "\033[31m"
COLOR_RESET = "\033[0m"


class PieceType(Enum):
    I = auto()
    J = auto()
    L = auto()
    O = auto()
    S = auto()
    T = auto()
    Z = auto()


# 2D Matrix representations for the 7 standard Tetrimino shapes
SHAPES = {
    PieceType.I: [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    PieceType.J: [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    PieceType.L: [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0],
    ],
    PieceType.O: [
        [1, 1],
        [1, 1],
    ],
    PieceType.S: [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0],
    ],
    PieceType.T: [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0],
    ],
    PieceType.Z: [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0],
    ],
}

COLORS = {
    PieceType.I: COLOR_CYAN,
    PieceType.J: COLOR_BLUE,
    PieceType.L: COLOR_ORANGE,
    PieceType.O: COLOR_YELLOW,
    PieceType.S: COLOR_GREEN,
    PieceType.T: COLOR_PURPLE,
    PieceType.Z: COLOR_RED,
}


@dataclass
class Piece:
    piece_type: PieceType
    shape: List[List[int]]
    color: str
    x: int = 0
    y: int = 0

    @classmethod
    def create(cls, piece_type: PieceType, x: int = 0, y: int = 0) -> "Piece":
        """Factory method to instantiate a piece of a given type."""
        shape = [row[:] for row in SHAPES[piece_type]]
        color = COLORS[piece_type]
        return cls(piece_type=piece_type, shape=shape, color=color, x=x, y=y)

    @classmethod
    def random(cls, x: int = 0, y: int = 0) -> "Piece":
        """Factory method to instantiate a random piece."""
        piece_type = random.choice(list(PieceType))
        return cls.create(piece_type, x, y)

    def get_rotated_shape(self, clockwise: bool = True) -> List[List[int]]:
        """Returns a new rotated shape matrix without mutating the current piece."""
        n_rows = len(self.shape)
        n_cols = len(self.shape[0])

        if clockwise:
            # Transpose and reverse each row
            return [
                [self.shape[n_rows - 1 - r][c] for r in range(n_rows)]
                for c in range(n_cols)
            ]
        else:
            # Reverse each row and transpose
            return [
                [self.shape[r][n_cols - 1 - c] for r in range(n_rows)]
                for c in range(n_cols)
            ]

    def rotate(self, clockwise: bool = True) -> None:
        """Rotates the piece shape in place."""
        self.shape = self.get_rotated_shape(clockwise=clockwise)

    def get_occupied_positions(self) -> List[Tuple[int, int]]:
        """Returns absolute (x, y) coordinates occupied by non-zero blocks."""
        positions = []
        for r_idx, row in enumerate(self.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    positions.append((self.x + c_idx, self.y + r_idx))
        return positions
