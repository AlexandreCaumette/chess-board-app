import pygame
import chess
import chess.engine
import chess.svg
import speech_recognition as sr
import re
import os
import sys

# Initialize pygame
pygame.init()

# Constants
BOARD_WIDTH, BOARD_HEIGHT = 600, 600
BENCH_WIDTH, BENCH_HEIGHT = BOARD_WIDTH, 40
BOARD_X, BOARD_Y = 30, 30 + BENCH_HEIGHT

GAME_WIDTH, GAME_HEIGHT = (
    BOARD_WIDTH + BOARD_X * 2,
    BOARD_HEIGHT + BOARD_Y + 2 * BENCH_HEIGHT,
)
CONSOLE_WIDTH, CONSOLE_HEIGHT = GAME_WIDTH, 40
CONSOLE_LEFT, CONSOLE_TOP = 0, GAME_HEIGHT
SCREEN_WIDTH, SCREEN_HEIGHT = (
    GAME_WIDTH,
    GAME_HEIGHT + CONSOLE_HEIGHT,
)
SQUARE_SIZE = BOARD_WIDTH // 8
SQUARE_COLORS = {
    "white": (238, 238, 210),
    "black": (118, 150, 86),
    "white_checker": (238, 238, 170),
    "black_checker": (70, 150, 86),
}
BENCH_COLOR = (204, 157, 58)
TEXT_COLOR = (0, 0, 0)
TURN_INDICATOR_COLOR = (50, 50, 200)
INVALID_MOVE_COLOR = (200, 0, 0)
BEST_MOVE_COLOR = (0, 200, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def fill_game_screen(color):
    screen.fill(color, rect=(0, 0, GAME_WIDTH, GAME_HEIGHT))


fill_game_screen(color=(255, 255, 255))

pygame.display.set_caption("Voice-Controlled Chess")

# Load sound
sounds = {
    "knight": pygame.mixer.Sound("assets/sounds/horse.mp3"),
    "valid_move": pygame.mixer.Sound("assets/sounds/piece_move.mp3"),
    "invalid_move": pygame.mixer.Sound("assets/sounds/wrong_move.mp3"),
    "capture": pygame.mixer.Sound("assets/sounds/gun_shot.mp3"),
    "suggestion": pygame.mixer.Sound("assets/sounds/suggestion.mp3"),
    "check": pygame.mixer.Sound("assets/sounds/check.mp3"),
    "bishop": pygame.mixer.Sound("assets/sounds/bishop.mp3"),
    "king": pygame.mixer.Sound("assets/sounds/king.mp3"),
    "castling": pygame.mixer.Sound("assets/sounds/castling_move.mp3"),
    "checkmate": pygame.mixer.Sound("assets/sounds/checkmate.mp3"),
    "pop_move": pygame.mixer.Sound("assets/sounds/pop_move.mp3"),
    "pawn_captured": pygame.mixer.Sound("assets/sounds/pawn_captured.mp3"),
    "rook": pygame.mixer.Sound("assets/sounds/rook.mp3"),
}

# Load piece images
piece_images = {}
piece_symbols = ["p", "n", "b", "r", "q", "k", "P", "N", "B", "R", "Q", "K"]
for symbol in piece_symbols:
    if symbol.isupper():
        image_filepath = f"assets/pieces/w{symbol.lower()}.png"
    else:
        image_filepath = f"assets/pieces/b{symbol}.png"

    piece_images[symbol] = pygame.transform.scale(
        pygame.image.load(image_filepath), (SQUARE_SIZE, SQUARE_SIZE)
    )


# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 20)

invalid_move_message = ""
best_move_message = ""
captured_pieces = {"WHITE": [], "BLACK": []}

# Stockfish engine setup
STOCKFISH_ENGINE_PATH = os.path.join(
    "models", "stockfish", "stockfish-windows-x86-64-avx2.exe"
)
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_ENGINE_PATH)


