from board import initial_board, move_piece, capture_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    capture_moves_for_piece,
    legal_moves,
    promote,
    winner,
)


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"
        self.continuation_piece = None

    def print_board(self):
        print("\n " + " ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r} " + " ".join(row))

    def _parse_move(self):
        raw = input(f"{self.player}> ").strip().lower().split()
        if raw == ["q"]:
            return "quit"
        if len(raw) != 4:
            print("Enter four coordinates.")
            return None
        try:
            sr, sc, er, ec = map(int, raw)
        except ValueError:
            print("Coordinates must be numbers.")
            return None
        if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
            print("Outside board.")
            return None
        return (sr, sc), (er, ec)

    def _make_move(self, start, end):
        player = self.player
        if self.continuation_piece is not None and start != self.continuation_piece:
            print("You must continue capturing with the same piece.")
            return False
        if self.board[start[0]][start[1]] not in (player, player + "K"):
            print("That is not your piece.")
            return False

        all_captures = [m for m in legal_moves(self.board, player) if capture_move(self.board, player, *m)]
        is_capture = capture_move(self.board, player, start, end)

        if all_captures and (start, end) not in all_captures:
            print("A capture is available; you must capture.")
            return False
        if is_capture:
            capture_piece(self.board, start, end)
            action = "capture"
        elif simple_move(self.board, player, start, end) and not all_captures:
            move_piece(self.board, start, end)
            action = "move"
        else:
            print("Invalid move.")
            return False

        promoted = promote(self.board)
        if promoted:
            promoted_text = " and promoted to king"
        else:
            promoted_text = ""
        print(f"Accepted: {action} {start[0]} {start[1]} -> {end[0]} {end[1]}{promoted_text}.")

        # Under standard English checkers/WCDF rules, a man that reaches the king-row
        # during a capturing move is crowned and the capturing turn ends immediately.
        if is_capture and promoted:
            self.continuation_piece = None
            return True

        if is_capture:
            extra = capture_moves_for_piece(self.board, player, end)
            if extra:
                self.continuation_piece = end
                print("Another capture is available; continue with the same piece.")
                return "continue"
            self.continuation_piece = None
        else:
            self.continuation_piece = None

        return True

    def run(self):
        print("Checkers — move: sr sc er ec (q to quit)")
        while True:
            self.print_board()
            result = winner(self.board, self.player)
            if result:
                print(f"Game over. {result} wins.")
                return

            parsed = self._parse_move()
            if parsed == "quit":
                print("Game ended by player.")
                return
            if parsed is None:
                continue

            start, end = parsed
            result = self._make_move(start, end)
            if result is False:
                continue
            if result == "continue":
                continue

            opponent = "B" if self.player == "R" else "R"
            game_winner = winner(self.board, opponent)
            if game_winner:
                self.print_board()
                print(f"Game over. {game_winner} wins.")
                return
            self.player = opponent
