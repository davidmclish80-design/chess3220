import chess
from .evaluation import evaluate_board

def minimax(board, depth, alpha, beta,  maximizing_player):


    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')

        for move in board.legal_moves:
            board.push(move)

            evaluation = minimax(board, depth -1, alpha, beta, False)

            board.pop()

            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, max_eval)

            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')

        for move in board.legal_moves:
            board.push(move)

            evaluation = minimax(board, depth - 1, alpha, beta, True)

            board.pop()

            min_eval = min(min_eval, evaluation)
            beta = min(beta, min_eval)

            if beta <= alpha:
                break

        return min_eval
