"""Terminal rendering logic using ANSI escape codes and ASCII/Unicode box-drawing."""

import sys
from typing import List, Optional
from src.board import Board
from src.pieces import COLOR_RESET


class Renderer:
    BLOCK_CHAR = "██"
    EMPTY_CHAR = " ."
    CLEAR_SCREEN = "\033[2J\033[H"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"

    @classmethod
    def hide_cursor(cls) -> None:
        sys.stdout.write(cls.HIDE_CURSOR)
        sys.stdout.flush()

    @classmethod
    def show_cursor(cls) -> None:
        sys.stdout.write(cls.SHOW_CURSOR)
        sys.stdout.flush()

    @classmethod
    def clear(cls) -> None:
        sys.stdout.write(cls.CLEAR_SCREEN)
        sys.stdout.flush()

    @classmethod
    def render(cls, board: Board) -> str:
        """Renders the game board and HUD as a single formatted terminal string."""
        buffer: List[str] = []

        # Create virtual grid combining locked cells + active piece
        grid_view: List[List[Optional[str]]] = [
            row[:] for row in board.grid
        ]

        if board.current_piece is not None:
            for px, py in board.current_piece.get_occupied_positions():
                if 0 <= py < board.height and 0 <= px < board.width:
                    grid_view[py][px] = board.current_piece.color

        # Header Title
        buffer.append("\033[1;33m  ═══ TETRIS TERMINAL ═══\033[0m\r\n")

        # Top border
        top_border = "╔" + "═" * (board.width * 2) + "╗"
        hud_top = "  ╔════════════════════════╗"
        buffer.append(f"{top_border}{hud_top}\r\n")

        # Side panel lines (exactly board.height lines so HUD box aligns with grid)
        side_panel_lines: List[str] = [
            f"  ║ \033[1;36mSCORE:\033[0m {board.score:<14} ║",
            f"  ║ \033[1;33mLEVEL:\033[0m {board.level:<14} ║",
            f"  ║ \033[1;32mLINES:\033[0m {board.lines_cleared:<14} ║",
            "  ╠════════════════════════╣",
            "  ║ \033[1;35mNEXT PIECE:\033[0m            ║",
        ]

        # Render next piece in 4x4 area inside HUD
        if board.next_piece is not None:
            shape = board.next_piece.shape
            color = board.next_piece.color
            for r in range(4):
                if r < len(shape):
                    row = shape[r]
                    row_cells = []
                    for cell in row:
                        if cell:
                            row_cells.append(f"{color}{cls.BLOCK_CHAR}{COLOR_RESET}")
                        else:
                            row_cells.append("  ")
                    while len(row_cells) < 4:
                        row_cells.append("  ")
                    drawn_row = "".join(row_cells)
                    side_panel_lines.append(f"  ║   {drawn_row}             ║")
                else:
                    side_panel_lines.append("  ║                        ║")
        else:
            for _ in range(4):
                side_panel_lines.append("  ║                        ║")

        side_panel_lines.extend([
            "  ╠════════════════════════╣",
            "  ║ \033[1;37mCONTROLS:\033[0m              ║",
            "  ║  ← / → : Move          ║",
            "  ║    ↑   : Rotate        ║",
            "  ║    ↓   : Soft Drop     ║",
            "  ║  Space : Hard Drop     ║",
            "  ║    Q   : Quit          ║",
        ])

        # Fill remaining lines up to (height - 1) with blank HUD rows, then add HUD bottom border
        while len(side_panel_lines) < board.height - 1:
            side_panel_lines.append("  ║                        ║")

        # Final line of HUD (bottom border of side panel)
        side_panel_lines.append("  ╚════════════════════════╝")

        # Draw grid rows with side panel
        for r_idx in range(board.height):
            row_str = "║"
            for c_idx in range(board.width):
                cell_color = grid_view[r_idx][c_idx]
                if cell_color:
                    row_str += f"{cell_color}{cls.BLOCK_CHAR}{COLOR_RESET}"
                else:
                    row_str += cls.EMPTY_CHAR
            row_str += "║"

            # Append side panel line
            row_str += side_panel_lines[r_idx]

            buffer.append(f"{row_str}\r\n")

        # Bottom border of main board
        bottom_border = "╚" + "═" * (board.width * 2) + "╝"
        buffer.append(f"{bottom_border}\r\n")

        if board.game_over:
            buffer.append("\r\n  \033[1;31m  ═══ GAME OVER ═══\033[0m\r\n")
            buffer.append("   Press 'q' to quit.\r\n")

        return "\033[H" + "".join(buffer)
