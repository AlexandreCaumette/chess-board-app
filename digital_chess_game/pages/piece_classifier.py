import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from tensorflow.keras.models import load_model
import pickle
import cv2
import streamlit as st
import numpy as np


class PieceClassifier:
    LABEL_ENCODER_PATH = r"chess_piece_model\label_encoder.pkl"
    CLASSIFIER_PATH = r"chess_piece_model\chess_piece_model.keras"

    def __init__(self):
        # Load the LabelEncoder object
        with open(self.LABEL_ENCODER_PATH, "rb") as f:
            self.LabelEncoder = pickle.load(f)

        self.Model = load_model(self.CLASSIFIER_PATH)

    def classify_pieces(self, squares):
        """_summary_

        Args:
            squares (_type_): _description_
            model (_type_): _description_

        Returns:
            list[tuple]: Une liste de couple contenant les informations des pièces avec la structure suivante :
                - [0] : la ligne, entre 1 et 8
                - [1] : la colonne, entre 1 et 8
                - [2] : le nom de la pièce
                - [3] : la couleur de la pièce
        """
        # Classifier les pièces
        piece_positions = []
        st.session_state["classified_pieces"] = {}

        for i, j, square in squares:
            square = cv2.resize(square, (64, 64))
            square = np.expand_dims(square, axis=0) / 255.0
            pred = self.Model.predict(square, verbose=0)
            piece_type = np.argmax(pred, axis=1)[0]
            piece = self.LabelEncoder.inverse_transform([piece_type])[0]

            st.session_state["classified_pieces"][(i, j)] = piece

            if "cell" not in piece:
                piece_positions.append((i, j, piece.split("_")[1], piece.split("_")[0]))

        return piece_positions
