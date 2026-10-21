import streamlit as st

from lib import load, viz

df = load.year_filter(load.load_models())

st.title("2. The field is opening up")
st.write("New organisations keep arriving, and more models are released openly.")

if not viz.is_empty(df):
    # Student C : charts D et E ici. Student D : chart G en dessous.
    st.info("Charts D, E and G go here.")

viz.footer()
