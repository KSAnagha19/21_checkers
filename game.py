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

            raw = input(
                f"{self.player}> "
            ).strip().lower().split()

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

            if self.board[sr][sc] not in (
                self.player,
                self.player + "K"
            ):
                print("That is not your piece.")
                continue

            start = (sr, sc)
            end = (er, ec)

            # Track whether this accepted turn is a capture
            # and how many pieces were captured.
            capture_count = 0

            # Check whether the player is forced to capture.
            if player_has_capture(self.board, self.player):
                if not capture_move(
                    self.board,
                    self.player,
                    start,
                    end
                ):
                    print("A capture is available. You must capture.")
                    continue

            # Capture move
            if capture_move(
                self.board,
                self.player,
                start,
                end
            ):
                capture_count = 1

                move_piece(
                    self.board,
                    start,
                    end
                )

                # Remove the jumped opponent piece.
                mr = (sr + er) // 2
                mc = (sc + ec) // 2
                self.board[mr][mc] = "."

                # Continue capturing with the same piece.
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
                        f"{self.player} capture again "
                        "(sr sc er ec)> "
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

                    if (
                        next_start != end
                        or next_end not in captures
                    ):
                        print(
                            "You must continue capturing "
                            "with the same piece."
                        )
                        continue

                    move_piece(
                        self.board,
                        next_start,
                        next_end
                    )

                    # Remove the jumped opponent piece.
                    mr = (nsr + ner) // 2
                    mc = (nsc + nec) // 2
                    self.board[mr][mc] = "."

                    capture_count += 1
                    end = next_end

            # Ordinary move
            elif simple_move(
                self.board,
                self.player,
                start,
                end
            ):
                move_piece(
                    self.board,
                    start,
                    end
                )

            # Invalid move
            else:
                print("Invalid move.")
                continue

            # Check promotion before switching players.
            was_promoted = False

            if (
                self.player == "R"
                and end[0] == 0
                and self.board[end[0]][end[1]] == "R"
            ):
                was_promoted = True

            elif (
                self.player == "B"
                and end[0] == SIZE - 1
                and self.board[end[0]][end[1]] == "B"
            ):
                was_promoted = True

            promote(self.board)

            # Give exactly one success message for the accepted turn.
            if capture_count > 0:
                message = (
                    f"{self.player} captured "
                    f"{capture_count} piece"
                )

                if capture_count > 1:
                    message += "s"

                message += (
                    f" and moved "
                    f"{start[0]},{start[1]} -> "
                    f"{end[0]},{end[1]}"
                )

            else:
                message = (
                    f"{self.player} moved "
                    f"{start[0]},{start[1]} -> "
                    f"{end[0]},{end[1]}"
                )

            if was_promoted:
                message += " and promoted to king"

            print(message)

            # Check whether the next player has lost.
            next_player = (
                "B" if self.player == "R" else "R"
            )

            if not has_pieces(
                self.board,
                next_player
            ):
                print(
                    f"{self.player} wins! "
                    f"{next_player} has no pieces left."
                )
                return

            if not has_legal_move(
                self.board,
                next_player
            ):
                print(
                    f"{self.player} wins! "
                    f"{next_player} has no legal moves."
                )
                return

            self.player = next_player