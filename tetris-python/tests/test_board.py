"""Unit tests for Board grid logic, collisions, line clearing, and scoring."""

import pytest
from src.board import Board
from src.pieces import Piece, PieceType


def test_board_initialization():
    board = Board(width=10, height=20)
    assert board.width == 10
    assert board.height == 20
    assert board.score == 0
    assert board.lines_cleared == 0
    assert board.level == 0
    assert not board.game_over
    assert board.current_piece is not None
    assert board.next_piece is not None


def test_boundary_collisions():
    board = Board(width=10, height=20)
    # Move piece far left
    for _ in range(15):
        board.move_left()
    left_x = board.current_piece.x

    # Attempting to move further left should be blocked
    assert not board.move_left()
    assert board.current_piece.x == left_x

    # Move piece far right
    for _ in range(15):
        board.move_right()
    right_x = board.current_piece.x

    # Attempting to move further right should be blocked
    assert not board.move_right()
    assert board.current_piece.x == right_x


def test_hard_drop():
    board = Board(width=10, height=20)
    initial_piece_type = board.current_piece.piece_type
    dropped_rows = board.hard_drop()
    assert dropped_rows > 0
    assert board.score == dropped_rows * 2
    # After hard drop, current piece should be locked and a new piece spawned
    assert board.current_piece is not None


def test_single_line_clear_and_scoring():
    board = Board(width=10, height=20)
    # Fill row 19 completely except for first cell, then fill first cell
    for c in range(10):
        board.grid[19][c] = "COLOR"

    cleared = board.clear_lines()
    assert cleared == 1
    assert board.lines_cleared == 1
    assert board.score == 100  # 100 * (level 0 + 1)
    # The cleared row should now be empty (inserted at top)
    assert all(cell is None for cell in board.grid[0])


def test_multi_line_clear_and_level_up():
    board = Board(width=10, height=20)
    # Fill bottom 4 rows completely (Tetris clear)
    for r in range(16, 20):
        for c in range(10):
            board.grid[r][c] = "COLOR"

    cleared = board.clear_lines()
    assert cleared == 4
    assert board.lines_cleared == 4
    assert board.score == 800  # 800 * (level 0 + 1)


def test_game_over_when_board_is_full():
    board = Board(width=10, height=20)
    # Fill the entire top rows of the board
    for r in range(5):
        for c in range(10):
            board.grid[r][c] = "COLOR"

    # Spawning next piece should trigger game over
    board.spawn_next_piece()
    assert board.game_over
