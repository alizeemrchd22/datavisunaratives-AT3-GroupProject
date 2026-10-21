import streamlit as st

from charts import chart_b_compute_share, chart_c_org_type
from lib import load, viz

df = load.year_filter(load.load_models())

st.title("1. A few companies dominate")
st.write("Who owns the training compute, and who builds the models.")

if not viz.is_empty(df):
    chart_b_compute_share.render(df)
    st.divider()
    chart_c_org_type.render(df)

viz.footer()
