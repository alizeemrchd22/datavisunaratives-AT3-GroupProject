import altair as alt
import streamlit as st

from lib import viz


def render(df):
    st.markdown("**Chart A - Notable AI models released each year (count)**")

    counts = df.groupby("year").size().reset_index(name="models")

    bars = alt.Chart(counts).mark_bar(color=viz.TEAL_DARK).encode(
        x=alt.X("year:O", title="Year of publication"),
        y=alt.Y("models:Q", title="Models released (count)"),
    )
    labels = bars.mark_text(dy=-8).encode(text="models:Q")

    st.altair_chart(bars + labels, use_container_width=True)
    st.caption(
        "Every model in the dataset, counted by year of publication. "
        "2026 is not a finished year."
    )
