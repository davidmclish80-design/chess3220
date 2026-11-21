import chess

from .evaluation import evaluate_board


def Max(board, depth, agent_color, alpha = float("-inf"), beta = float("inf"), stats = None):
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
                score = Min(board, depth - 1, agent_color, alpha, beta, stats)
            # except Exception as e:
            #     print("Error => ", e)
            #     print(f"\nError type => {type(e).__name__}\n")
            finally:
                board.pop()
            best_score = max(best_score, score)
            if alpha < best_score:
                alpha = best_score
            #PRUNING BELOW IF REQUIRED
            if alpha >= beta:
                if stats is not None:
                    stats["prunes"] += 1
                break

    return best_score
    

def Min(board, depth, agent_color, alpha = float("-inf"), beta = float("inf"), stats = None):
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
                score = Max(board, depth - 1, agent_color, alpha, beta, stats)
            # except Exception as e:
            #     print("Error => ", e)
            #     print(f"\nError type => {type(e).__name__}\n")
            finally:
                board.pop()
            best_score = min(best_score, score)
            if beta > best_score:
                beta = best_score
            #PRUNING BELOW IF REQUIRED
            if alpha >= beta:
                if stats is not None:
                    stats["prunes"] += 1
                break                        
    return best_score 


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

    # if board.is_checkmate():
    #     return evaluate_board()
    # else:
    #     if board.is_draw(claim =True):
    #         return



# def minimax(board, depth):
#     # BASE CASE
#     if depth == 0 or board.is_game_over(claim_draw=True):
#         return evaluate_board(board)
#     # WHITE'S TURN — MAXIMIZE
#     if board.turn == chess.WHITE:
#         best_score = float("-inf")
#         for move in list(board.legal_moves):
#             board.push(move)
#             score = minimax(board, depth - 1)
#             board.pop()
#             best_score = max(best_score, score)
#         return best_score

#     # BLACK'S TURN — MINIMIZE
#     else:
#         best_score = float("inf")
#         for move in list(board.legal_moves):
#             board.push(move)
#             score = minimax(board, depth - 1)
#             board.pop()
#             best_score = min(best_score, score)
#         return best_score