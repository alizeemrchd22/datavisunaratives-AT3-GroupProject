
import altair as alt
import pandas as pd
import streamlit as st

from lib import viz


def render(df):
    st.subheader("Chart F — Compute share vs model share")

    top_n = st.selectbox(
        "Compare the top organisations",
        options=[3, 5, 10],
        index=1,
        format_func=lambda n: f"Top {n}"
    )

    data = df.copy()

    # Only models with known, positive training compute
    data["compute_flops"] = pd.to_numeric(
        data["compute_flops"], errors="coerce"
    )

    data = data[
        data["compute_flops"].notna()
        & (data["compute_flops"] > 0)
    ].copy()

    if data.empty:
        st.warning("No models with known compute for these years.")
        return

    # Rank organisations by total compute in selected period
    top_orgs = (
        data.groupby("org")["compute_flops"]
        .sum()
        .nlargest(top_n)
        .index
    )

    data["is_top"] = data["org"].isin(top_orgs)

    # Add columns for yearly totals
    data["top_compute"] = data["compute_flops"].where(
        data["is_top"], 0
    )
    data["top_model"] = data["is_top"].astype(int)

    yearly = (
        data.groupby("year", as_index=False)
        .agg(
            total_compute=("compute_flops", "sum"),
            top_compute=("top_compute", "sum"),
            total_models=("top_model", "size"),
            top_models=("top_model", "sum")
        )
    )

    yearly["Compute share"] = (
        yearly["top_compute"] / yearly["total_compute"] * 100
    )

    yearly["Model share"] = (
        yearly["top_models"] / yearly["total_models"] * 100
    )

    # Convert to long format for two Altair lines
    plot_data = yearly.melt(
        id_vars="year",
        value_vars=["Compute share", "Model share"],
        var_name="Measure",
        value_name="Share"
    )

    colors = alt.Scale(
        domain=["Compute share", "Model share"],
        range=[viz.TEAL_DARK, viz.CAMEL]
    )

    base = alt.Chart(plot_data).encode(
        x=alt.X("year:O", title="Publication year"),
        y=alt.Y(
            "Share:Q",
            title="Share (%)",
            scale=alt.Scale(domain=[0, 100])
        ),
        color=alt.Color("Measure:N", scale=colors),
        tooltip=[
            alt.Tooltip("year:O", title="Year"),
            "Measure:N",
            alt.Tooltip("Share:Q", format=".1f")
        ]
    )

    lines = base.mark_line(point=True, strokeWidth=3)

    # Data labels, without needing to hover
    compute_labels = (
        alt.Chart(plot_data[plot_data["Measure"] == "Compute share"])
        .mark_text(dy=-16, fontSize=11, color=viz.TEAL_DARK)
        .encode(
            x="year:O",
            y=alt.Y("Share:Q", scale=alt.Scale(domain=[0, 100])),
            text=alt.Text("Share:Q", format=".1f")
        )
    )

    model_labels = (
        alt.Chart(plot_data[plot_data["Measure"] == "Model share"])
        .mark_text(dy=18, fontSize=11, color=viz.CAMEL)
        .encode(
            x="year:O",
            y=alt.Y("Share:Q", scale=alt.Scale(domain=[0, 100])),
            text=alt.Text("Share:Q", format=".1f")
        )
    )

    st.altair_chart(
        lines + compute_labels + model_labels,
        use_container_width=True
    )

    # One evidence-based sentence using calculated results
    compute_pct = (
        data.loc[data["is_top"], "compute_flops"].sum()
        / data["compute_flops"].sum() * 100
    )

    models_pct = data["is_top"].mean() * 100

    st.write(
        f"Across the selected years, the top {top_n} organisations "
        f"produced {models_pct:.1f}% of models with known compute, "
        f"but accounted for {compute_pct:.1f}% of known training compute."
    )

    st.caption(
        "Organisations are ranked by total known training compute "
        "within the selected year range, then held fixed across its "
        "annual comparisons. Both measures use only models with "
        "known positive compute. Compute is attributed to the "
        "dataset's designated organisation, not necessarily its owner. "
        "2026 is an incomplete year."
    )
