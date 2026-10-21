import altair as alt
import streamlit as st

from lib import viz

TOP_N = 10


def render(df):
    st.markdown(
        f"**Chart B - Share of all training compute, top {TOP_N} organisations (%)**"
    )

    # Only models whose training compute is known can be counted at all.
    known = df[df["compute_flops"].notna()]
    if len(known) == 0:
        st.warning(
            "No model in the years selected has a known training compute. "
            "Widen the year filter."
        )
        return

    # The denominator is the total over ALL organisations, not the top 10: summing
    # only the top 10 would make their shares add up to 100% by construction.
    total = known["compute_flops"].sum()
    rank = known.groupby("org")["compute_flops"].sum().sort_values(ascending=False)
    top = (rank.head(TOP_N) / total * 100).round(1)

    chart_df = top.rename("share").reset_index()
    chart_df["label"] = chart_df["share"].map(lambda p: f"{p:.1f}%")
    # A sort array puts its first entry at the top of a nominal y axis, so the
    # descending order is passed as is: biggest bar on top.
    order = chart_df["org"].tolist()

    bars = alt.Chart(chart_df).mark_bar(color=viz.TEAL_DARK, cornerRadiusEnd=4).encode(
        x=alt.X(
            "share:Q",
            title="Share of all known training compute (%)",
            scale=alt.Scale(domain=[0, float(top.max()) * 1.18]),
        ),
        y=alt.Y("org:N", title=f"Organisation (top {TOP_N} by share)", sort=order),
        tooltip=[
            alt.Tooltip("org:N", title="Organisation"),
            alt.Tooltip("share:Q", title="Share (%)", format=".1f"),
        ],
    )
    labels = bars.mark_text(align="left", dx=6, color=viz.TEAL_DARK).encode(
        text=alt.Text("label:N")
    )

    st.altair_chart((bars + labels).properties(height=360), width="stretch")

    rest = 100 - top.sum()
    others = rank.size - len(top)
    tail = (
        f" The remaining {rest:.0f}% is spread across {others} other organisations."
        if others > 0
        else ""
    )
    first, last = int(known["year"].min()), int(known["year"].max())
    st.caption(
        f"Years shown: {first}-{last}. The top {len(top)} organisations hold "
        f"{top.sum():.0f}% of all KNOWN training compute in those years.{tail} "
        "Recent years count the most, because models use far more compute now. "
        f"Only {len(known)} of {len(df)} models ({len(known) / len(df) * 100:.0f}%) "
        "have a known training compute, so the share is of known compute, not of "
        "all compute."
    )
