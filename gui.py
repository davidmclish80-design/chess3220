import tkinter as tk
from tkinter import ttk, messagebox
import chess

# Import the shared game controller
from controller import ChessController


class ChessGUI:

    # Initialize the main application window and game controller
    def __init__(self, root):

        # Store the main Tkinter window
        self.root = root
        self.root.title("Chess AI - Minimax and Alpha-Beta Pruning")
        self.root.geometry("650x650")

        # Set the application background to black
        self.root.configure(bg="#101014")

        # Initialize the shared chess controller
        self.controller = ChessController()

        # Track the square selected by the human player
        self.selected_square = None
        # Track pending AI moves so restarting does not duplicate them
        self.ai_job = None
        # Create the game mode selection controls
        self.create_game_controls()
         # Create the chessboard interface
        self.create_board()
         # Display the chess pieces
        self.update_board()

     # Create the visual 8x8 chessboard
    def create_board(self):

        # Store references to each square button
        self.squares = {}

        # Create a frame to hold the chessboard
        self.board_frame = tk.Frame(self.root, bg="#101014")
        self.board_frame.pack(pady=20)

        # Generate all 64 chessboard squares
        for row in range(8):
            for col in range(8):

                # Convert row and column into a python-chess square index
                square = chess.square(col, 7 - row)

                

                # Alternate between muted purple and slate grey
                color = "#A99AC5" if (row + col) % 2 == 0 else "#747480"

                # Create a button for each chessboard square
                button = tk.Button(
                    self.board_frame,
                    width=3,
                    height=1,
                    bg=color,
                    font=("Segoe UI Symbol", 18),
                    command=lambda s=square: self.on_square_click(s)
                )

                # Position the button in the grid
                button.grid(row=row, column=col)

                # Save the button for future updates
                self.squares[square] = button

     # Update the visual chessboard to match the current game state
    def update_board(self):

        # Go through all 64 squares
        for square, button in self.squares.items():

            # Get the chess piece currently occupying the square
            piece = self.controller.board.piece_at(square)

            # Display the piece using its Unicode chess symbol
            if piece:
                button.config(text=piece.unicode_symbol())
            else:
                button.config(text="")

            # Restore the square's original color
            row = 7 - chess.square_rank(square)
            col = chess.square_file(square)

            color = "#A99AC5" if (row + col) % 2 == 0 else "#747480"

            button.config(bg=color)


    # Handle a human player clicking a square on the chessboard
    def on_square_click(self, square):

        # Prevent human moves when the game has ended
        if self.controller.board.is_game_over(claim_draw=True):
            return

        # Prevent human input during an AI player's turn
        if self.controller.players[self.controller.board.turn] != "human":
            return

        # Get the piece occupying the clicked square
        piece = self.controller.board.piece_at(square)

        # Select a piece if no square has been selected yet
        if self.selected_square is None:

            # Only allow selection of the current player's pieces
            if piece and piece.color == self.controller.board.turn:
                self.selected_square = square

                # Highlight the selected square
                self.squares[square].config(bg="#C5A3FF")

            return

        # Allow the player to select a different piece
        if piece and piece.color == self.controller.board.turn:
            self.selected_square = square
            self.update_board()
            self.squares[square].config(bg="#C5A3FF")
            return

        # Create a move from the selected square to the destination
        move = chess.Move(self.selected_square, square)

        # Automatically promote pawns to queens when necessary
        selected_piece = self.controller.board.piece_at(self.selected_square)

        if selected_piece.piece_type == chess.PAWN:
            if chess.square_rank(square) in (0, 7):
                move = chess.Move(
                    self.selected_square,
                    square,
                    promotion=chess.QUEEN
                )

        # Ask the controller to validate and execute the move
        success = self.controller.make_human_move(move.uci())

        # Clear the selection and refresh the chessboard
        self.selected_square = None
        self.update_board()

        # Notify the player if the move was illegal
        if not success:
            messagebox.showwarning("Illegal Move", "That move is not allowed.")
            return
        # Check whether the human move ended the game
        if self.controller.board.is_game_over(claim_draw=True):
            self.check_game_over()
            return

        # Schedule the AI's response after a successful human move
        self.ai_job = self.root.after(500, self.process_ai_turn)


     # Create the dropdown menu and button for selecting a game mode
    def create_game_controls(self):

        self.control_frame = tk.Frame(
            self.root,
            bg="#101014"
        )
        self.control_frame.pack(pady=10)

        # Available players for either color
        player_options = [
            "Human",
            "Material Agent",
            "Aggressive Agent"
        ]

        # White player selection
        tk.Label(
            self.control_frame,
            text="White:",
            bg="#101014",
            fg="white",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5)

        self.white_player = tk.StringVar(value="Human")

        ttk.Combobox(
            self.control_frame,
            textvariable=self.white_player,
            values=player_options,
            state="readonly",
            width=18
        ).grid(row=0, column=1, padx=5)

        # Black player selection
        tk.Label(
            self.control_frame,
            text="Black:",
            bg="#101014",
            fg="white",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=5, pady=5)

        self.black_player = tk.StringVar(value="Material Agent")

        ttk.Combobox(
            self.control_frame,
            textvariable=self.black_player,
            values=player_options,
            state="readonly",
            width=18
        ).grid(row=1, column=1, padx=5)

        # Start the selected game
        self.start_button = tk.Button(
            self.control_frame,
            text="Start Game",
            command=self.start_game,
            bg="#8064A2",
            fg="white",
            font=("Arial", 11)
        )

        self.start_button.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10
        )

        # Start a new game with the selected White and Black players
    def start_game(self):

        # Convert dropdown names into controller player types
        player_types = {
            "Human": "human",
            "Material Agent": "material",
            "Aggressive Agent": "aggressive"
        }

        # Get the selected players
        white = player_types[self.white_player.get()]
        black = player_types[self.black_player.get()]

        # Cancel any AI move scheduled from the previous game
        if self.ai_job is not None:
            self.root.after_cancel(self.ai_job)
            self.ai_job = None

        # Reset the board and assign players
        self.controller.set_players(white, black)

        # Clear the previous selection
        self.selected_square = None

        # Refresh the chessboard
        self.update_board()

        # Start the AI automatically if White is an agent
        if white != "human":
            self.ai_job = self.root.after(500, self.process_ai_turn)

    # Execute an AI move and update the graphical chessboard
    def process_ai_turn(self):
        # Clear the scheduled job because it is now executing
        self.ai_job = None

        # Stop if the game has already ended
        if self.controller.board.is_game_over(claim_draw=True):
            self.check_game_over()
            return

        # Identify the player whose turn it is
        current_player = self.controller.players[self.controller.board.turn]

        # Only continue if the current player is an AI agent
        if current_player == "human":
            return

        # Ask the controller to calculate and execute the AI move
        move = self.controller.make_ai_move(depth=3)

        # Stop if the agent could not produce a move
        if move is None:
            return

        # Refresh the board to display the AI's move
        self.update_board()

        # Check whether the game has ended
        if self.controller.board.is_game_over(claim_draw=True):
            self.check_game_over()
            return

        # Schedule another AI move if the next player is also an agent
        next_player = self.controller.players[self.controller.board.turn]

        if next_player != "human":
            self.ai_job = self.root.after(500, self.process_ai_turn)

     # Check whether the game has ended and display the result
    def check_game_over(self):

        # Get the current chessboard
        board = self.controller.board

        # Stop if the game is still ongoing
        if not board.is_game_over(claim_draw=True):
            return

        # Determine the outcome of the game
        outcome = board.outcome(claim_draw=True)

        # Check whether the game ended in a draw
        if outcome.winner is None:
            result = f"Draw: {board.outcome(claim_draw=True).termination.name}"

        # Check whether White won
        elif outcome.winner == chess.WHITE:
            result = "White wins!"

        # Otherwise, Black won
        else:
            result = "Black wins!"

        # Display the result to the user
        messagebox.showinfo("Game Over", result)

# Launch the chess application
if __name__ == "__main__":

    # Create the main Tkinter window
    root = tk.Tk()

    # Initialize the chess GUI
    app = ChessGUI(root)

    # Keep the application running until the window is closed
    root.mainloop()