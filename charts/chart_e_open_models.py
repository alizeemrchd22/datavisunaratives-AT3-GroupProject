
import altair as alt
import streamlit as st
from lib import viz


def render(df):
    st.markdown(
        "### Chart E — Percentage of models with open weights"
    )

    # Show the years required by the group plan.
    data = df[df["year"].between(2018, 2025)].copy()

    # Standardise the open-weight status values.
    data["open_weights"] = (
        data["open_weights"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Exclude unknown status from the percentage denominator.
    known = data[
        data["open_weights"].isin(["yes", "no"])
    ].copy()

    if known.empty:
        st.info(
            "No models with known open-weight status "
            "for the selected years."
        )
        return

    # Calculate the yearly percentage of open-weight models.
    yearly = (
        known.groupby("year")
        .agg(
            known_models=("open_weights", "size"),
            open_models=(
                "open_weights",
                lambda s: (s == "yes").sum(),
            ),
        )
        .reset_index()
    )

    yearly["open_percentage"] = (
        yearly["open_models"]
        / yearly["known_models"]
        * 100
    )

    # Line chart with points.
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
            alt.Tooltip(
                "year:O",
                title="Year",
            ),
            alt.Tooltip(
                "open_percentage:Q",
                title="Open-weight models (%)",
                format=".1f",
            ),
            alt.Tooltip(
                "open_models:Q",
                title="Open models",
            ),
            alt.Tooltip(
                "known_models:Q",
                title="Models with known status",
            ),
        ],
    ).properties(height=350)

    # Percentage labels above every point.
    labels = alt.Chart(yearly).mark_text(
        dy=-12,
        fontSize=12,
        color="#222222",
    ).encode(
        x=alt.X("year:O"),
        y=alt.Y("open_percentage:Q"),
        text=alt.Text(
            "open_percentage:Q",
            format=".1f",
        ),
    )

    # Display the line chart and labels together.
    st.altair_chart(
        chart + labels,
        width="stretch",
    )

    st.caption(
        "Percentage calculated as models marked yes divided by "
        "models marked yes or no for each year. Models with unknown "
        "open-weight status are excluded from the denominator."
    )
