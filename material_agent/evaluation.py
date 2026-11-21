import chess

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def evaluate_board(board):

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -100000
        else:
            return 100000
    if board.is_game_over():
        return 0
    
    score = 0

    for piece_type in PIECE_VALUES:
        value = PIECE_VALUES[piece_type]

        score += len(board.pieces(piece_type, chess.WHITE)) * value

        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    
    return score