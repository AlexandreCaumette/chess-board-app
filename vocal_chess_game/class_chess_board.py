import chess
import logging
import random


class ChessBoard:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.logger.info("Board initializing")

        self.board = chess.Board()

        self.actions = {chess.WHITE: [], chess.BLACK: []}

        self.captured_pieces = {chess.WHITE: [], chess.BLACK: []}
        self.squares_to_highlight = []

        self.logger.info("Board initialized")

    def rollback_last_move(self):
        self.board.pop()

    def reset_variable(self):
        self.squares_to_highlight = []

    def get_squares_to_highlight(self) -> list:
        return self.squares_to_highlight

    def command_walking_dead(self):
        self.logger.debug('commande "walking dead"')

        try:
            if "walking dead" in self.actions[self.board.turn]:
                raise Exception("player has already used its walking dead power")

            self.actions[self.board.turn].append("walking dead")

            self.logger.debug(
                f"zombie action registered for player <{self.board.turn}>"
            )

            zombie_piece = random.choice(self.captured_pieces[self.board.turn])

            self.logger.debug(f"zombie piece : <{zombie_piece}>")

            self.captured_pieces[self.board.turn].remove(zombie_piece)

            if self.board.turn == chess.WHITE:
                index_square = 0
                square = chess.SQUARES[index_square]

                while self.board.piece_at(square) is not None:
                    index_square += 1
                    square = chess.SQUARES[index_square]
            else:
                index_square = 63
                square = chess.SQUARES[index_square]

                while self.board.piece_at(square) is not None:
                    index_square -= 1
                    square = chess.SQUARES[index_square]

            self.board.set_piece_at(
                square=square,
                piece=chess.Piece(piece_type=zombie_piece, color=self.board.turn),
            )

            self.squares_to_highlight.append(square)

            self.board.turn = not self.board.turn
        except Exception as err:
            print(err)
            self.logger.error(err)

    def command_roulette_russe(self):
        self.logger.debug('commande "roulette russe"')

        if "roulette" in self.actions[self.board.turn]:
            raise Exception("player has already used its roulette power")

        self.actions[self.board.turn].append("roulette")

        white_squares = [
            sq
            for sq, piece in self.board.piece_map().items()
            if piece.color == chess.WHITE and piece.piece_type != chess.KING
        ]
        black_squares = [
            sq
            for sq, piece in self.board.piece_map().items()
            if piece.color == chess.BLACK and piece.piece_type != chess.KING
        ]

        # Ensure there are pieces to modify
        if not white_squares or not black_squares:
            raise Exception("Pas assez de cases blanches ou noires pour la surprise")

        # Select one random piece from white and black
        white_sq = random.choice(white_squares)
        black_sq = random.choice(black_squares)

        # Get the piece objects
        white_piece = self.board.piece_at(white_sq)
        new_white_piece = white_piece.piece_type

        while new_white_piece == white_piece.piece_type:
            new_white_piece = chess.Piece(random.choice(range(1, 7)), chess.WHITE)

        self.logger.debug(f"new white piece type : <{new_white_piece}>")

        black_piece = self.board.piece_at(black_sq)
        new_black_piece = black_piece.piece_type

        while new_black_piece == black_piece.piece_type:
            new_black_piece = chess.Piece(random.choice(range(1, 7)), chess.BLACK)

        self.logger.debug(f"new black piece type : <{new_black_piece}>")

        # Set the new pieces on the board
        self.board.set_piece_at(white_sq, new_white_piece)
        self.board.set_piece_at(black_sq, new_black_piece)

        self.squares_to_highlight.append(white_sq)
        self.squares_to_highlight.append(black_sq)

        self.board.turn = not self.board.turn
