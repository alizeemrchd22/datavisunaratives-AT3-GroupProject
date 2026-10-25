import streamlit as st

from charts import chart_a_models_per_year
from lib import load, viz

df = load.load_models()

viz.page_style()

st.title("Are a few companies monopolising AI, or is the field opening up?")
st.write(
    "The answer depends on what you count: training compute, or the number of "
    "models and organisations. This app shows both, for an ACCC competition analyst."
)

col1, col2, col3 = st.columns(3)
col1.metric("Models in the dataset", f"{len(df):,}", border=True)
col2.metric("Organisations", f"{df['org'].nunique():,}", border=True)
col3.metric(
    "Years in the dataset",
    f"{int(df['year'].min())}-{int(df['year'].max())}",
    border=True,
)

with st.container(border=True):
    st.markdown("**What this app lets you do**")
    st.markdown(
        "- **Spot dominant organisations** - who holds the training compute "
        "(page *1. A few companies dominate*)\n"
        "- **Judge how hard it is to enter** - who is arriving, and what it costs "
        "to compete (page *2. The field is opening up*)\n"
        "- **Compare the two measures** before recommending an investigation "
        "(page *3. It depends what you count*)"
    )

st.divider()
# La home montre tout le dataset : le filtre annees ne s'applique pas ici.
chart_a_models_per_year.render(df)

viz.footer()
