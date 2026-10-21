import altair as alt
import streamlit as st

from lib import load, viz


def render(df):
    st.markdown("**Chart A - Notable AI models released each year (count)**")

    recent = df[df["year"] >= load.START_YEAR]
    counts = recent.groupby("year").size().reset_index(name="models")

    bars = alt.Chart(counts).mark_bar(color=viz.TEAL_DARK).encode(
        x=alt.X("year:O", title="Year of publication"),
        y=alt.Y("models:Q", title="Models released (count)"),
    )
    labels = bars.mark_text(dy=-8).encode(text="models:Q")

    st.altair_chart(bars + labels, width="stretch")
    st.caption(
        f"Every notable model published from {load.START_YEAR} onwards. "
        f"The dataset also holds {len(df) - len(recent)} earlier models, back to "
        f"{int(df['year'].min())}, kept for the new-organisation count. "
        "2026 is not a finished year."
    )
