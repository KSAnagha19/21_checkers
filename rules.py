SIZE = 8


def is_player_piece(piece, player):
    return piece == player or piece == player + "K"


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    piece = board[sr][sc]

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 1 or abs(ec - sc) != 1:
        return False

    # Kings can move in both directions
    if piece == player + "K":
        return True

    # Normal pieces move only forward
    direction = -1 if player == "R" else 1
    return er - sr == direction


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end

    piece = board[sr][sc]

    if board[er][ec] != ".":
        return False

    if abs(er - sr) != 2 or abs(ec - sc) != 2:
        return False

    mr, mc = (sr + er) // 2, (sc + ec) // 2

    # The jumped piece must belong to the opponent
    if board[mr][mc] in (".", player, player + "K"):
        return False

    # Kings can capture in both directions
    if piece == player + "K":
        return True

    # Normal pieces capture only forward
    direction = -1 if player == "R" else 1
    return er - sr == 2 * direction


def get_capture_moves(board, player, start):
    """Return all legal captures for one piece."""
    sr, sc = start
    moves = []

    for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        end = (sr + dr, sc + dc)

        if 0 <= end[0] < SIZE and 0 <= end[1] < SIZE:
            if capture_move(board, player, start, end):
                moves.append(end)

    return moves


def get_legal_moves(board, player, start):
    """Return legal moves for one piece."""
    sr, sc = start
    moves = []

    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        end = (sr + dr, sc + dc)

        if 0 <= end[0] < SIZE and 0 <= end[1] < SIZE:
            if simple_move(board, player, start, end):
                moves.append(end)

    for move in get_capture_moves(board, player, start):
        moves.append(move)

    return moves


def player_has_capture(board, player):
    """Return True if the player has at least one capture."""
    for r in range(SIZE):
        for c in range(SIZE):
            if is_player_piece(board[r][c], player):
                if get_capture_moves(board, player, (r, c)):
                    return True

    return False


def has_pieces(board, player):
    return any(
        is_player_piece(cell, player)
        for row in board
        for cell in row
    )


def has_legal_move(board, player):
    for r in range(SIZE):
        for c in range(SIZE):
            if is_player_piece(board[r][c], player):
                if get_legal_moves(board, player, (r, c)):
                    return True

    return False


def promote(board):
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"