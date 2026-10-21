
import altair as alt
import streamlit as st

from lib import load, viz


def render(df):
    st.markdown("### Chart D — New organisations entering the AI field")

    # Use the full dataset to identify each organisation's first year.
    # Do not use only the filtered years, or older organisations may look new.
    all_models = load.load_models()

    if "org" not in all_models.columns or "year" not in all_models.columns:
        st.warning("The dataset needs 'org' and 'year' columns for Chart D.")
        return

    organisations = all_models.dropna(subset=["org", "year"]).copy()
    organisations["org"] = organisations["org"].astype(str).str.strip()
    organisations = organisations[organisations["org"] != ""]

    first_year = (
        organisations.groupby("org", as_index=False)["year"]
        .min()
        .rename(columns={"year": "first_year"})
    )

    counts = (
        first_year[first_year["first_year"] >= load.START_YEAR]
        .groupby("first_year")
        .size()
        .reset_index(name="organisations")
        .rename(columns={"first_year": "year"})
    )

    # Match the year range selected in the app's sidebar.
    years_shown = sorted(df["year"].dropna().unique())
    counts = counts[counts["year"].isin(years_shown)]

    if counts.empty:
        st.info("No new organisations found for the selected years.")
        return

    bars = alt.Chart(counts).mark_bar(color=viz.TEAL_DARK).encode(
        x=alt.X("year:O", title="Year first releasing a model"),
        y=alt.Y("organisations:Q", title="New organisations (count)"),
        tooltip=["year:O", "organisations:Q"],
    )

    labels = bars.mark_text(dy=-8).encode(text="organisations:Q")

    st.altair_chart((bars + labels).properties(height=350), width="stretch")

    st.caption(
        "Each organisation is counted once, in its earliest recorded publication "
        "year across the full dataset. Earlier records are retained so existing "
        "organisations are not incorrectly counted as new."
    )
