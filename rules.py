SIZE = 8


def _directions(piece):
    if piece.endswith("K"):
        return ((-1, -1), (-1, 1), (1, -1), (1, 1))
    return ((-1, -1), (-1, 1)) if piece == "R" else ((1, -1), (1, 1))


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if piece not in (player, player + "K") or board[er][ec] != ".":
        return False
    dr, dc = er - sr, ec - sc
    return (dr, dc) in _directions(piece)


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if piece not in (player, player + "K") or board[er][ec] != ".":
        return False
    dr, dc = er - sr, ec - sc
    if abs(dr) != 2 or abs(dc) != 2:
        return False
    if (dr // 2, dc // 2) not in _directions(piece):
        return False
    mr, mc = (sr + er) // 2, (sc + ec) // 2
    middle = board[mr][mc]
    return middle != "." and not middle.startswith(player)


def legal_moves(board, player):
    captures = []
    simple = []
    for r in range(SIZE):
        for c in range(SIZE):
            piece = board[r][c]
            if piece not in (player, player + "K"):
                continue
            for dr, dc in _directions(piece):
                nr, nc = r + dr, c + dc
                if 0 <= nr < SIZE and 0 <= nc < SIZE and board[nr][nc] == ".":
                    simple.append(((r, c), (nr, nc)))
                jr, jc = r + 2 * dr, c + 2 * dc
                if 0 <= jr < SIZE and 0 <= jc < SIZE and capture_move(board, player, (r, c), (jr, jc)):
                    captures.append(((r, c), (jr, jc)))
    return captures if captures else simple


def capture_moves_for_piece(board, player, start):
    piece = board[start[0]][start[1]]
    if piece not in (player, player + "K"):
        return []
    moves = []
    r, c = start
    for dr, dc in _directions(piece):
        end = (r + 2 * dr, c + 2 * dc)
        if 0 <= end[0] < SIZE and 0 <= end[1] < SIZE and capture_move(board, player, start, end):
            moves.append((start, end))
    return moves


def promote(board):
    promoted = []
    for c in range(SIZE):
        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted.append((0, c, "R"))
        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted.append((SIZE - 1, c, "B"))
    return promoted


def has_pieces(board, player):
    return any(cell in (player, player + "K") for row in board for cell in row)


def has_legal_moves(board, player):
    return bool(legal_moves(board, player))


def winner(board, player_to_move):
    """Return the winner, or None if the game is not over."""
    opponent = "B" if player_to_move == "R" else "R"
    if not has_pieces(board, player_to_move) or not has_legal_moves(board, player_to_move):
        return opponent
    if not has_pieces(board, opponent):
        return player_to_move
    return None
