import chess

from .evaluation import evaluate_board

#Uses evaluation.py to score the board states that are simuated at a node and its branches.
def Max(board, depth, agent_color, alpha = float("-inf"), beta = float("inf"), stats = None):
    #stats is a dictionary passed into the function that can be used to count 
    # the number nodes expanded and the number of prunes by alpha and beta pruning
    # If it is none then the function essentially ignores it.
    # If it is that it is to be tried, a dictionary with keys: nodes, evaluations and prunes
    # and values being 0,   should work when passed into the function.
    if stats is not None:
        stats["nodes"] += 1

    #USED AS THE WORSE VALUEE TO IMPLEMENT ALPHA BETA PRUNING
    best_score = float("-inf")

    #This section calculates the scores at the leaf nodes
    if depth <= 0 or board.is_game_over(claim_draw=True):
        if stats is not None:
            stats["evaluations"] += 1
        return evaluate_board(board, agent_color)
    
    else:
        #Expands the nodes for the moves
        for move in list(board.legal_moves):
            board.push(move)
            try:
                score = Min(board, depth - 1, agent_color, alpha, beta, stats)
            finally:
                board.pop()
            best_score = max(best_score, score)

            #Implements alpha beta pruning
            if alpha < best_score:
                alpha = best_score
            #PRUNING BELOW IF REQUIRED
            if alpha >= beta:
                if stats is not None:
                    stats["prunes"] += 1
                break

    return best_score
    
#Uses evaluation.py to score the board states that are simuated at a node and its branches.
def Min(board, depth, agent_color, alpha = float("-inf"), beta = float("inf"), stats = None):
    #stats is a dictionary passed into the function that can be used to count 
    # the number nodes expanded and the number of prunes by alpha and beta pruning
    # If it is none then the function essentially ignores it.
    # If it is that it is to be tried, a dictionary with keys: nodes, evaluations and prunes
    # and values being 0,   should work when passed into the function.
    if stats is not None:
        stats["nodes"] += 1

    #USED AS THE WORSE VALUEE TO IMPLEMENT ALPHA BETA PRUNING
    best_score = float("inf")

    #This section calculates the scores at the leaf nodes
    if depth <=0 or board.is_game_over(claim_draw=True):
        if stats is not None:
            stats["evaluations"] += 1

        return evaluate_board(board, agent_color)
    else:
        #Expands the nodes for the moves
        for move in list(board.legal_moves):
            board.push(move)
            try:
                score = Max(board, depth - 1, agent_color, alpha, beta, stats)
            finally:
                board.pop()
            best_score = min(best_score, score)

            #Implements alpha beta pruning
            if beta > best_score:
                beta = best_score
            #PRUNING BELOW IF REQUIRED
            if alpha >= beta:
                if stats is not None:
                    stats["prunes"] += 1
                break                        
    return best_score 






#BELOW FUNCTION WAS USED TO CREATE A SLIGHT TEST TO ASCERTAIN IF THE ABOVE FUNCTIONS WERE ACCURATE
def MaxWithoutPrune(board, depth, agent_color, stats = None):
    if stats is not None:
        stats["nodes"] += 1
    best_score = float("-inf")
    if depth <= 0 or board.is_game_over(claim_draw=True):
        if stats is not None:
            stats["evaluations"] += 1
        return evaluate_board(board, agent_color)
    else:
        for move in list(board.legal_moves):
            board.push(move)
            try:
                score = MinWithoutPrune(board, depth - 1, agent_color, stats)
            # except Exception as e:
            #     print("Error => ", e)
            #     print(f"\nError type => {type(e).__name__}\n")
            finally:
                board.pop()
            best_score = max(best_score, score)
    return best_score
    
#BELOW FUNCTION WAS USED TO CREATE A SLIGHT TEST TO ASCERTAIN IF THE ABOVE FUNCTIONS WERE ACCURATE
def MinWithoutPrune(board, depth, agent_color, stats = None):
    if stats is not None:
        stats["nodes"] += 1
    best_score = float("inf")
    if depth <=0 or board.is_game_over(claim_draw=True):
        if stats is not None:
            stats["evaluations"] += 1
        return evaluate_board(board, agent_color)
    else:
        for move in list(board.legal_moves):
            board.push(move)
            try:
                score = MaxWithoutPrune(board, depth - 1, agent_color, stats)
            # except Exception as e:
            #     print("Error => ", e)
            #     print(f"\nError type => {type(e).__name__}\n")
            finally:
                board.pop()
            best_score = min(best_score, score)                            
    return best_score 