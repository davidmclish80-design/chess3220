import chess
from .evaluation import evaluate_board

# Minimax algorithm with Alpha-Beta pruning to find the best evaluation
def minimax(board, depth, alpha, beta, maximizing_player):

    # Stop searching when the depth limit is reached or the game ends
    if depth <= 0 or board.is_game_over(claim_draw=True):
        return evaluate_board(board)

    # Maximizing player (White) searches for the highest evaluation score
    if maximizing_player:
        max_eval = float('-inf')

        # Examine each legal move available
        for move in board.legal_moves:

            # Temporarily make the move on the board
            board.push(move)

            # Recursively evaluate the position from Black's perspective
            evaluation = minimax(board, depth -1, alpha, beta, False)

            # Undo the move to restore the previous board position
            board.pop()

            # Update the highest evaluation found
            max_eval = max(max_eval, evaluation)

            # Alpha stores the best score found so far for the maximizing player
            alpha = max(alpha, max_eval)

            # Stop searching this branch if it cannot improve the result
            if beta <= alpha:
                break

        # Return the highest evaluation found
        return max_eval

    # Minimizing player (Black) searches for the lowest evaluation score
    else:
        min_eval = float('inf')

        # Examine each legal move available
        for move in board.legal_moves:

            # Temporarily make the move on the board
            board.push(move)

            # Recursively evaluate the position from White's perspective
            evaluation = minimax(board, depth - 1, alpha, beta, True)

            # Undo the move to restore the previous board position
            board.pop()

            # Update the lowest evaluation found
            min_eval = min(min_eval, evaluation)

            # Beta stores the best score found so far for the minimizing player
            beta = min(beta, min_eval)

            # Stop searching this branch if it cannot improve the result
            if beta <= alpha:
                break

        # Return the lowest evaluation found
        return min_eval