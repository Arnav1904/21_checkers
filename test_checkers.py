import unittest
from board import capture_piece, move_piece
from rules import simple_move, capture_move, legal_moves, capture_moves_for_piece, promote, winner
from game import Checkers


class CheckersTests(unittest.TestCase):
    def empty(self):
        return [['.'] * 8 for _ in range(8)]

    def test_capture_removes_jumped_piece(self):
        b = self.empty(); b[5][0] = 'R'; b[4][1] = 'B'
        self.assertTrue(capture_move(b, 'R', (5,0), (3,2)))
        capture_piece(b, (5,0), (3,2))
        self.assertEqual(b[3][2], 'R'); self.assertEqual(b[4][1], '.'); self.assertEqual(b[5][0], '.')

    def test_forced_capture(self):
        b = self.empty(); b[5][0] = 'R'; b[5][4] = 'R'; b[4][1] = 'B'
        moves = legal_moves(b, 'R')
        self.assertEqual(moves, [((5,0),(3,2))])

    def test_multi_capture_available(self):
        b = self.empty(); b[5][0] = 'R'; b[4][1] = 'B'; b[2][3] = 'B'
        capture_piece(b, (5,0), (3,2))
        self.assertEqual(capture_moves_for_piece(b, 'R', (3,2)), [((3,2),(1,4))])

    def test_multi_capture_forces_same_piece(self):
        game = Checkers()
        game.board = self.empty()
        game.board[5][0] = 'R'
        game.board[4][1] = 'B'
        game.board[2][3] = 'B'
        game.board[5][4] = 'R'
        self.assertEqual(game._make_move((5,0), (3,2)), 'continue')
        self.assertEqual(game.continuation_piece, (3,2))
        self.assertFalse(game._make_move((5,4), (4,3)))
        self.assertEqual(game.continuation_piece, (3,2))
        self.assertTrue(game._make_move((3,2), (1,4)))
        self.assertIsNone(game.continuation_piece)

    def test_king_moves_both_directions(self):
        b = self.empty(); b[3][3] = 'RK'
        self.assertTrue(simple_move(b, 'R', (3,3), (2,2)))
        self.assertTrue(simple_move(b, 'R', (3,3), (4,4)))
        b[2][2] = 'B'; self.assertTrue(capture_move(b, 'R', (3,3), (1,1)))
        b[2][2] = '.'; b[4][4] = 'B'; self.assertTrue(capture_move(b, 'R', (3,3), (5,5)))

    def test_promotion(self):
        b = self.empty(); b[1][2] = 'R'; b[6][5] = 'B'
        self.assertEqual(len(promote(b)), 0)
        move_piece(b, (1,2), (0,1)); self.assertEqual(b[0][1], 'R')
        promoted = promote(b); self.assertEqual(b[0][1], 'RK'); self.assertTrue(promoted)
        move_piece(b, (6,5), (7,4)); promote(b); self.assertEqual(b[7][4], 'BK')

    def test_promotion_ends_capturing_turn(self):
        game = Checkers()
        game.board = self.empty()
        game.board[2][1] = 'R'
        game.board[1][2] = 'B'
        game.board[1][4] = 'B'  # would be capturable backward after promotion
        self.assertTrue(game._make_move((2,1), (0,3)))
        self.assertEqual(game.board[0][3], 'RK')
        self.assertIsNone(game.continuation_piece)

    def test_no_piece_win(self):
        b = self.empty(); b[3][3] = 'R'
        self.assertEqual(winner(b, 'B'), 'R')

    def test_no_move_win(self):
        b = self.empty(); b[7][0] = 'B'
        self.assertEqual(winner(b, 'B'), 'R')

    def test_invalid_simple_direction(self):
        b = self.empty(); b[5][0] = 'R'
        self.assertFalse(simple_move(b, 'R', (5,0), (6,1)))
        self.assertFalse(simple_move(b, 'R', (5,0), (4,0)))

    def test_quit_command_is_clean(self):
        from unittest.mock import patch
        from io import StringIO
        from contextlib import redirect_stdout
        game = Checkers()
        out = StringIO()
        with patch('builtins.input', return_value='q'):
            with redirect_stdout(out):
                game.run()
        self.assertIn('Game ended by player.', out.getvalue())


if __name__ == '__main__':
    unittest.main(verbosity=2)
