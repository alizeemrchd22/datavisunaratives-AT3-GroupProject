import streamlit as st

from lib import load, viz

df = load.year_filter(load.load_models())

st.title("3. It depends what you count")
st.write("Share of compute and share of models, for the same organisations.")

if not viz.is_empty(df):
    # Student A : chart F, avec son propre filtre top 3 / 5 / 10.
    st.info("Chart F goes here.")

viz.footer()
