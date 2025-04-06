import chess
import logging
import random
from class_chess_stockfish import ChessStockfish


class ChessBoard:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.logger.info("Board initializing")

        self.board = chess.Board()

        self.stockfish = ChessStockfish()

        self.actions = {chess.WHITE: [], chess.BLACK: []}

        self.captured_pieces = {chess.WHITE: [], chess.BLACK: []}
        self.squares_to_highlight = []
        self.forbidden_moves = []

        self.logger.info("Board initialized")

    def reset_custom_lists(self):
        self.forbidden_moves = []
        self.squares_to_highlight = []

    def play_move(self, move: chess.Move):
        self.board.push(move)
        self.reset_custom_lists()

    def play_action(self, action):
        try:
            if action in self.actions[self.board.turn]:
                raise Exception(f"player has already used its <{action}> action")

            self.actions[self.board.turn].append(action)

            self.logger.debug(
                f"action <{action}> registered for player <{self.board.turn}>"
            )

            if action == "zombie":
                self.command_zombie()
                self.board.turn = not self.board.turn
                return

            if action == "magie":
                self.reset_custom_lists()
                self.command_magie()
                self.board.turn = not self.board.turn
                return

            if action == "annule":
                self.command_annule()
                return

            if action == "roulette":
                self.command_roulette()
                self.board.turn = not self.board.turn
                return

            if action == "suggestion":
                best_move = self.stockfish.get_best_move(self.board)
                return f"Mouvement suggéré : {best_move}"

        except Exception as err:
            self.logger.error(err)
            raise err

    def is_move_legal(self, move: chess.Move) -> bool:
        """Verify if a movement is legal, meaning it's a valid chess move, or it's not in the list of forbidden moves (e.g.
        when a move has been rolled back by an action).

        Args:
            move (chess.Move): The movement to verify.

        Returns:
            bool: Whether the move is legal or not.
        """
        if move not in self.board.legal_moves:
            return False

        if move in self.forbidden_moves:
            return False

        return True

    def command_annule(self):
        move = self.board.pop()
        self.logger.debug(f"popped out move : <{move}>")

        self.forbidden_moves.append(move)

        self.squares_to_highlight.append(move.to_square)
        self.squares_to_highlight.append(move.from_square)

    def get_squares_to_highlight(self) -> list:
        return self.squares_to_highlight

    def command_zombie(self):
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

    def get_random_square_with_piece_on_board(self, color):
        squares = [
            sq
            for sq, piece in self.board.piece_map().items()
            if piece.color == color and piece.piece_type != chess.KING
        ]

        if not squares:
            raise Exception("not enough piece to get a random one")

        square = random.choice(squares)

        return square

    def command_magie(self):
        # Select one random piece from white and black
        white_sq = self.get_random_square_with_piece_on_board(color=chess.WHITE)
        black_sq = self.get_random_square_with_piece_on_board(color=chess.BLACK)

        # Get the piece objects
        white_piece = self.board.piece_at(white_sq)
        new_white_piece = white_piece.piece_type

        while new_white_piece == white_piece.piece_type:
            new_white_piece = chess.Piece(
                random.choice(
                    [chess.PAWN, chess.ROOK, chess.KNIGHT, chess.BISHOP, chess.QUEEN]
                ),
                chess.WHITE,
            )

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

    def command_roulette(self):
        for color in [chess.WHITE, chess.BLACK]:
            square = self.get_random_square_with_piece_on_board(color=color)

            self.captured_pieces[color].append(self.board.piece_type_at(square))

            self.board.remove_piece_at(square)

            self.squares_to_highlight.append(square)
