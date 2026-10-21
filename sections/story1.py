import streamlit as st

from lib import load, viz

df = load.year_filter(load.load_models())

st.title("1. A few companies dominate")
st.write("Who owns the training compute, and who builds the models.")

if not viz.is_empty(df):
    # Student B : importe ton module en haut, puis appelle-le ici.
    # from charts import chart_b_compute_share
    # chart_b_compute_share.render(df)
    st.info("Charts B and C go here.")

viz.footer()
