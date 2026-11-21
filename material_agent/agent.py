import chess
from minimax import minimax

def choose_move(board, depth):
    maximizing_player = board.turn ==chess.WHITE

    if maximizing_player:
       best_score = float('-inf')
    else:
        best_score = float('inf')

    best_move = None

    for move in board.legal_moves:
        board.push(move)

        evaluation = minimax(
            board,
            depth - 1,
            float('-inf'),
            float('inf'),
            not maximizing_player
        )

        board.pop()
        if maximizing_player:
            if evaluation > best_score:
                best_score = evaluation
                best_move = move
        else:
            if evaluation < best_score:
                best_score = evaluation
                best_move = move

    return best_move
