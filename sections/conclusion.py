
import streamlit as st
import pandas as pd

from lib import load, viz

df = load.load_models()

st.title("Our answer")

st.write(
    "The answer depends on what we count: a few organisations account "
    "for a large share of known training compute, while new organisations "
    "continue to enter the notable AI model landscape. These patterns "
    "are warning signs worth investigating, but they do not by themselves "
    "prove that the AI industry is a monopoly."
)


st.subheader("What the comparison tells us")

analysis = df[df["year"].between(2012, 2026)].copy()

analysis["compute_flops"] = pd.to_numeric(
    analysis["compute_flops"],
    errors="coerce"
)

# Same eligible records used in Chart F
analysis = analysis[
    analysis["compute_flops"].notna()
    & (analysis["compute_flops"] > 0)
].copy()

if not analysis.empty:

    # Rank organisations by total known compute
    top_five = (
        analysis.groupby("org")["compute_flops"]
        .sum()
        .nlargest(5)
        .index
    )

    top_models = analysis[
        analysis["org"].isin(top_five)
    ]

    # Compute share of top five organisations
    compute_share = (
        top_models["compute_flops"].sum()
        / analysis["compute_flops"].sum()
        * 100
    )

    # Model share of the same organisations
    model_share = (
        len(top_models) / len(analysis) * 100
    )

    difference = compute_share - model_share

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Training compute share",
        f"{compute_share:.1f}%"
    )

    col2.metric(
        "Model share",
        f"{model_share:.1f}%"
    )

    col3.metric(
        "Difference",
        f"{difference:.1f} pp"
    )

    st.write(
        f"Across 2012–2026, the five organisations with "
        f"the highest recorded training compute accounted "
        f"for {compute_share:.1f}% of known training compute, "
        f"while producing {model_share:.1f}% of models "
        f"with known positive compute."
    )

    st.write(
        "This difference suggests that training compute "
        "is more concentrated among these organisations "
        "than model production. Although other organisations "
        "participate in AI development, access to the "
        "computing resources needed for large-scale training "
        "may represent a barrier to competition."
    )

    st.info(
        "For an ACCC analyst, these results provide "
        "potential warning signs that justify further "
        "investigation. However, training compute is not "
        "equivalent to commercial market share, and these "
        "results do not establish a monopoly."
    )

    st.caption(
        "Calculated using models with known positive training "
        "compute from 2012–2026. Organisations are ranked "
        "over the full period. The 2026 data is incomplete."
    )

else:
    st.warning(
        "Insufficient training-compute data "
        "to calculate the comparison."
    )


st.subheader("What our data cannot show")

st.write(
    "Training compute is not the same as revenue, market share, or "
    "customer numbers. The Epoch AI dataset covers notable models, "
    "not every AI model developed, and training-compute values are "
    "missing for many models. Therefore, our results cannot establish "
    "whether a company has a monopoly or fully describe competition "
    "across the AI industry."
)
st.write(
    "Coverage of training-compute data varies considerably across "
    "years, reaching 79.0% in 2021 before falling to 37.4% in 2025. "
    "This missing information limits how confidently we can compare "
    "the computing power used to train models across the industry."
)
st.markdown("**How often is training compute known?**")

data = df.copy()

data["compute_flops"] = pd.to_numeric(
    data["compute_flops"], errors="coerce"
)

coverage = (
    data[data["year"].between(2012, 2025)]
    .groupby("year")
    .agg(
        total_models=("model", "size"),
        known_compute=("compute_flops", "count"),
    )
    .reset_index()
)

coverage["known_compute_pct"] = (
    coverage["known_compute"] / coverage["total_models"] * 100
)

coverage["Coverage (%)"] = coverage["known_compute_pct"].map(
    lambda value: f"{value:.1f}%"
)

st.dataframe(
    coverage[["year", "total_models", "known_compute", "Coverage (%)"]]
    .rename(
        columns={
            "year": "Year",
            "total_models": "Total models",
            "known_compute": "Models with known compute",
        }
    ),
    hide_index=True,
    use_container_width=True,
)

st.caption(
    "Coverage is the percentage of recorded models with a numeric "
    "training-compute value. Missing values do not mean a model used "
    "no compute. The 2026 data is excluded because the year is incomplete."
)

viz.footer()
