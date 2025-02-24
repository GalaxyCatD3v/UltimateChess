import pygame
import chess
import chess.engine
import sys
import os

# --- Configuration ---
WIDTH = HEIGHT = 640  # Window size in pixels
DIMENSION = 8  # Chessboard dimensions are 8x8
SQ_SIZE = WIDTH // DIMENSION  # Size of each square
MAX_FPS = 15
IMAGES = {}  # Dictionary to hold the images


# --- Helper Functions ---
def load_images():
    """
    Loads images from the 'images' folder into the global IMAGES dictionary.
    The images should be named 'wp.png', 'wR.png', 'wN.png', 'wB.png', 'wQ.png', 'wK.png',
    'bp.png', 'bR.png', 'bN.png', 'bB.png', 'bQ.png', and 'bK.png'.
    """
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK',
              'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        path = os.path.join("images\png", piece + ".png")
        try:
            image = pygame.image.load(path)
        except pygame.error:
            print(f"Unable to load image at path: {path}")
            sys.exit(1)
        IMAGES[piece] = pygame.transform.scale(image, (SQ_SIZE, SQ_SIZE))


def draw_board(screen):
    """
    Draws the chessboard on the screen.
    """
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """
    Draws the chess pieces on the board based on the current state.
    """
    # Note: In pygame, (0,0) is the top-left; we flip the board vertically
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            square = chess.square(c, 7 - r)
            piece = board.piece_at(square)
            if piece:
                # Mapping chess piece symbols to our image keys
                mapping = {
                    'P': 'wp', 'R': 'wR', 'N': 'wN', 'B': 'wB', 'Q': 'wQ', 'K': 'wK',
                    'p': 'bp', 'r': 'bR', 'n': 'bN', 'b': 'bB', 'q': 'bQ', 'k': 'bK'
                }
                key = mapping[piece.symbol()]
                screen.blit(IMAGES[key], pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# --- Main Game Function ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    load_images()  # Load piece images

    board = chess.Board()
    selected_sq = None  # Stores the selected square (if any) as an index (0-63)
    player_clicks = []  # List to store the player's clicks (source and destination)
    game_over = False

    # --- Set Up Stockfish Engine ---
    # Replace the path below with the actual path to your Stockfish binary.
    STOCKFISH_PATH = "stockfish\\stockfish.exe"
    try:
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
    except Exception as e:
        print(
            "Error initializing Stockfish engine.")
        sys.exit(1)

    running = True
    while running:
        # Human (White) move if it is White's turn
        human_turn = board.turn == chess.WHITE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Process mouse clicks only on human's turn and if the game isn't over
            elif event.type == pygame.MOUSEBUTTONDOWN and human_turn and not game_over:
                location = pygame.mouse.get_pos()  # (x, y) coordinates of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                square = chess.square(col, 7 - row)  # Convert to chess square index

                if selected_sq is None:
                    # Select the piece only if it belongs to the human (white)
                    piece = board.piece_at(square)
                    if piece and piece.color == chess.WHITE:
                        selected_sq = square
                        player_clicks.append(square)
                else:
                    # Second click: attempt to make a move
                    player_clicks.append(square)
                    move = chess.Move(player_clicks[0], player_clicks[1])
                    if move in board.legal_moves:
                        board.push(move)
                        selected_sq = None
                        player_clicks = []
                        # After a legal human move, let the computer play if game isn't over
                        if not board.is_game_over():
                            try:
                                result = engine.play(board, chess.engine.Limit(time=1.0))
                                board.push(result.move)
                            except Exception as e:
                                print("Error during engine move:", e)
                    else:
                        # Reset selection if the move was illegal
                        selected_sq = None
                        player_clicks = []

        draw_board(screen)
        draw_pieces(screen, board)
        pygame.display.flip()
        clock.tick(MAX_FPS)

        # Check for game over
        if board.is_game_over():
            print("Game over:", board.result())
            game_over = True

    engine.quit()
    pygame.quit()


if __name__ == "__main__":
    main()