def draw_bench():
    BLACK_BENCH_Y = BOARD_Y - BENCH_HEIGHT
    WHITE_BENCH_Y = BOARD_Y + BOARD_HEIGHT

    screen.fill(BENCH_COLOR, rect=(BOARD_X, BLACK_BENCH_Y, BENCH_WIDTH, BENCH_HEIGHT))
    screen.fill(BENCH_COLOR, rect=(BOARD_X, WHITE_BENCH_Y, BENCH_WIDTH, BENCH_HEIGHT))

    for index, piece_type in enumerate(captured_pieces["WHITE"]):
        piece_image = piece_images[chess.piece_symbol(piece_type).upper()]
        image = pygame.transform.scale(piece_image, (30, 30))

        screen.blit(source=image, dest=(BOARD_X + index * 20, WHITE_BENCH_Y))

    for index, piece_type in enumerate(captured_pieces["BLACK"]):
        piece_image = piece_images[chess.piece_symbol(piece_type)]
        image = pygame.transform.scale(piece_image, (30, 30))

        screen.blit(source=image, dest=(BOARD_X + index * 20, BLACK_BENCH_Y))


# Draw chessboard
def draw_board(board):
    checkers = board.checkers()

    for row in range(8):
        for col in range(8):
            color_name = "white" if (row + col) % 2 == 0 else "black"
            square = chess.parse_square(f"{chr(97 + col)}{str(8 - row)}")
            color_name = f"{color_name}_checker" if square in checkers else color_name

            pygame.draw.rect(
                surface=screen,
                color=SQUARE_COLORS[color_name],
                rect=(
                    BOARD_X + col * SQUARE_SIZE,
                    BOARD_Y + row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                ),
            )

    # Draw row labels (1-8)
    for row in range(8):
        label = small_font.render(str(8 - row), True, TEXT_COLOR)
        screen.blit(label, (BOARD_X + 5, BOARD_Y + row * SQUARE_SIZE + 10))

    # Draw column labels (a-h)
    for col in range(8):
        label = small_font.render(chr(97 + col), True, TEXT_COLOR)
        screen.blit(
            label,
            (
                BOARD_X + col * SQUARE_SIZE + SQUARE_SIZE - 12,
                BOARD_Y + BOARD_HEIGHT - 20,
            ),
        )


