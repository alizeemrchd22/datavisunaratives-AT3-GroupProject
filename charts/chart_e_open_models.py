
import altair as alt
import streamlit as st
from lib import viz


def render(df):
    st.markdown(
        "### Chart E — Percentage of models with open weights"
    )

    data = df[df["year"].between(2018, 2025)].copy()

    # Exclude unknown status from the denominator.
    data["open_weights"] = (
        data["open_weights"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    known = data[data["open_weights"].isin(["yes", "no"])].copy()

    if known.empty:
        st.info("No models with known open-weight status for these years.")
        return

    yearly = (
        known.groupby("year")
        .agg(
            known_models=("open_weights", "size"),
            open_models=("open_weights", lambda s: (s == "yes").sum()),
        )
        .reset_index()
    )

    yearly["open_percentage"] = (
        yearly["open_models"] / yearly["known_models"] * 100
    )

    chart = alt.Chart(yearly).mark_line(
        point=True,
        color=viz.TEAL_DARK,
    ).encode(
        x=alt.X(
            "year:O",
            title="Year",
            axis=alt.Axis(labelAngle=0),
        ),
        y=alt.Y(
            "open_percentage:Q",
            title="Models with open weights (%)",
            scale=alt.Scale(domain=[0, 100]),
        ),
        tooltip=[
            alt.Tooltip("year:O", title="Year"),
            alt.Tooltip(
                "open_percentage:Q",
                title="Open-weight models (%)",
                format=".1f",
            ),
            alt.Tooltip("open_models:Q", title="Open models"),
            alt.Tooltip("known_models:Q", title="Models with known status"),
        ],
    ).properties(height=350)

    st.altair_chart(chart, width="stretch")

    st.caption(
        "Percentage = models marked yes divided by models marked yes or no "
        "in each year. Models with unknown open-weight status are excluded."
    )
