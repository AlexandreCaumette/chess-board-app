from class_chess_screen import ChessScreen
from class_chess_stockfish import ChessStockfish
from class_chess_board import ChessBoard
from class_chess_sounds import ChessSounds
from class_chess_vocal import ChessVocal
import pygame
import sys
import chess
import logging


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Add color codes to the log messages
        if record.levelno == logging.DEBUG:
            record.msg = f"\033[94m{record.msg}\033[0m"  # Blue
        elif record.levelno == logging.INFO:
            record.msg = f"\033[92m{record.msg}\033[0m"  # Green
        elif record.levelno == logging.WARNING:
            record.msg = f"\033[93m{record.msg}\033[0m"  # Yellow
        elif record.levelno == logging.ERROR:
            record.msg = f"\033[91m{record.msg}\033[0m"  # Red
        elif record.levelno == logging.CRITICAL:
            record.msg = f"\033[91m{record.msg}\033[0m"  # Red
        return super().format(record)


root_logger = logging.getLogger()
root_logger.setLevel(level=logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    CustomFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
root_logger.addHandler(stream_handler)


class ChessApp:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Main application logger initialized")

        try:
            pygame.init()
            pygame.display.set_caption("Voice-Controlled Chess")

            self.chess_game = ChessBoard()

            self.stockfish = ChessStockfish()

            self.chess_screen = ChessScreen()

            self.vocal = ChessVocal()

            self.sounds = ChessSounds()

            self.running = True
            self.invalid_move_message = ""
            self.best_move_message = ""

        except Exception as err:
            self.logger.critical(msg=err)

    def run(self):
        self.logger.info("Running the application")

        while self.running:
            try:
                self.chess_screen.fill_game_screen(color=(0, 0, 0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.exit()

                self.chess_screen.draw_turn_indicator(
                    board_turn=self.chess_game.board.turn
                )

                self.chess_screen.draw_board(self.chess_game)
                self.chess_screen.draw_bench(
                    captured_pieces=self.chess_game.captured_pieces
                )
                self.chess_screen.draw_pieces(self.chess_game.board)

                self.chess_screen.draw_console(
                    invalid_move_message=self.invalid_move_message,
                    best_move_message=self.best_move_message,
                )
                pygame.display.flip()

                command = self.vocal.recognize_speech()

                if command:
                    self.process_move(command)

            except Exception as err:
                self.logger.warning(err)

    def exit(self):
        self.logger.info("Exiting the application")
        pygame.quit()
        sys.exit()

    def process_move(self, command):
        self.logger.debug(f"Processing move : {command}")

        try:
            self.chess_game.reset_variable()

            if command == "zombie":
                self.sounds.play("zombie")
                self.chess_game.command_walking_dead()
                return

            if command == "roulette":
                self.sounds.play("roulette")
                self.chess_game.command_roulette_russe()
                return

            if command == "annule":
                self.sounds.play("pop_move")
                self.chess_game.rollback_last_move()
                return

            if command == "suggestion":
                best_move = self.stockfish.get_best_move(self.chess_game.board)
                self.best_move_message = f"Mouvement suggéré : {best_move}"
                self.sounds.play("suggestion")
                return

            move = chess.Move.from_uci(command)

            self.logger.debug(f"chess move : <{move}>")

            from_chess_square = chess.parse_square(command[:2])

            if move in self.chess_game.board.legal_moves:
                if self.chess_game.board.is_capture(move):
                    self.sounds.play("capture")  # Play the sound
                    captured_piece = self.chess_game.board.piece_type_at(move.to_square)

                    self.chess_game.captured_pieces[
                        not self.chess_game.board.turn
                    ].append(captured_piece)

                    if captured_piece == chess.PAWN:
                        self.sounds.play("pawn_captured")

                elif (
                    self.chess_game.board.piece_type_at(from_chess_square)
                    == chess.KNIGHT
                ):
                    self.sounds.play("knight")
                elif (
                    self.chess_game.board.piece_type_at(from_chess_square)
                    == chess.BISHOP
                ):
                    self.sounds.play("bishop")
                elif self.chess_game.board.is_castling(move):
                    self.sounds.play("castling")
                elif (
                    self.chess_game.board.piece_type_at(from_chess_square) == chess.KING
                ):
                    self.sounds.play("king")
                elif (
                    self.chess_game.board.piece_type_at(from_chess_square) == chess.ROOK
                ):
                    self.sounds.play("rook")
                else:
                    self.sounds.play("valid_move")

                self.chess_game.board.push(move)

                if self.chess_game.board.is_checkmate():
                    self.logger.info("is checkmate")
                    self.sounds.play("checkmate")
                elif self.chess_game.board.is_check():
                    self.logger.info("is check")
                    self.sounds.play("check")

                self.invalid_move_message = ""  # Clear invalid move message
            else:
                self.logger.warning("the move is not legal")

                self.sounds.play("invalid_move")
                self.invalid_move_message = f"{command} n'est pas un mouvement valide !"

            self.best_move_message = ""  # Clear best move message

        except Exception as err:
            self.logger.error(err)
            self.invalid_move_message = str(err)
