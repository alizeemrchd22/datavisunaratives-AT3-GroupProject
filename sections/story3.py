import streamlit as st
from charts import chart_f_compute_vs_models
from lib import load, viz

df = load.year_filter(load.load_models())

st.title("3. It depends what you count")

st.write(
    "Comparing the share of training compute with the share "
    "of models helps us understand concentration in AI."
)

if not viz.is_empty(df):
    chart_f_compute_vs_models.render(df)

viz.footer()
