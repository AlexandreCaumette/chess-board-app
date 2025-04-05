import pygame
import chess
import logging


class ChessScreen:
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
        "white_roulette": (238, 238, 50),
        "black_roulette": (160, 150, 86),
    }
    BENCH_COLOR = (204, 157, 58)
    TEXT_COLOR = (0, 0, 0)
    TURN_INDICATOR_COLOR = (50, 50, 200)
    INVALID_MOVE_COLOR = (200, 0, 0)
    BEST_MOVE_COLOR = (0, 200, 0)

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        try:
            self.logger.info(msg="Screen initializing...")
            pygame.init()

            self.NORMAL_FONT = pygame.font.Font(None, 36)
            self.SMALL_FONT = pygame.font.Font(None, 24)

            self.load_pieces_images()

            self.screen = pygame.display.set_mode(
                (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            )

            self.fill_game_screen(color=(255, 255, 255))

            self.logger.info(msg="Screen initialized")

        except Exception as err:
            self.logger.critical(msg="Screen failed to initialize")
            raise err

    def fill_game_screen(self, color):
        self.screen.fill(color, rect=(0, 0, self.GAME_WIDTH, self.GAME_HEIGHT))

    def load_pieces_images(self):
        piece_images = {}
        piece_symbols = ["p", "n", "b", "r", "q", "k", "P", "N", "B", "R", "Q", "K"]
        for symbol in piece_symbols:
            if symbol.isupper():
                image_filepath = f"vocal_chess_game/assets/pieces/w{symbol.lower()}.png"
            else:
                image_filepath = f"vocal_chess_game/assets/pieces/b{symbol}.png"

            piece_images[symbol] = pygame.transform.scale(
                pygame.image.load(image_filepath), (self.SQUARE_SIZE, self.SQUARE_SIZE)
            )

        self.PIECE_IMAGES = piece_images

    def draw_bench(self, captured_pieces: dict):
        try:
            BLACK_BENCH_Y = self.BOARD_Y - self.BENCH_HEIGHT
            WHITE_BENCH_Y = self.BOARD_Y + self.BOARD_HEIGHT

            self.screen.fill(
                self.BENCH_COLOR,
                rect=(self.BOARD_X, BLACK_BENCH_Y, self.BENCH_WIDTH, self.BENCH_HEIGHT),
            )
            self.screen.fill(
                self.BENCH_COLOR,
                rect=(self.BOARD_X, WHITE_BENCH_Y, self.BENCH_WIDTH, self.BENCH_HEIGHT),
            )

            for index, piece_type in enumerate(captured_pieces["WHITE"]):
                piece_image = self.PIECE_IMAGES[chess.piece_symbol(piece_type).upper()]
                image = pygame.transform.scale(piece_image, (32, 32))

                self.screen.blit(
                    source=image, dest=(self.BOARD_X + index * 20, WHITE_BENCH_Y)
                )

            for index, piece_type in enumerate(captured_pieces["BLACK"]):
                piece_image = self.PIECE_IMAGES[chess.piece_symbol(piece_type)]
                image = pygame.transform.scale(piece_image, (32, 32))

                self.screen.blit(
                    source=image, dest=(self.BOARD_X + index * 20, BLACK_BENCH_Y)
                )

        except Exception as err:
            self.logger.error(err)

    def draw_board(self, chess_game):
        squares_to_highlight = chess_game.get_squares_to_highlight()
        checkers = chess_game.board.checkers()

        for row in range(8):
            for col in range(8):
                color_name = "white" if (row + col) % 2 == 0 else "black"
                square = chess.parse_square(f"{chr(97 + col)}{str(8 - row)}")

                if square in checkers:
                    color_name = f"{color_name}_checker"
                elif square in squares_to_highlight:
                    color_name = f"{color_name}_roulette"

                pygame.draw.rect(
                    surface=self.screen,
                    color=self.SQUARE_COLORS[color_name],
                    rect=(
                        self.BOARD_X + col * self.SQUARE_SIZE,
                        self.BOARD_Y + row * self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                        self.SQUARE_SIZE,
                    ),
                )

        # On écrit le nom des lignes (1, 2, 3, 4, 5, 6, 7, 8) sur la colonne la plus à gauche du plateau
        for row in range(8):
            label = self.SMALL_FONT.render(str(8 - row), True, self.TEXT_COLOR)
            self.screen.blit(
                label, (self.BOARD_X + 5, self.BOARD_Y + row * self.SQUARE_SIZE + 10)
            )

        # On écrit le nom des colonnes (a, b, c, d, e, f, g, h) sur la ligne la plus en bas du plateau
        for col in range(8):
            label = self.SMALL_FONT.render(chr(97 + col), True, self.TEXT_COLOR)
            self.screen.blit(
                label,
                (
                    self.BOARD_X + col * self.SQUARE_SIZE + self.SQUARE_SIZE - 12,
                    self.BOARD_Y + self.BOARD_HEIGHT - 20,
                ),
            )

    def draw_pieces(self, board):
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                col, row = chess.square_file(square), chess.square_rank(square)
                self.screen.blit(
                    self.PIECE_IMAGES[piece.symbol()],
                    (
                        self.BOARD_X + col * self.SQUARE_SIZE,
                        self.BOARD_Y + (7 - row) * self.SQUARE_SIZE,
                    ),
                )

    def draw_turn_indicator(self, board_turn: chess.Color = None):
        if board_turn == chess.WHITE:
            self.fill_game_screen(color=(255, 255, 255))
        elif board_turn == chess.BLACK:
            self.fill_game_screen(color=(0, 0, 0))

    def draw_console(
        self, invalid_move_message: str = None, best_move_message: str = None
    ):
        self.screen.fill(
            color=(220, 220, 220),
            rect=(
                self.CONSOLE_LEFT,
                self.CONSOLE_TOP,
                self.CONSOLE_WIDTH,
                self.CONSOLE_HEIGHT,
            ),
        )

        if invalid_move_message:
            text_surface = self.SMALL_FONT.render(
                invalid_move_message, True, self.INVALID_MOVE_COLOR
            )
            self.screen.blit(
                text_surface, (self.CONSOLE_LEFT + 10, self.CONSOLE_TOP + 5)
            )

        if best_move_message:
            text_surface = self.SMALL_FONT.render(
                best_move_message, True, self.BEST_MOVE_COLOR
            )
            self.screen.blit(
                text_surface, (self.CONSOLE_LEFT + 10, self.CONSOLE_TOP + 20)
            )
