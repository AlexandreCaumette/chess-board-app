import streamlit as st
from PIL import Image
from models.chess_board import ChessBoard

if "ChessBoard" not in st.session_state:
    st.session_state["ChessBoard"] = ChessBoard()

st.set_page_config(
    page_title="Module d'entrée", initial_sidebar_state="expanded", page_icon="📷"
)

st.title("Module d'entrée")

st.divider()

st.header("Prendre le plateau en photo")

st.markdown(
    body="""
Vous devez prendre une photo de votre plateau d'échec, avec une vue de dessus, et en étant le plus proche du plateau.
L'image doit être prise du côté des blancs, i.e. le côté des blancs sera en bas de la photo, tandis que le côté des noirs sera en haut de la photo.
"""
)

picture = st.camera_input(
    label="La caméra de votre appareil est allumée", label_visibility="hidden"
)

if picture is not None:
    current_picture = picture
elif "initial_image" in st.session_state:
    current_picture = st.session_state["initial_image"]
else:
    current_picture = None

st.divider()

if current_picture is not None:
    st.header("Valider la photo du plateau")

    st.markdown(
        body="""
    Vous devez vérifier que la photo que vous avez prise est suffisamment droite et nette.
    Si ce n'est pas le cas, vous pouvez en prendre une nouvelle.
    Si c'est bien le cas, vous pouvez cliquer sur le bouton "Traiter la photo" pour continuer.
    """
    )

    # img = Image.open(current_picture)
    img = Image.open(r"assets\WhatsApp Image 2025-03-02 à 13.21.29_d7b3166c.jpg")
    st.session_state["initial_image"] = img

    st.image(
        image=img, width=300, caption="Aperçu de l'image prise avant le traitement"
    )

    def start_processing():
        st.session_state["processing_status"] = "running"

    st.button(label="Traiter la photo", type="primary", on_click=start_processing)

    st.divider()

    if (
        "processing_status" in st.session_state
        and st.session_state["processing_status"] == "running"
    ):
        with st.spinner(text="Traitement de la photo...", show_time=True):
            st.session_state["ChessBoard"].update_data(img)

            st.switch_page(r"pages/3_Sortie.py")

    if (
        "processing_status" in st.session_state
        and st.session_state["processing_status"] == "completed"
    ):
        st.header("Analyser le traitement")

        st.subheader("Visualiser le pré-traitement de la photo")

        if (
            "error_message" in st.session_state
            and st.session_state["error_message"] is not None
        ):
            st.error(st.session_state["error_message"])

        images_row = st.columns(3)

        if "initial_image" in st.session_state:
            images_row[0].image(
                image=st.session_state["initial_image"], caption="Image de départ"
            )

        if "edged_image" in st.session_state:
            images_row[1].image(
                image=st.session_state["edged_image"],
                caption="1ère mise en relief des contours",
            )

        if "warped_image" in st.session_state:
            images_row[2].image(
                image=st.session_state["warped_image"],
                caption="Image centrée sur l'échiquier",
            )

        images_row = st.columns(3)

        if "edged_image_bis" in st.session_state:
            images_row[0].image(
                image=st.session_state["edged_image_bis"],
                caption="2ème mise en relief des contours",
            )

        if "warped_image_bis" in st.session_state:
            images_row[1].image(
                image=st.session_state["warped_image_bis"],
                caption="Image en sortie du pré-traitement et avant le découpage en case",
            )

        st.subheader("Visualiser les cases identifiées")

        if "squares" in st.session_state:
            grid = st.container(border=True)
            columns = grid.columns(8)

            if (
                "classified_pieces" in st.session_state
                and len(st.session_state["classified_pieces"].values()) > 0
            ):
                labels = st.session_state["classified_pieces"]
            else:
                labels = {}

            for row, col, square in st.session_state["squares"]:
                columns[col].image(
                    image=square,
                    caption=labels[(row, col)] if len(labels.values()) > 0 else None,
                )
