import streamlit as st
from models.chess_board import ChessBoard

if 'ChessBoard' not in st.session_state:
    st.session_state['ChessBoard'] = ChessBoard()

st.title('Accueil')

st.header('Bienvenu sur Chess Master App')