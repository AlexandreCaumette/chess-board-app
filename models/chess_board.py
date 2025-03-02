from models.image_extractor import ImageExtractor
from models.piece_classifier import PieceClassifier
import os
import chess
import chess.engine
import chess.svg
from PIL import Image
import cairosvg
import streamlit as st


class ChessBoard:
    STOCKFISH_ENGINE_PATH = os.path.join(
        'models',
        'stockfish',
        'stockfish-windows-x86-64-avx2.exe'
    )
    
    def __init__(self):
        self.Board = chess.Board()
        self.ImageExtractor = ImageExtractor()
        self.PieceClassifier = PieceClassifier()

    def update_data(self, image):
        try:
            st.session_state['error_message'] = None
            
            squares = self.ImageExtractor.extract_squares_from_image(image)
            pieces_position = self.PieceClassifier.classify_pieces(squares)
            self.update_board(pieces_position)
            
            st.session_state['processing_status'] = 'completed'
            st.session_state['error_message'] = None
        except Exception as err:
            st.session_state['processing_status'] = 'error'
            st.session_state['error_message'] = str(err)
            print(err)
        
    def suggest_next_move(self):
        self.Engine = chess.engine.SimpleEngine.popen_uci(self.STOCKFISH_ENGINE_PATH)
        
        # Obtenir le meilleur coup
        result = self.Engine.play(self.Board, chess.engine.Limit(time=2.0))

        return result.move

    def update_board(self, pieces_position):
        board = chess.Board(None)

        alphabet = "abcdefgh"

        # Set the pieces on the board
        for i, j, name, color in pieces_position:
            position = f"{alphabet[i]}{j + 1}"

            piece = chess.Piece(
                piece_type=self.chess_type_from_piece(name),
                color=chess.BLACK if "black" in color else chess.WHITE,
            )

            board.set_piece_at(square=chess.parse_square(position), piece=piece)

        self.Board = board

    def export_board_as_png(self):
        svg_data = chess.svg.board(self.Board)

        # Convert SVG to PNG
        png_filename = os.path.join(
            'assets',
            'digital_chessboards',
            "chessboard.png"
        )
        cairosvg.svg2png(bytestring=svg_data.encode("utf-8"), write_to=png_filename)
        
        return png_filename
        
    def export_board_as_numpy_array(self):
        image_path = self.export_board_as_png()        
        return Image.open(image_path)
    
    def export_next_board_as_numpy_array(self):
        image_path = self.export_board_as_png()
        return Image.open(image_path)

    def chess_type_from_piece(self, piece_name: str):
        if piece_name == "pawn":
            return chess.PAWN
        if piece_name == "queen":
            return chess.QUEEN
        if piece_name == "king":
            return chess.KING
        if piece_name == "rook":
            return chess.ROOK
        if piece_name == "bishop":
            return chess.BISHOP
        if piece_name == "horse":
            return chess.KNIGHT
        return None