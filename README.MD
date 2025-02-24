# Chess AI with Stockfish

## Overview
This is a simple chess game built using `pygame` and `python-chess`, which allows a human player to play against the Stockfish chess engine. The game provides a graphical interface where the player controls the white pieces and Stockfish plays as black. 

## Features
- Interactive chessboard using `pygame`
- Allows a human player to move pieces by clicking on squares
- Validates legal moves
- Integrates with Stockfish to provide AI moves
- Detects checkmate, stalemate, and other game-ending conditions

## Installation and Setup

### Prerequisites
Ensure you have Python installed on your system (version 3.6+ recommended). You will also need to install the required dependencies and set up Stockfish correctly.

### Step 1: Install Required Libraries
Run the following command to install the necessary Python libraries:

```sh
pip install pygame chess
```

### Step 2: Download and Set Up Stockfish
Stockfish is an open-source chess engine that this program relies on to generate AI moves.

1. Download Stockfish from [the official website](https://stockfishchess.org/download/).
2. Extract the downloaded file to a directory of your choice.
3. Locate the `stockfish.exe` file (on Windows) or the Stockfish binary (on macOS/Linux).
4. Move or copy the Stockfish binary to a folder named `stockfish` inside the project directory.
5. Ensure that the script is pointing to the correct path for Stockfish:

   ```python
   STOCKFISH_PATH = "stockfish/stockfish.exe"  # Update this path if necessary
   ```

### Step 3: Add Piece Images
The game requires chess piece images stored in a directory named `images/png`. Ensure that you have the following images in that folder:

```
images/png/
    wp.png  # White pawn
    wR.png  # White rook
    wN.png  # White knight
    wB.png  # White bishop
    wQ.png  # White queen
    wK.png  # White king
    bp.png  # Black pawn
    bR.png  # Black rook
    bN.png  # Black knight
    bB.png  # Black bishop
    bQ.png  # Black queen
    bK.png  # Black king
```

If you don't have these images, you can find them online (e.g., from chess sprite resources) or create your own.

## How It Works

### Board Representation
The game uses `python-chess` to manage the board state, keeping track of moves, legality, and turn-based play.

### Loading and Displaying Pieces
- The `load_images()` function loads images from the `images/png` folder and scales them to fit the board squares.
- The `draw_board()` function renders an 8x8 chessboard using alternating colors.
- The `draw_pieces()` function places the loaded piece images onto the board based on the `python-chess` board state.

### Handling Player Moves
- The player can click on a piece to select it and then click on a destination square to move it.
- If the move is legal, the board updates accordingly.
- If the move is illegal, the selection resets.

### AI Integration (Stockfish)
- The program spawns a Stockfish process using `chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)`.
- After each player move, the AI calculates its best move within 1 second and executes it.
- The AI move is then applied to the board state.

### Game Over Detection
- The game checks if the board is in a checkmate, stalemate, or other terminal state after each move.
- If the game is over, it prints the result in the console.

## Running the Game
To start the game, run the following command in your terminal or command prompt:

```sh
python game.py
```

Replace `game.py` with the actual name of the Python script containing this code.

## Troubleshooting

### Issue: Stockfish Not Found
**Solution:** Ensure that the `STOCKFISH_PATH` variable correctly points to the `stockfish.exe` file on your system.

### Issue: Piece Images Not Loading
**Solution:** Ensure that the images are in the correct directory (`images/png/`) and named correctly.

### Issue: Pygame Not Installed
**Solution:** Install `pygame` using:

```sh
pip install pygame
```

## License
This project is open-source and free to use. Ensure that you comply with Stockfish's licensing terms if you distribute this project.

## Credits
- Stockfish chess engine ([stockfishchess.org](https://stockfishchess.org/))
- `pygame` for graphical interface
- `python-chess` for board management

