import chess
import chess.pgn
import time

from controller import ChessController

# Match configuration
NUMBER_OF_GAMES = 6
SEARCH_DEPTH = 3


# Run a complete game between the two agents
def play_game(game_number, white, black):

    # Initialize the shared chess controller
    controller = ChessController()
    controller.set_players(white, black)

    board = controller.board

    # Initialize the PGN game record
    game = chess.pgn.Game()
    game.headers["Event"] = "Chess Agent Match"
    game.headers["Round"] = str(game_number)
    game.headers["White"] = white
    game.headers["Black"] = black

    node = game
    move_count = 0

    print(f"\nGame {game_number}")
    print(f"White: {white} | Black: {black}")

    start_time = time.perf_counter()

    # Continue playing until the game ends
    while not board.is_game_over(claim_draw=True):

        # Determine which agent is currently playing
        player = white if board.turn == chess.WHITE else black

        # Save the board position before making the move
        previous_board = board.copy()

        # Execute the current agent's move
        move = controller.make_ai_move(depth=SEARCH_DEPTH)

        # Detect unexpected move-selection failures
        if move is None:
            raise RuntimeError(f"{player} failed to select a move")

        # Convert the move to standard chess notation
        move_notation = previous_board.san(move)

        # Record the move in the PGN game
        node = node.add_variation(move)

        move_count += 1

        # Display each move in the terminal
        print(f"Move {move_count}: {player} - {move_notation}",
              flush=True)

    # Calculate the total execution time
    elapsed_time = time.perf_counter() - start_time

    # Retrieve the final game outcome
    outcome = board.outcome(claim_draw=True)

    result = outcome.result()
    termination = outcome.termination.name

    # Determine the winning agent
    if outcome.winner == chess.WHITE:
        winner = white
    elif outcome.winner == chess.BLACK:
        winner = black
    else:
        winner = "draw"

    # Store the final result in the PGN record
    game.headers["Result"] = result
    game.headers["Termination"] = termination

    # Save every move played during the game
    with open("match_games.pgn", "a", encoding="utf-8") as file:
        file.write(str(game) + "\n\n")

    # Create a summary of the completed game
    summary = (
        f"Game {game_number}\n"
        f"White: {white}\n"
        f"Black: {black}\n"
        f"Winner: {winner}\n"
        f"Result: {result}\n"
        f"Termination: {termination}\n"
        f"Total half-moves: {move_count}\n"
        f"Duration: {elapsed_time:.2f} seconds\n"
    )

    # Save the game summary
    with open("match_results.txt", "a", encoding="utf-8") as file:
        file.write(summary + "\n")

    print("\n" + summary)

    return winner


# Run the complete match and calculate the final scoreline
def run_match():

    results = {
        "material": 0,
        "aggressive": 0,
        "draw": 0
    }

    # Clear previous match records before starting a new match
    with open("match_games.pgn", "w", encoding="utf-8"):
        pass

    with open("match_results.txt", "w", encoding="utf-8") as file:
        file.write("CHESS AGENT MATCH REPORT\n")
        file.write(f"Search depth: {SEARCH_DEPTH}\n")
        file.write(f"Number of games: {NUMBER_OF_GAMES}\n\n")

    match_start = time.perf_counter()

    # Run the specified number of games
    for game_number in range(1, NUMBER_OF_GAMES + 1):

        # Alternate agent colors after every game
        if game_number % 2 == 1:
            white = "material"
            black = "aggressive"
        else:
            white = "aggressive"
            black = "material"

        winner = play_game(game_number, white, black)

        # Update the match statistics
        results[winner] += 1

    total_time = time.perf_counter() - match_start

    # Calculate match points, awarding half a point for each draw
    material_points = results["material"] + results["draw"] * 0.5
    aggressive_points = results["aggressive"] + results["draw"] * 0.5

    # Generate the final match summary
    final_summary = (
        "\nFINAL MATCH RESULTS\n"
        f"Total games: {NUMBER_OF_GAMES}\n"
        f"Material Agent wins: {results['material']}\n"
        f"Aggressive Agent wins: {results['aggressive']}\n"
        f"Draws: {results['draw']}\n"
        f"Material Agent points: {material_points}\n"
        f"Aggressive Agent points: {aggressive_points}\n"
        f"Total duration: {total_time:.2f} seconds\n"
    )

    print(final_summary)

    # Save the final match statistics
    with open("match_results.txt", "a", encoding="utf-8") as file:
        file.write(final_summary)


# Start the automated match
if __name__ == "__main__":
    run_match()