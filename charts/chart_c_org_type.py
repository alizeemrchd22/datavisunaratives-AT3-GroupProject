import altair as alt
import streamlit as st

from lib import viz

LABELS = {
    "industry": "Industry",
    "academia": "Academia",
    "industry-academia": "Industry + academia",
    "other": "Other",
}
# Legend order (top to bottom) = stack order on screen (top to bottom).
ORDER = ["Industry", "Academia", "Industry + academia", "Other"]

# Stacking is forced with an explicit `order` channel, because the default
# stacking follows the row order of the data frame, not the legend. Without it
# the legend says Industry first while Academia sits on top of the bar.
STACK_INDEX = {"Other": 0, "Industry + academia": 1, "Academia": 2, "Industry": 3}

MIN_LABEL = 5.0      # below this, the number does not fit inside the band
N_ROW_Y = 104        # where the "n = ..." row sits above the 100% line
Y_MAX = 112


def render(df):
    st.markdown(
        "**Chart C - Who releases the models: type of organisation (% per year)**"
    )

    if len(df) == 0:
        return

    counts = (
        df.assign(org_type=df["org_type"].map(LABELS).fillna("Other"))
        .groupby(["year", "org_type"])
        .size()
        .reset_index(name="models")
    )
    counts["share"] = (
        counts["models"] / counts.groupby("year")["models"].transform("sum") * 100
    ).round(1)
    counts["label"] = counts["share"].map(lambda p: f"{p:.0f}%" if p >= MIN_LABEL else "")
    counts["stack_idx"] = counts["org_type"].map(STACK_INDEX).fillna(9)

    # Centre of each band, computed here rather than left to Vega-Lite: on a text
    # mark the stacked `y` is the top edge of the band, so labels would sit on the
    # boundary (and the top band's label would be cut by the 100% line).
    counts = counts.sort_values(["year", "stack_idx"]).reset_index(drop=True)
    counts["cum"] = counts.groupby("year")["share"].cumsum()
    counts["mid"] = (counts["cum"] - counts["share"] / 2).round(2)

    per_year = counts.groupby("year", as_index=False)["models"].sum()
    per_year["n_label"] = per_year["models"].map(lambda n: f"n={n}")
    per_year["n_y"] = N_ROW_Y

    years = counts["year"].astype(int)
    first, last = int(years.min()), int(years.max())

    bars = alt.Chart(counts).mark_bar(stroke="white", strokeWidth=1.5).encode(
        x=alt.X(
            "year:O",
            title="Year of publication",
            axis=alt.Axis(labelAngle=0),
            scale=alt.Scale(paddingInner=0.3, paddingOuter=0.1),
        ),
        y=alt.Y(
            "share:Q",
            title="Share of models released (%)",
            stack="zero",
            scale=alt.Scale(domain=[0, Y_MAX]),
            axis=alt.Axis(values=[0, 25, 50, 75, 100]),
        ),
        # Ascending stack_idx => Other at the baseline, Industry on top, which is
        # the same top-to-bottom order as the legend.
        order=alt.Order("stack_idx:Q", sort="ascending"),
        color=alt.Color(
            "org_type:N",
            title="Type of organisation",
            sort=ORDER,
            scale=alt.Scale(domain=ORDER, range=viz.SEQUENCE),
        ),
    )

    # Label ink per band: pale on the two dark fills, dark on the two pale fills.
    # A value condition, not a second colour field: a second colour encoding in a
    # layer silently removes the legend from the whole chart.
    ink = alt.condition(
        "datum.org_type === 'Industry' || datum.org_type === 'Academia'",
        alt.value(viz.MINT),
        alt.value(viz.TEAL_DARK),
    )
    labels = alt.Chart(counts).mark_text(fontSize=11).encode(
        x=alt.X("year:O"),
        y=alt.Y("mid:Q", scale=alt.Scale(domain=[0, Y_MAX])),
        text=alt.Text("label:N"),
        color=ink,
    )

    # How many models each column is a 100% share of: a share of 22 models is not
    # the same evidence as a share of 36, and the chart should not hide that.
    ns = alt.Chart(per_year).mark_text(
        fontSize=9, color=viz.GREY, baseline="bottom"
    ).encode(
        x=alt.X("year:O"),
        y=alt.Y("n_y:Q", scale=alt.Scale(domain=[0, Y_MAX])),
        text=alt.Text("n_label:N"),
    )

    st.altair_chart((bars + labels + ns).properties(height=400), width="stretch")

    industry = (
        counts[counts["org_type"] == "Industry"].set_index("year")["share"].to_dict()
    )
    move = ""
    if first in industry and last in industry:
        a, b = industry[first], industry[last]
        move = (
            f"Industry was {a:.0f}% of models in {first} and {b:.0f}% in {last} "
            f"({'down' if b < a else 'up'} {abs(b - a):.0f} points). "
        )

    hidden = int((counts["share"] < MIN_LABEL).sum())
    st.caption(
        f"Years shown: {first}-{last}. Each column adds up to 100% of the models "
        f"released that year, and 'n=' gives how many models that is. "
        f"{move}Percentages are written inside every band wider than "
        f"{MIN_LABEL:.0f}%; the other {hidden} bands are listed in the table below. "
        "'Industry + academia' means at least one organisation of each type was "
        "involved in the model. 2026 is not a finished year."
    )

    with st.expander("All values in this chart (no hovering needed)"):
        table = (
            counts.pivot(index="year", columns="org_type", values="share")
            .reindex(columns=ORDER)
            .fillna(0)
            .round(1)
        )
        table["Models (n)"] = per_year.set_index("year")["models"]
        table.index.name = "Year"
        st.dataframe(table, width="stretch")
