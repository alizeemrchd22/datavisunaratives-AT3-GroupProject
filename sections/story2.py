
import streamlit as st

from lib import load, viz
from charts import chart_d_new_companies

df = load.year_filter(load.load_models())

st.title("2. The field is opening up")
st.write("New organisations keep arriving, and more models are released openly.")

if not viz.is_empty(df):
    chart_d_new_companies.render(df)

    # Charts E and G will be added here.

viz.footer()