# Draw pieces
def draw_pieces(board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            col, row = chess.square_file(square), chess.square_rank(square)
            screen.blit(
                piece_images[piece.symbol()],
                (BOARD_X + col * SQUARE_SIZE, BOARD_Y + (7 - row) * SQUARE_SIZE),
            )


# Draw turn indicator
def draw_turn_indicator(board):
    if board.turn == chess.WHITE:
        fill_game_screen(color=(255, 255, 255))
    else:
        fill_game_screen(color=(0, 0, 0))


def draw_console():
    screen.fill(
        color=(220, 220, 220),
        rect=(CONSOLE_LEFT, CONSOLE_TOP, CONSOLE_WIDTH, CONSOLE_HEIGHT),
    )

    if invalid_move_message:
        text_surface = small_font.render(invalid_move_message, True, INVALID_MOVE_COLOR)
        screen.blit(text_surface, (CONSOLE_LEFT + 10, CONSOLE_TOP + 5))

    if best_move_message:
        text_surface = small_font.render(best_move_message, True, BEST_MOVE_COLOR)
        screen.blit(text_surface, (CONSOLE_LEFT + 10, CONSOLE_TOP + 20))


def clean_vocal_command(vocal_input: str) -> str:
    # Define the replacement function
    def replacement(match):
        number = match.group(1)
        unit_digit = number[1]
        return f"d{unit_digit}"

    # Correction de la reconnaissance vocale
    command = vocal_input.replace("dessin", "d7")
    command = command.replace("géant", "g1")
    command = command.replace("j'ai ", "g")
    command = command.replace("à ", "a")
    command = command.replace("à", "")
    command = command.replace("recette", "e7")
    command = command.replace("bessette", "b7")
    command = command.replace("baisser", "b7")
    command = command.replace(" ans ", " en ")
    command = command.replace("-", "")
    command = command.replace("un", "1")
    command = command.replace("détroit", "d3")
    command = command.replace("angers ", "en g")
    command = command.replace("aussi", "e6")
    command = command.replace("c'est ", "c ")
    command = command.replace("des ", "d")
    command = command.replace("deux", "2")
    command = command.replace("annuler", "annule")
    command = re.sub(pattern=r"\b(1[0-9])\b", repl=replacement, string=command)
    command = re.sub(pattern=r"\bans\b", repl="en", string=command)
    return command


# Speech recognition function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # print("Enoncez votre mouvement (e.g. 'bouge e2 en e4') :")
        try:
            audio = recognizer.listen(source)
            vocal_input = recognizer.recognize_google(audio, language="fr-FR").lower()

            command = clean_vocal_command(vocal_input)

            print(f"<{vocal_input}> est compris comme <{command}>")

            return command
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Speech recognition service unavailable.")
    return None


# Interpret and apply move
def process_move(command, board):
    try:
        global invalid_move_message, best_move_message, captured_pieces

        words = command.split()

        if "annule" in words:
            sounds["pop_move"].play()
            board.pop()
            return

        if "suggestion" in words:
            best_move_message = get_best_move(board)
            sounds["suggestion"].play()
            return

        if "en" not in words:
            raise Exception("Le mot clé 'en' n'est pas présent dans la commande")

        if len(words) < 3:
            raise Exception("La commande contient moins de 3 éléments")

        if any([len(word) < 2 for word in words]):
            raise Exception("Une des positions n'est pas complète")

        index_en = words.index("en")
        from_square = words[index_en - 1]
        to_square = words[index_en + 1]

        move = chess.Move.from_uci(from_square + to_square)

        from_chess_square = chess.parse_square(from_square)

        if move in board.legal_moves:
            if board.is_capture(move):
                sounds["capture"].play()  # Play the sound
                captured_piece = board.piece_type_at(move.to_square)
                captured_color = "WHITE" if board.color_at(move.to_square) else "BLACK"
                captured_pieces[captured_color].append(captured_piece)

                if captured_piece == chess.PAWN:
                    sounds["pawn_captured"].play()

            elif board.piece_type_at(from_chess_square) == chess.KNIGHT:
                sounds["knight"].play()
            elif board.piece_type_at(from_chess_square) == chess.BISHOP:
                sounds["bishop"].play()
            elif board.is_castling(move):
                sounds["castling"].play()
            elif board.piece_type_at(from_chess_square) == chess.KING:
                sounds["king"].play()
            elif board.piece_type_at(from_chess_square) == chess.ROOK:
                sounds["rook"].play()
            else:
                sounds["valid_move"].play()

            board.push(move)

            if board.is_checkmate():
                sounds["checkmate"].play()
            elif board.is_check():
                sounds["check"].play()

            invalid_move_message = ""  # Clear invalid move message
        else:
            print("Invalid move.")
            sounds["invalid_move"].play()
            invalid_move_message = (
                f"{from_square + to_square} n'est pas un mouvement valide !"
            )

        best_move_message = ""  # Clear best move message

    except Exception as err:
        print(err)
        invalid_move_message = str(err)


# Get best move from Stockfish
def get_best_move(board):
    result = engine.play(board, chess.engine.Limit(time=1.0))
    return f"Mouvement suggéré : {result.move.uci()}"


# Main loop
board = chess.Board()
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    draw_turn_indicator(board)
    draw_board(board)
    draw_bench()
    draw_pieces(board)
    draw_console()
    pygame.display.flip()

    command = recognize_speech()
    if command:
        process_move(command, board)

pygame.quit()
sys.exit()
