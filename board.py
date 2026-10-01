SIZE = 8


def initial_board():
    board = [["."] * SIZE for _ in range(SIZE)]
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"
    return board


def move_piece(board, start, end):
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = "."


def capture_piece(board, start, end):
    """Move a piece two squares diagonally and remove the jumped piece."""
    sr, sc = start
    er, ec = end
    mr, mc = (sr + er) // 2, (sc + ec) // 2
    move_piece(board, start, end)
    board[mr][mc] = "."
