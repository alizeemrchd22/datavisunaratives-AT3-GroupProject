# Are a few companies monopolising AI, or is the field opening up?

An interactive data narrative built with Streamlit, using Epoch AI's dataset of
notable AI models.

## The question

Are a few companies monopolising AI, or is the field opening up?

The same data answers this two ways. Counted by training compute, a handful of
organisations hold most of it. Counted by models and organisations, hundreds of
players are active. The answer depends on what you count.

## The persona

A competition analyst at the ACCC, Australia's competition regulator. Her
decision: whether to recommend a deeper investigation into the AI industry. She
does not need proof of a monopoly. She needs warning signs that would justify
opening one.

## User stories

- As a competition analyst, I want to see which organisations hold most of the
  training compute, so that I can spot organisations that may be too dominant.
- As a competition analyst, I want to see whether new organisations keep
  arriving and how much compute it takes to compete, so that I can judge whether
  the market is getting harder to enter.
- As a competition analyst, I want to compare concentration by compute against
  concentration by model count, so that I can decide whether an investigation is
  warranted.

## Data

Source: Epoch AI, "Notable AI Models" - https://epoch.ai/data/ai-models
Licence: Creative Commons Attribution (CC BY).
Downloaded 21 October 2026, frozen at data/raw/epoch_all_ai_models_2026-10-21.csv

The script scripts/build_processed.py turns the raw file into
data/processed/models.csv, which every chart reads. The transforms:

- keep only notable models (the "Notability criteria" field is filled)
- attribute each model to the first organisation listed, keeping the full list
  in org_all; the organisation type still uses every contributor
- merge organisation name variants using data/processed/org_merges.csv
- map "Open model weights?" to open_weights: yes / no / unknown
- drop rows with no publication date, and exact duplicates

Training compute is known for 51% of notable models, and coverage falls in
recent years. Every chart that uses compute says so.

## Running it

    pip install -r requirements.txt
    streamlit run app.py

## Repository layout

- app.py - the five-page narrative
- lib/load.py - data loading and the shared year filter
- lib/viz.py - the group palette and shared helpers
- charts/ - one chart per file, each exposing render(df)
- sections/ - the five pages
- scripts/build_processed.py - raw data to processed data
