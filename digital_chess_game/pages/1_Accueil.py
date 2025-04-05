import streamlit as st
from digital_chess_game.pages.chess_board import ChessBoard

if "ChessBoard" not in st.session_state:
    st.session_state["ChessBoard"] = ChessBoard()

st.title("Accueil")

st.header("Bienvenu sur Chess Master App")
