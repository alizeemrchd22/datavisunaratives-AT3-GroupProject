
import altair as alt
import streamlit as st

from lib import load, viz


def render(df):
    st.markdown("**Chart D - New organisations releasing AI models each year**")

    # Use all years to find each organisation's first model year.
    # The chart itself starts at the narrative's START_YEAR.
    required = {"publication_date", "year"}
    if not required.issubset(df.columns):
        st.warning("Required publication date or year data is unavailable.")
        return

    company_col = next(
        (c for c in ["organisation", "organization", "company", "company_name"]
         if c in df.columns),
        None,
    )
    if company_col is None:
        st.warning("The cleaned organisation-name column was not found.")
        return

    work = df.dropna(subset=[company_col, "year"]).copy()
    work[company_col] = work[company_col].astype(str).str.strip()
    work = work[work[company_col] != ""]

    first_year = (
        work.groupby(company_col)["year"]
        .min()
        .reset_index(name="first_year")
    )
    counts = (
        first_year[first_year["first_year"] >= load.START_YEAR]
        .groupby("first_year")
        .size()
        .reset_index(name="organisations")
        .rename(columns={"first_year": "year"})
    )

    if counts.empty:
        st.info("No new organisations found for these years.")
        return

    bars = alt.Chart(counts).mark_bar(color=viz.TEAL_DARK).encode(
        x=alt.X("year:O", title="First year releasing a model"),
        y=alt.Y("organisations:Q", title="New organisations (count)"),
        tooltip=["year:O", "organisations:Q"],
    )
    labels = bars.mark_text(dy=-8).encode(text="organisations:Q")

    st.altair_chart(bars + labels, width="stretch")
    st.caption(
        "An organisation is counted once, in the first year it released a model. "
        "Earlier records are retained to identify previously active organisations. "
        "2026 is not a finished year."
    )
