import chess

#Used in evaluate_threats(). A way to determine which piece is to be attacked if attacking multiple.
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}


#Main function for pushing th aggressive functionality. 
#This function pushes for the ability to attack and kill pieces. 
#Slighty considers pieces defended
def evaluate_threats(board, color):
    score = 0
    for square, piece in board.piece_map().items():
        # Ignore our own pieces
        if piece.color == color:
            continue

        # Ignore the king for ordinary material threats
        if piece.piece_type == chess.KING:
            continue
        
        attackers = board.attackers(color, square)
        if len(attackers) == 0:
            continue
        defenders = board.attackers(piece.color, square)
        piece_value = PIECE_VALUES[piece.piece_type]
        if len(defenders) == 0:
            score += piece_value
        else:
            score += piece_value * 0.5
    return score

#Determines if a piece is being attacked to push the aggressive functionality.
#Slightly considers the pieces defending another piece.
def inspect_threat(board, square, attacker_color):

    target = board.piece_at(square)

    if target is None:
        return None

    # Identify which player owns the target
    defender_color = target.color

    # Find pieces attacking the target
    attackers = board.attackers(attacker_color, square)

    # Find pieces defending the target
    defenders = board.attackers(defender_color, square)

    return {
        "target": target,
        "attackers": attackers,
        "defenders": defenders
    }

#Evaluates pressuse being placed on the enemy king
def evaluate_king_pressure(board, color):
    score = 0
    # Find the enemy king
    enemy_color = not color
    king_square = board.king(enemy_color)
    if king_square is None:
        return 0

    # Get the squares surrounding the enemy king
    surrounding_squares = board.attacks(king_square)

    # Check whether we attack each surrounding square
    for square in surrounding_squares:
        if board.is_attacked_by(color, square):
            score += 1

    # Extra reward for directly attacking the king
    if board.is_attacked_by(color, king_square):
        score += 2
    return score

#evaluate_piece_activity uses this. Center squares provide relatively 
# more access to squares especially depending on the piece in the center.
#More access means greater ability to threathen.
CENTER_SQUARES = {
    chess.D4,
    chess.E4,
    chess.D5,
    chess.E5
}

#This function considers the number of squares being attacked by pieces.
#Greater number of sqaures attacked, means more threats
def evaluate_piece_activity(board, color):
    score = 0
    for square, piece in board.piece_map().items():
        # Only evaluate our own pieces
        if piece.color != color:
            continue
        # Ignore the king for this basic activity score
        if piece.piece_type == chess.KING:
            continue
        
        attacked_squares = board.attacks(square)
        # Reward the number of squares attacked
        score += len(attacked_squares) * 0.1

        # Reward control of the center
        for target in attacked_squares:
            if target in CENTER_SQUARES:
                score += 0.5
    return score



#Adds slight value to the number of pieces remaining to make the agent 
# slightly more aware of its possible disadvantage in numbers
def evaluate_material(board):

    score = 0

    for square, piece in board.piece_map().items():

        value = PIECE_VALUES[piece.piece_type]

        if piece.color == chess.WHITE:
            score += value

        else:
            score -= value

    return score


#Values used to adjust the weights of the scenarios being 
# considerd by the functions above, in the function evaluate_white_perspective()
THREAT_WEIGHT = 1.5
KING_PRESSURE_WEIGHT = 2.0
ACTIVITY_WEIGHT = 0.5
MATERIAL_WEIGHT = 1.0

#This function uses the functions defined above to score the state of the board based on a white playing perspective
def evaluate_white_perspective(board):

    # 1. Handle completed games
    if board.is_checkmate():

        if board.turn == chess.WHITE:
            return -100000

        else:
            return 100000

    if board.is_game_over(claim_draw=True):
        return 0

    # 2. Calculate threats
    white_threats = evaluate_threats(board, chess.WHITE)
    black_threats = evaluate_threats(board, chess.BLACK)

    threat_balance = white_threats - black_threats

    # 3. Calculate king pressure
    white_pressure = evaluate_king_pressure(board, chess.WHITE)
    black_pressure = evaluate_king_pressure(board, chess.BLACK)

    pressure_balance = white_pressure - black_pressure

    # 4. Calculate piece activity
    white_activity = evaluate_piece_activity(board, chess.WHITE)
    black_activity = evaluate_piece_activity(board, chess.BLACK)

    activity_balance = white_activity - black_activity

    # 5. Calculate material balance
    material_balance = evaluate_material(board)

    # 6. Combine the evaluation components
    total_score = (
        THREAT_WEIGHT * threat_balance
        + KING_PRESSURE_WEIGHT * pressure_balance
        + ACTIVITY_WEIGHT * activity_balance
        + MATERIAL_WEIGHT * material_balance
    )

    return total_score


#Since the functions above calculate based on a white perspectve,
# to account for the agent possibly being black, evaulate_board() below
# inverses the score received to make it black's perspective
# if the agent is Black that is.
def evaluate_board(board, agent_color):
    score = evaluate_white_perspective(board)
    return score if agent_color == chess.WHITE else -score