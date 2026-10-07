from board import initial_board, move_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    has_pieces,
    has_legal_move,
    player_has_capture,
    get_capture_moves,
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def run(self):
        print("Checkers — move: sr sc er ec")

        while True:
            self.print_board()

            raw = input(f"{self.player}> ").strip().lower().split()

            if raw == ["q"]:
                return

            if len(raw) != 4:
                print("Enter four coordinates.")
                continue

            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
                print("Outside board.")
                continue

            if self.board[sr][sc] not in (self.player, self.player + "K"):
                print("That is not your piece.")
                continue

            start, end = (sr, sc), (er, ec)

            # Forced capture
            if player_has_capture(self.board, self.player):
                if not capture_move(self.board, self.player, start, end):
                    print("A capture is available. You must capture.")
                    continue

            if capture_move(self.board, self.player, start, end):
                move_piece(self.board, start, end)

                # Remove captured piece
                mr = (sr + er) // 2
                mc = (sc + ec) // 2
                self.board[mr][mc] = "."

                # Multi-capture
                while True:
                    captures = get_capture_moves(
                        self.board,
                        self.player,
                        end
                    )

                    if not captures:
                        break

                    self.print_board()
                    raw = input(
                        f"{self.player} capture again (sr sc er ec)> "
                    ).strip().split()

                    if len(raw) != 4:
                        print("Enter four coordinates.")
                        continue

                    try:
                        nsr, nsc, ner, nec = map(int, raw)
                    except ValueError:
                        print("Coordinates must be numbers.")
                        continue

                    next_start = (nsr, nsc)
                    next_end = (ner, nec)

                    if next_start != end or next_end not in captures:
                        print("You must continue capturing with the same piece.")
                        continue

                    move_piece(self.board, next_start, next_end)

                    mr = (nsr + ner) // 2
                    mc = (nsc + nec) // 2
                    self.board[mr][mc] = "."

                    end = next_end

            elif simple_move(self.board, self.player, start, end):
                move_piece(self.board, start, end)

            else:
                print("Invalid move.")
                continue

            promote(self.board)

            next_player = "B" if self.player == "R" else "R"

            if not has_pieces(self.board, next_player):
                print(f"{self.player} wins! {next_player} has no pieces left.")
                return

            if not has_legal_move(self.board, next_player):
                print(f"{self.player} wins! {next_player} has no legal moves.")
                return

            self.player = next_player