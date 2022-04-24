from my_forum.models import Board
from flask import g


def is_authenticated(board_id):
    board = Board.query.get(board_id)
    if board is None or board.user_id != g.user.id:
        return False
    return True
