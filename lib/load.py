from pathlib import Path

import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).parent.parent / "data" / "processed" / "models.csv"

SOURCE_NAME = "Epoch AI, Notable AI Models"
SOURCE_URL = "https://epoch.ai/data/ai-models"
DOWNLOAD_DATE = "2026-10-21"  # a mettre a jour quand on re-telecharge le CSV


@st.cache_data
def load_models():
    df = pd.read_csv(DATA_FILE, parse_dates=["publication_date"])
    df["year"] = df["publication_date"].dt.year
    return df


def year_filter(df):
    """Filtre B : la plage d'annees, dans la sidebar. Partage par toutes les pages."""
    years = sorted(df["year"].dropna().unique())
    first, last = st.sidebar.slider(
        "Years shown",
        min_value=int(years[0]),
        max_value=int(years[-1]),
        value=(int(years[0]), int(years[-1])),
        key="year_range",
    )
    return df[(df["year"] >= first) & (df["year"] <= last)]
