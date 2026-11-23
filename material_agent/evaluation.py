import chess

# Assign material values to each chess piece based on its importance
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # Checkmate is handled separately
}

# Positional bonuses for pawns and knights
POSITION_BONUS = {
    chess.PAWN: 0.02,
    chess.KNIGHT: 0.05
}

# Evaluate the board using material values and positional bonuses
# Positive scores favor White, while negative scores favor Black
def evaluate_board(board):

    # Check for checkmate
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -100000
        else:
            return 100000

    # Check for a drawn game
    if board.is_game_over(claim_draw=True):
        return 0

    score = 0

    # Calculate the material difference
    for piece_type, value in PIECE_VALUES.items():

        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value

    # Add positional bonuses for both players
    for color in [chess.WHITE, chess.BLACK]:

        for piece_type, bonus in POSITION_BONUS.items():

            for square in board.pieces(piece_type, color):

                # Measure distance from the center of the board
                file = chess.square_file(square)
                rank = chess.square_rank(square)

                center_distance = (
                    abs(file - 3.5) +
                    abs(rank - 3.5)
                )

                # Reward pieces closer to the center
                positional_score = (7 - center_distance) * bonus

                if color == chess.WHITE:
                    score += positional_score
                else:
                    score -= positional_score

    # Return the combined material and positional evaluation
    return score