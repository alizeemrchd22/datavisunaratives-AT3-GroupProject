"""Build data/processed/models.csv from the raw Epoch CSV.

Run from the repo root:  python3 scripts/build_processed.py
"""

import pandas as pd

RAW = "data/raw/epoch_all_ai_models_2026-10-21.csv"
OUT = "data/processed/models.csv"
MERGE_TABLE = "data/processed/org_merges.csv"

# Student D: extend this table. Left side is merged into the right side.
ORG_MERGES = {
    "Google DeepMind": "Google",
    "DeepMind": "Google",
    "Google Research": "Google",
    "Google Brain": "Google",
    "Meta AI": "Meta",
    "Facebook AI Research": "Meta",
    "Microsoft Research": "Microsoft",
}


def org_type(value):
    """Epoch lists one category per contributing organisation, e.g. 'Industry,Academia'."""
    if pd.isna(value):
        return "other"
    parts = {p.strip() for p in str(value).split(",")}
    industry = "Industry" in parts
    academia = "Academia" in parts
    if industry and academia:
        return "industry-academia"
    if industry:
        return "industry"
    if academia:
        return "academia"
    return "other"


raw = pd.read_csv(RAW)

# Keep only notable models: compute coverage goes from 39% to 51%.
notable = raw[raw["Notability criteria"].notna()].copy()

df = pd.DataFrame({
    "model": notable["Model"],
    # Epoch lists every contributing organisation, comma separated (28% of notable
    # models have more than one). We attribute the model to the first one listed,
    # so compute is never counted twice, and keep the full list for the record.
    "org_all": notable["Organization"].fillna("Unknown"),
    "org_count": notable["Organization"].fillna("Unknown").str.count(",") + 1,
    "org": notable["Organization"].fillna("Unknown").str.split(",").str[0].str.strip().replace(ORG_MERGES),
    "org_type": notable["Organization categorization"].apply(org_type),
    "open_weights": notable["Open model weights?"].map({"Yes": "yes", "No": "no"}).fillna("unknown"),
    "compute_flops": pd.to_numeric(notable["Training compute (FLOP)"], errors="coerce"),
    "publication_date": pd.to_datetime(notable["Publication date"], errors="coerce"),
})

df = df[df["publication_date"].notna()]
df = df.drop_duplicates(subset=["model", "org_all", "publication_date"])
df = df.sort_values("publication_date")

df.to_csv(OUT, index=False)

merges = pd.DataFrame(sorted(ORG_MERGES.items()), columns=["raw_name", "merged_into"])
merges.to_csv(MERGE_TABLE, index=False)

year = df["publication_date"].dt.year
print("rows:", len(df))
print("organisations:", df["org"].nunique())
print("years:", int(year.min()), "-", int(year.max()))
print("training compute known:", round(df["compute_flops"].notna().mean() * 100, 1), "%")
print()
print(df["org_type"].value_counts())
print()
print(df["open_weights"].value_counts())
print()
print(df["org"].value_counts().head(10))
