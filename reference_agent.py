import chess
import random
import time

# Import the move selection functions from both agents
from material_agent.agent import choose_move as material_move
from Aggressive_agent.agent import choose_move as aggressive_move

# Set the search depth for both agents
SEARCH_DEPTH = 2


# Selects a random legal move without using an evaluation function
def reference_move(board):
    moves = list(board.legal_moves)
    return random.choice(moves) if moves else None


# Runs a complete game against the reference agent
def test_agent(agent_name, agent_function, agent_color):

    # Initialize a new chess board, move counter and timer
    board = chess.Board()
    move_count = 0
    start_time = time.perf_counter()

    print(f"\nTesting {agent_name}", flush=True)
    print(f"Colour: {'White' if agent_color else 'Black'}")

    # Continue playing until a win, loss or draw occurs
    while not board.is_game_over(claim_draw=True):

        # Determine which agent should make the next move
        if board.turn == agent_color:
            move = agent_function(board, SEARCH_DEPTH)
        else:
            move = reference_move(board)

        # Verify that the selected move is legal
        if move is None or move not in board.legal_moves:
            raise RuntimeError("Invalid move selected")

        # Apply the move to the board and update the move counter
        board.push(move)
        move_count += 1

        print(f"Move {move_count}: {move}", flush=True)

    # Retrieve the game outcome and calculate the execution time
    outcome = board.outcome(claim_draw=True)
    duration = time.perf_counter() - start_time

    # Determine the result from the tested agent's perspective
    if outcome.winner == agent_color:
        result = "Win"
    elif outcome.winner is None:
        result = "Draw"
    else:
        result = "Loss"

    # Return the game statistics as a formatted string
    return (
        f"Agent: {agent_name}\n"
        f"Colour: {'White' if agent_color else 'Black'}\n"
        f"Result: {result}\n"
        f"Termination: {outcome.termination.name}\n"
        f"Total half-moves: {move_count}\n"
        f"Duration: {duration:.2f} seconds\n"
    )


# Displays a summary table of both agents' performances
def print_summary(results):
    print("\nFINAL SUMMARY")
    print("-" * 80)

    # Display the column headings with consistent spacing
    print(f"{'Agent':<20}{'Wins':<8}{'Losses':<8}"
          f"{'Draws':<8}{'White Moves':<15}{'Black Moves':<15}")

    print("-" * 80)

    for name in ["Material Agent", "Aggressive Agent"]:

        # Retrieve the game results belonging to the current agent
        games = [r for r in results if f"Agent: {name}\n" in r]

        # Calculate the total wins, losses and draws
        wins = sum("Result: Win" in r for r in games)
        losses = sum("Result: Loss" in r for r in games)
        draws = sum("Result: Draw" in r for r in games)

        # Initialize the move counts for both colour assignments
        white_moves = "-"
        black_moves = "-"

        for game in games:

            # Extract the total number of half-moves from each result
            moves = game.split("Total half-moves: ")[1].split("\n")[0]

            # Store the move count based on the agent's colour
            if "Colour: White" in game:
                white_moves = moves
            else:
                black_moves = moves

        # Display the agent's statistics in the summary table
        print(f"{name:<20}{wins:<8}{losses:<8}"
              f"{draws:<8}{white_moves:<15}{black_moves:<15}")

    print("-" * 80)


# Tests both agents against the reference agent
def main():

    # Stores the results of all completed games
    results = []

    # Define the agents and their corresponding move selection functions
    agents = [
        ("Material Agent", material_move),
        ("Aggressive Agent", aggressive_move)
    ]

    # Test each agent once as White and once as Black
    for name, function in agents:
        for color in [chess.WHITE, chess.BLACK]:

            # Use a fixed random seed to make the tests reproducible
            random.seed(42)

            # Run the game and store its results
            result = test_agent(name, function, color)
            results.append(result)
            print(result)

    # Save the individual game results to a text file
    with open("reference_results.txt", "w") as file:
        file.write("REFERENCE AGENT TEST RESULTS\n")
        file.write(f"Search depth: {SEARCH_DEPTH}\n\n")
        file.write("\n".join(results))

    # Display the overall performance of both agents
    print_summary(results)


# Run the tests only when this file is executed directly
if __name__ == "__main__":
    main()