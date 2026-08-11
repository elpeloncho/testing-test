"""Unit tests for pieces module."""

import pytest
from src.pieces import Piece, PieceType, SHAPES, COLORS


def test_piece_creation():
    piece = Piece.create(PieceType.I, x=3, y=1)
    assert piece.piece_type == PieceType.I
    assert piece.x == 3
    assert piece.y == 1
    assert piece.shape == SHAPES[PieceType.I]
    assert piece.color == COLORS[PieceType.I]


def test_piece_rotation_clockwise():
    piece = Piece.create(PieceType.T)
    original_shape = [row[:] for row in piece.shape]
    rotated_shape = piece.get_rotated_shape(clockwise=True)

    # 360 degree rotation should return to original
    piece.rotate(clockwise=True)
    piece.rotate(clockwise=True)
    piece.rotate(clockwise=True)
    piece.rotate(clockwise=True)
    assert piece.shape == original_shape


def test_piece_rotation_counterclockwise():
    piece = Piece.create(PieceType.L)
    cw_rotated = piece.get_rotated_shape(clockwise=True)
    piece.rotate(clockwise=True)
    piece.rotate(clockwise=False)
    assert piece.get_rotated_shape(clockwise=True) == cw_rotated


def test_occupied_positions():
    piece = Piece.create(PieceType.O, x=2, y=5)
    positions = piece.get_occupied_positions()
    expected = [(2, 5), (3, 5), (2, 6), (3, 6)]
    assert sorted(positions) == sorted(expected)


def test_random_piece():
    piece = Piece.random()
    assert isinstance(piece, Piece)
    assert piece.piece_type in PieceType
