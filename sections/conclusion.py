
import streamlit as st

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

data["compute_flops"] = __import__("pandas").to_numeric(
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
