import chess

from .minimax import Max, Min, MaxWithoutPrune, MinWithoutPrune

#Agent function used by controller.py to call an agent to action
#THIS IS THE FUNCTION THAT IS USED
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

    #Notes the moves and their scores to determine the best move as defined by this agent's
    # minimax.py(which uses evalution.py to get scores)
    for move in list(board.legal_moves):
        board.push(move)
        try:
            #Calls Min(), as a move has already been pushed (MOVED FROM MAX NODE TO MIN NODE)
            score = Min(
                board,
                depth - 1,
                agent_color,
                alpha,
                beta
            )
        finally:
            board.pop()

        #WHERE A MOVE IS REMEMBERED, BASED ON THE BETTER SCORE WHEN COMPARED
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