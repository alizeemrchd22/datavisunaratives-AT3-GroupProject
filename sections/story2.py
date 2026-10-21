
import streamlit as st
from charts import chart_d_new_companies, chart_e_open_models
from lib import load, viz


df = load.year_filter(load.load_models())

st.title("2. The field is opening up")
st.write("New organisations keep arriving, and more models are released openly.")

if not viz.is_empty(df):
    chart_d_new_companies.render(df)
    chart_e_open_models.render(df)

    # Student D: Chart G goes here.

    # Charts E and G will be added here.

viz.footer()
