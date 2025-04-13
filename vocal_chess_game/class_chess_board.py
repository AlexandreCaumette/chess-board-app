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

            if action == "annule":
                self.command_annule()
                return

            if action == "suggestion":
                best_move = self.stockfish.get_best_move(self.board)
                return f"Mouvement suggéré : {best_move}"

            if self.board.is_checkmate():
                raise Exception("can't use action when you're checkmate")

            if action == "zombie":
                self.command_zombie()
                self.board.turn = not self.board.turn
                return

            if action == "magie":
                self.reset_custom_lists()
                self.command_magie()
                self.board.turn = not self.board.turn
                return

            if action == "roulette":
                self.command_roulette()
                self.board.turn = not self.board.turn
                return

            if action == "tremblement":
                self.command_tremblement()
                self.board.turn = not self.board.turn
                return

        except Exception as err:
            self.logger.error(err)
            raise err

    def command_tremblement(self):
        side = random.choice([-1, 1])

        columns = ["a", "b", "c", "d", "e", "f", "g", "h"][::side]

        # on parcourt chaque ligne de l'échiquier
        for number in range(1, 9):
            # pour chaque ligne on parcourt chaque colonne
            for index_col in range(8):
                # on repère la case de l'échiquier
                current_square = chess.parse_square(columns[index_col] + str(number))

                # on récupère la pièce sur cette case
                piece = self.board.piece_at(current_square)

                # s'il n'y a pas de pièces sur cette case, on passe
                if piece is None:
                    continue

                self.logger.debug(
                    f"tremblement square <{current_square}> and piece <{piece}>"
                )

                next_squares = [current_square]

                # on regarde la colonne suivante (dans le sens du glissement de terrain)
                index_next_col = index_col - 1

                # on cherche tant que le numéro de la colonne est valide
                while index_next_col >= 0:
                    square = chess.parse_square(columns[index_next_col] + str(number))

                    # si on trouve une pièce sur cette case, on ne peut pas aller plus loin et on s'arrête
                    if self.board.piece_at(square) is not None:
                        break

                    # sinon, on peut aller sur cette case, et on cherche plus loin
                    next_squares.append(square)
                    index_next_col -= 1

                new_square = next_squares[-1]

                if new_square != current_square:
                    self.board.set_piece_at(new_square, piece)
                    self.board.remove_piece_at(current_square)

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
        for color in [chess.WHITE, chess.BLACK]:
            # Select one random piece
            square = self.get_random_square_with_piece_on_board(color=color)

            # Get the piece objects
            piece = self.board.piece_at(square)
            new_piece = piece.piece_type

            while new_piece == piece.piece_type:
                new_piece = chess.Piece(
                    random.choice(
                        [
                            chess.PAWN,
                            chess.ROOK,
                            chess.KNIGHT,
                            chess.BISHOP,
                            chess.QUEEN,
                        ]
                    ),
                    color,
                )

            # Set the new pieces on the board
            self.board.set_piece_at(square, new_piece)

            self.squares_to_highlight.append(square)

    def command_roulette(self):
        for color in [chess.WHITE, chess.BLACK]:
            square = self.get_random_square_with_piece_on_board(color=color)

            self.captured_pieces[color].append(self.board.piece_type_at(square))

            self.board.remove_piece_at(square)

            self.squares_to_highlight.append(square)
