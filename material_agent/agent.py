import chess
from .minimax import minimax

# Select the best legal move using Minimax with Alpha-Beta pruning
def choose_move(board, depth):

    # White maximizes the evaluation score while Black minimizes it
    maximizing_player = board.turn == chess.WHITE

    # Initialize the best score based on the current player
    if maximizing_player:
        best_score = float('-inf')
    else:
        best_score = float('inf')

    # Store the best move found during the search
    best_move = None

    # Evaluate every legal move available to the current player
    for move in board.legal_moves:

        # Temporarily execute the move on the chessboard
        board.push(move)

        # Evaluate the resulting position using Minimax
        evaluation = minimax(
            board,
            depth - 1,
            float('-inf'),
            float('inf'),
            not maximizing_player
        )

        # Discourage repeating positions to reduce repeated-move draws
        if board.is_repetition(2):

            # Reduce the score for White when a position is repeated
            if maximizing_player:
                evaluation -= 0.15

            # Increase the score for Black since Black prefers lower scores
            else:
                evaluation += 0.15

        # Undo the temporary move to restore the original board
        board.pop()

        # White selects the move with the highest evaluation score
        if maximizing_player:
            if evaluation > best_score:
                best_score = evaluation
                best_move = move

        # Black selects the move with the lowest evaluation score
        else:
            if evaluation < best_score:
                best_score = evaluation
                best_move = move

    # Return the best move found by the agent
    return best_move