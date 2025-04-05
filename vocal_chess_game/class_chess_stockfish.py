import chess
import chess.engine
import os
import logging


class ChessStockfish:
    STOCKFISH_ENGINE_PATH = os.path.join(
        "models", "stockfish", "stockfish-windows-x86-64-avx2.exe"
    )

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Stockfish initialiazing")

        self.engine = chess.engine.SimpleEngine.popen_uci(self.STOCKFISH_ENGINE_PATH)

        self.logger.info("Stockfish initialized")

    def get_best_move(self, board):
        engine_logger = logging.getLogger("chess.engine")
        engine_logger.setLevel(logging.INFO)
        engine_logger.info("stockfish finding the best move")

        try:
            result = self.engine.play(board, chess.engine.Limit(time=1.0))
            move = result.move.uci()

            self.logger.info(f"stockfish finded the best move : <{move}>")

            return move

        except Exception as err:
            self.logger.error("stockfish failed to find the best move")
            raise err
