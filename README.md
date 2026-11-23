# chess3220

# Chess AI – Using Minimax and Alpha-Beta Pruning with differing algorithm strategies

## Project Overview

This project implements two chess-playing agents using the Minimax algorithm enhanced with Alpha-Beta pruning. The python-chess library is used to manage board states, validate moves and detect game outcomes.

The project includes a graphical user interface that supports Human vs Agent and Agent vs Agent gameplay, as well as an automated match harness for testing both agents.

## Agent Strategies

### Material-Based Agent

Prioritizes gaining and maintaining a material advantage by assigning numerical values to chess pieces. The agent also uses positional bonuses for pawns and knights and a repetition penalty to discourage repetitive moves.

### Aggressive Agent 

Prioritizes offensive opportunities by evaluating threats, king pressure, piece activity and material balance.

Both agents use Minimax with Alpha-Beta pruning to determine their moves.

## Project Structure

```text
chess3220/
├── material_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── evaluation.py
│   └── minimax.py
├── Aggressive_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── evaluation.py
│   └── minimax.py
├── controller.py
├── gui.py
├── match.py
├── match_games.pgn
├── match_results.txt
├── .gitignore
└── README.md
```

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
