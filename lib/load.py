from pathlib import Path

import pandas as pd
import streamlit as st

DATA_FILE = Path(__file__).parent.parent / "data" / "processed" / "models.csv"

SOURCE_NAME = "Epoch AI, Notable AI Models"
SOURCE_URL = "https://epoch.ai/data/ai-models"
DOWNLOAD_DATE = "2026-10-21"

# The dataset goes back to 1950. The narrative starts in 2012, but the older rows
# stay in the file: Chart D needs them to know which organisations were already active.
START_YEAR = 2012


@st.cache_data
def load_models():
    df = pd.read_csv(DATA_FILE, parse_dates=["publication_date"])
    df["year"] = df["publication_date"].dt.year
    return df


def year_filter(df):
    """Filter B: the year range, in the sidebar. Shared by every page."""
    years = sorted(int(y) for y in df["year"].dropna().unique() if y >= START_YEAR)
    first, last = st.sidebar.slider(
        "Years shown",
        min_value=years[0],
        max_value=years[-1],
        value=(years[0], years[-1]),
        key="year_range",
    )
    return df[(df["year"] >= first) & (df["year"] <= last)]
