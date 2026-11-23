import chess

# Import both chess agents and give their move functions unique names
from material_agent.agent import choose_move as material_move
from Aggressive_agent.agent import choose_move as aggressive_move


class ChessController:

    # Initialize a new chess game with the starting board and default players
    def __init__(self):

        # Create a chessboard with all pieces in their starting positions
        self.board = chess.Board()

        # Assign the default players to White and Black
        self.players = {
            chess.WHITE: "human",
            chess.BLACK: "material"
        }
    # Set players and reset the board for a new game
    def set_players(self, white, black):
        self.board.reset()

        self.players = {
            chess.WHITE: white,
            chess.BLACK: black
        }
    def make_human_move(self, move_uci):

        # Prevent moves if the game has already ended
        if self.board.is_game_over(claim_draw=True):
            return False

        # Ensure it is currently the human player's turn
        if self.players[self.board.turn] != "human":
            return False

        # Convert the move from UCI notation into a chess.Move object
        try:
            move = chess.Move.from_uci(move_uci)
        except ValueError:
            return False

        # Reject illegal moves
        if move not in self.board.legal_moves:
            return False

        # Execute the move on the chessboard
        self.board.push(move)

        return True
    
     # Select and execute a move using the current AI agent
    def make_ai_move(self, depth=3):

        # Prevent the AI from moving if the game has ended
        if self.board.is_game_over(claim_draw=True):
            return None

        # Identify which player controls the current turn
        player = self.players[self.board.turn]

        # Ask the Material Agent to select its best move
        if player == "material":
            move = material_move(self.board, depth)

        # Ask the Aggressive Agent to select its best move
        elif player == "aggressive":
            move = aggressive_move(self.board, depth)

        # Do not generate an AI move during a human player's turn
        else:
            return None

        # Ensure the selected move is valid before executing it
        if move is None or move not in self.board.legal_moves:
            return None

        # Update the chessboard with the AI's selected move
        self.board.push(move)

        # Return the move so the GUI can display it
        return move

