import streamlit as st
from digital_chess_game.pages.chess_board import ChessBoard

if "ChessBoard" not in st.session_state:
    st.session_state["ChessBoard"] = ChessBoard()

st.set_page_config(
    page_title="Module de sortie", initial_sidebar_state="expanded", page_icon="♟️"
)

st.title("Module de sortie")

st.divider()

st.header("Etat actuelle de la partie")

st.image(st.session_state["ChessBoard"].export_board_as_numpy_array())

st.divider()

st.header("Suggestion pour le prochain mouvement")

st.image(st.session_state["ChessBoard"].export_next_board_as_numpy_array())
