import streamlit as st

from lib.load import DOWNLOAD_DATE, SOURCE_NAME, SOURCE_URL

# Palette du groupe. Personne n'ecrit une couleur ailleurs que dans ce fichier.
TEAL_DARK = "#2D5550"   # le compute, partout dans l'app
CAMEL = "#CD9B63"       # le nombre de modeles, partout dans l'app
TEAL = "#3F7D76"
TEAL_LIGHT = "#9CC7C1"
YELLOW = "#F2DC9A"
MINT = "#EDF5F3"
GREY = "#8C9A98"        # "other", et tout ce qui est contexte

# Pour les charts a plusieurs categories (chart C par exemple) :
# on alterne fonce / clair pour que les parts restent distinctes.
SEQUENCE = [TEAL_DARK, CAMEL, TEAL_LIGHT, YELLOW]


def page_style():
    """Le style des cartes, partage par toutes les pages."""
    st.markdown(
        """
        <style>
        [data-testid="stMetric"] {
            background-color: #EDF5F3;
            border: 1px solid #C3DBD6;
            border-radius: 10px;
            padding: 14px 18px;
        }
        [data-testid="stMetricValue"] {
            color: #2D5550;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def is_empty(df, message="No data for the years selected. Widen the year filter."):
    """Un message au lieu d'un graphique vide ou d'une erreur."""
    if len(df) == 0:
        st.warning(message)
        return True
    return False


def footer():
    """Source et date de rafraichissement, visibles sur chaque page."""
    st.divider()
    st.caption(
        f"Source: {SOURCE_NAME} - {SOURCE_URL}. "
        f"Data downloaded {DOWNLOAD_DATE}. Training compute in FLOP."
    )
