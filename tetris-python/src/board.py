"""Board grid representation, piece collision detection, line clearing, and scoring."""

from typing import List, Optional, Tuple
from src.pieces import Piece


class Board:
    LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}

    def __init__(self, width: int = 10, height: int = 20):
        self.width = width
        self.height = height
        # grid[row][col] stores None if empty, or color string if filled
        self.grid: List[List[Optional[str]]] = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]
        self.score: int = 0
        self.lines_cleared: int = 0
        self.level: int = 0
        self.game_over: bool = False

        self.current_piece: Optional[Piece] = None
        self.next_piece: Optional[Piece] = None
        self.spawn_next_piece()

    def _get_spawn_x(self, piece: Piece) -> int:
        """Calculates centered spawn x coordinate for a given piece."""
        piece_width = len(piece.shape[0])
        return (self.width - piece_width) // 2

    def spawn_next_piece(self) -> None:
        """Spawns the next piece onto the board and generates a new upcoming piece."""
        if self.next_piece is None:
            self.next_piece = Piece.random()

        self.current_piece = self.next_piece
        self.next_piece = Piece.random()

        self.current_piece.x = self._get_spawn_x(self.current_piece)
        self.current_piece.y = 0

        # Check for immediate Game Over
        if not self.is_valid_position(self.current_piece):
            self.game_over = True

    def is_valid_position(
        self,
        piece: Piece,
        offset_x: int = 0,
        offset_y: int = 0,
        shape: Optional[List[List[int]]] = None,
    ) -> bool:
        """Validates if a piece shape placed at (piece.x + offset_x, piece.y + offset_y) fits legally on the grid."""
        target_shape = shape if shape is not None else piece.shape
        target_x = piece.x + offset_x
        target_y = piece.y + offset_y

        for r_idx, row in enumerate(target_shape):
            for c_idx, cell in enumerate(row):
                if not cell:
                    continue

                grid_x = target_x + c_idx
                grid_y = target_y + r_idx

                # Check horizontal boundaries
                if grid_x < 0 or grid_x >= self.width:
                    return False

                # Check vertical boundaries
                if grid_y < 0 or grid_y >= self.height:
                    return False

                # Check overlap with locked blocks
                if self.grid[grid_y][grid_x] is not None:
                    return False

        return True

    def move_left(self) -> bool:
        """Attempts to shift current piece left."""
        if self.game_over or self.current_piece is None:
            return False

        if self.is_valid_position(self.current_piece, offset_x=-1):
            self.current_piece.x -= 1
            return True
        return False

    def move_right(self) -> bool:
        """Attempts to shift current piece right."""
        if self.game_over or self.current_piece is None:
            return False

        if self.is_valid_position(self.current_piece, offset_x=1):
            self.current_piece.x += 1
            return True
        return False

    def move_down(self) -> bool:
        """Attempts to drop current piece by 1 row. If blocked, locks it."""
        if self.game_over or self.current_piece is None:
            return False

        if self.is_valid_position(self.current_piece, offset_y=1):
            self.current_piece.y += 1
            return True
        else:
            self.lock_piece()
            return False

    def hard_drop(self) -> int:
        """Drops piece instantly to bottom and locks it. Returns rows dropped."""
        if self.game_over or self.current_piece is None:
            return 0

        dropped_rows = 0
        while self.is_valid_position(self.current_piece, offset_y=1):
            self.current_piece.y += 1
            dropped_rows += 1

        self.score += dropped_rows * 2  # Hard drop bonus points
        self.lock_piece()
        return dropped_rows

    def rotate_piece(self, clockwise: bool = True) -> bool:
        """Attempts to rotate current piece with simple wall kick support."""
        if self.game_over or self.current_piece is None:
            return False

        rotated_shape = self.current_piece.get_rotated_shape(clockwise=clockwise)

        # Standard rotation check
        if self.is_valid_position(self.current_piece, shape=rotated_shape):
            self.current_piece.shape = rotated_shape
            return True

        # Basic wall kicks (offset left or right by 1 or 2 units)
        for offset_x in [-1, 1, -2, 2]:
            if self.is_valid_position(self.current_piece, offset_x=offset_x, shape=rotated_shape):
                self.current_piece.x += offset_x
                self.current_piece.shape = rotated_shape
                return True

        return False

    def lock_piece(self) -> None:
        """Locks current piece onto grid, triggers line clears, and spawns next piece."""
        if self.current_piece is None:
            return

        for px, py in self.current_piece.get_occupied_positions():
            if 0 <= py < self.height and 0 <= px < self.width:
                self.grid[py][px] = self.current_piece.color

        self.clear_lines()
        self.spawn_next_piece()

    def clear_lines(self) -> int:
        """Identifies and removes completed rows, updating score and level."""
        full_row_indices = [
            r_idx for r_idx, row in enumerate(self.grid)
            if all(cell is not None for cell in row)
        ]

        num_cleared = len(full_row_indices)
        if num_cleared == 0:
            return 0

        # Remove completed rows
        for r_idx in full_row_indices:
            del self.grid[r_idx]
            # Insert new empty row at top
            self.grid.insert(0, [None for _ in range(self.width)])

        # Update stats
        self.lines_cleared += num_cleared
        base_points = self.LINE_SCORES.get(num_cleared, 100 * num_cleared)
        self.score += base_points * (self.level + 1)
        self.level = self.lines_cleared // 10

        return num_cleared
