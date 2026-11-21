import chess

from .minimax import Max, Min, MaxWithoutPrune, MinWithoutPrune


def choose_move(board, depth=3):
    if board.is_game_over(claim_draw=True):
        return None
    if depth < 1:
        raise ValueError("Search depth must be at least 1")

    # The current player is our agent
    agent_color = board.turn

    best_score = float("-inf")
    best_move = None

    alpha = float("-inf")
    beta = float("inf")

    for move in list(board.legal_moves):
        board.push(move)
        try:
            score = Min(
                board,
                depth - 1,
                agent_color,
                alpha,
                beta
            )
        finally:
            board.pop()

        if best_move is None or score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, best_score)

    return best_move

#USED TO CONFIRM THAT BOTH PRUNING AND NO PRUNING GIVE THE SAME VALUE(operation testing)
def choose_moveTest(board, depth=3):
    if board.is_game_over(claim_draw=True):
        return None
    if depth < 1:
        raise ValueError("Search depth must be at least 1")

    # The current player is our agent
    agent_color = board.turn

    best_score = float("-inf")
    best_move = None

    alpha = float("-inf")
    beta = float("inf")

    for move in list(board.legal_moves):
        board.push(move)
        try:
            score = MinWithoutPrune(
                board,
                depth - 1,
                agent_color
            )
        finally:
            board.pop()

        if best_move is None or score > best_score:
            best_score = score
            best_move = move
            
    return best_move