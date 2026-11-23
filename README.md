# chess3220

# Chess AI – Using Minimax and Alpha-Beta Pruning with differing algorithm strategies

## Project Overview

This project implements two chess-playing agents using the Minimax algorithm enhanced with Alpha-Beta pruning. The python-chess library is used to manage board states, validate moves and detect game outcomes.

The project includes a graphical user interface that supports Human vs Agent and Agent vs Agent gameplay, as well as an automated match harness for testing both agents. Additionally, a basic reference agent is used to evaluate the performance of both chess-playing agents against a random-move strategy.

## Algorithm Strategies for Agent 

### Material-Based Agent

Prioritizes gaining and maintaining a material advantage by assigning numerical values to chess pieces. The agent also uses positional bonuses for pawns and knights and a repetition penalty to discourage repetitive moves.

### Aggressive Agent 

Prioritizes offensive opportunities by evaluating threats, king pressure, piece activity and material balance.

Both agents use Minimax with Alpha-Beta pruning to determine their moves.

### Reference Agent

Randomly selects legal chess moves without using a search algorithm or evaluation function. It serves as a basic reference for testing the effectiveness of both chess-playing agents.


## File Descriptions

- **`__init__.py`** – Identifies each agent directory as a Python package, allowing its modules to be imported.
- **`agent.py`** – Selects the most favourable move using the Minimax search results.
- **`evaluation.py`** – Evaluates board positions based on the agent's individual strategy.
- **`minimax.py`** – Implements the Minimax algorithm with Alpha-Beta pruning.
- **`controller.py`** – Manages the shared board state, player selection, move validation and integration of both agents.
- **`gui.py`** – Implements the graphical chess interface using Tkinter.
- **`match.py`** – Runs automated games between both agents, alternates their colours and records the results.
- **`match_games.pgn`** – Stores the moves and outcomes of completed automated games.
- **`match_results.txt`** – Stores individual game statistics and the overall match results.
- **`reference_agent.py`** – Implements a basic random-move agent, automatically tests both chess-playing
        agents against it and displays a summary table of their performances.

- **`reference_results.txt`** – Stores individual game results and statistics from the reference-agent tests.
- **`.gitignore`** – Prevents unnecessary files, such as Python cache files and virtual environments, from being tracked.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/davidmclish80-design/chess3220.git
cd chess3220
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows (Git Bash):

```bash
source venv/Scripts/activate
```

Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source venv/bin/activate
```

### 4. Install the required dependency

```bash
pip install python-chess
```

Tkinter is included with most standard Python installations. If unavailable, it must be installed separately.

## Running the Application

Launch the graphical user interface:

```bash
python gui.py
```

### Human vs Agent

1. Select Human as either the White or Black player.
2. Select Material Agent or Aggressive Agent as the opposing player.
3. Start the game.
4. Select a piece and its destination square to make a move.
5. The selected agent will automatically respond.

### Agent vs Agent

1. Select Material Agent as one player.
2. Select Aggressive Agent as the opposing player.
3. Start the game.
4. Both agents will automatically play against each other.

The default search depth for GUI gameplay is three.

## Running the Automated Match Harness

To run automated matches without the graphical interface:

```bash
python match.py
```

By default, the match harness runs six games at a search depth of three, alternating the colours of both agents after each game.

The number of games and search depth can be modified using the `NUMBER_OF_GAMES` and `SEARCH_DEPTH` constants in `match.py`.

Upon completion, the match harness records the moves in `match_games.pgn` and the match statistics in `match_results.txt`. 
Running the match harness again overwrites the previous match records.

## Running the Reference Agent Tests

To test both chess-playing agents against the basic reference agent:

```bash
python reference_agent.py
```

The program automatically runs four games, with each chess-playing agent playing once as White and once as Black against the reference agent.

Both chess-playing agents use a search depth of two, while the reference agent randomly selects legal moves. A fixed random seed is used to ensure reproducibility.

Upon completion, the program displays a final summary table containing the total wins, losses, draws and number of half-moves played for each colour assignment.

The individual game results and statistics are saved in reference_results.txt.

Running the reference-agent tests again overwrites the previous reference-agent results.\


*Note: AI was used to assist with debugging, testing and documentation.
