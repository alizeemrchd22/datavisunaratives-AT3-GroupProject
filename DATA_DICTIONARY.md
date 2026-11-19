# Data Dictionary

The app answers one question: are a few companies monopolising AI, or is the
field opening up? It reads a single processed file built from one Epoch AI
download. This document covers every dataset in `data/`: the raw source sample
and the two processed files.

| File | Role | Rows | Read by the app? |
| ---- | ---- | ---- | ---------------- |
| `data/raw/epoch_all_ai_models_2026-10-21.csv` | Source sample (frozen download) | 3,628 | No, input to the build script |
| `data/processed/models.csv` | Processed, one row per notable model | 1,104 | Yes, every chart |
| `data/processed/org_merges.csv` | Processed lookup, organisation name merges | 7 | No, written by the build script as a record of the merges |

All processed files are produced by one script:

    python3 scripts/build_processed.py

Run from the repo root. Re-running it on the raw file reproduces both processed
files byte for byte (checked on 20 Nov 2026: `git status` shows no change after
the run).

---

## 1. Source sample: epoch_all_ai_models_2026-10-21.csv

**File location:** `data/raw/epoch_all_ai_models_2026-10-21.csv`

**Source:** Epoch AI, "Data on AI Models" (the "All AI models" CSV export).

**Source URL:** https://epoch.ai/data/ai-models

**Licence:** Creative Commons Attribution (CC BY). Reuse is allowed
with credit to Epoch AI.

**Retrieved:** 21 October 2026. The file is kept unchanged as downloaded; the
date in the filename is the download date.

**Rows / columns:** 3,628 rows, 57 columns.

**Primary key:** `Model`. Checked: all 3,628 values are unique.

**Time coverage:** `Publication date` runs from 1950-07-02 to 2026-10-17
(12 rows have no publication date).

**Latest observation:** latest publication date 2026-10-17; latest record edit
(`Last modified`) 2026-10-19 22:22 UTC.

### Columns used by the build script

The file has 57 columns. Only these seven are read; the others are kept so the
sample stays identical to the download.

| Column | Description | Units / format |
| ------ | ----------- | -------------- |
| Model | Model name | Text |
| Organization | Every contributing organisation, comma separated | Text |
| Organization categorization | One category per contributing organisation, comma separated: Industry, Academia, Research collective, Government | Text |
| Notability criteria | Why Epoch counts the model as notable (e.g. "Highly cited", "SOTA improvement"); empty if not notable | Text |
| Open model weights? | Whether the weights are publicly released | Yes / No / empty |
| Training compute (FLOP) | Estimated total training compute | FLOP (floating-point operations), float |
| Publication date | Date the model was published or announced | YYYY-MM-DD |

Other columns (parameters, dataset size, hardware, cost, country, etc.) are
described on the Epoch AI page above and are not used by the app.

---

## 2. Processed: models.csv

**File location:** `data/processed/models.csv`

**Produced by:** `scripts/build_processed.py` from the source sample above.

**Source / URL / licence:** as the source sample (Epoch AI,
https://epoch.ai/data/ai-models, CC BY).

**Rows / columns:** 1,104 rows, 8 columns. One row per notable model.

**Primary key:** `model`. Checked: all 1,104 values are unique.

**Time coverage:** `publication_date` from 1950-07-02 to 2026-09-30. The app's
charts show 2012 onwards (954 rows); the older rows stay in the file because
Chart D needs them to know which organisations were already active before 2012.

**Latest observation:** 2026-09-30 (latest publication date of a notable model).

### Columns

| Column | Description | Units / format | Derived from |
| ------ | ----------- | -------------- | ------------ |
| model | Model name | Text | `Model` |
| org_all | Full list of contributing organisations | Text, comma separated; "Unknown" if empty | `Organization` |
| org_count | Number of contributing organisations | Count (integer, 1 to 37) | commas in `Organization` + 1 |
| org | Organisation the model is attributed to: the first one listed, after name merges | Text (240 distinct values) | first entry of `Organization`, then `org_merges.csv` |
| org_type | Type of organisation behind the model | Category: industry, academia, industry-academia, other | `Organization categorization` |
| open_weights | Whether the model weights are public | Category: yes, no, unknown | `Open model weights?` |
| compute_flops | Estimated training compute | FLOP, float; empty if Epoch has no estimate (known for 51.2% of rows; range 4.0e1 to 9.4e26) | `Training compute (FLOP)` |
| publication_date | Publication date | YYYY-MM-DD | `Publication date` |

Value counts, for checking against the app:

- `org_type`: industry 635, academia 258, industry-academia 182, other 29
- `open_weights`: no 492, yes 356, unknown 256
- `org` with "Unknown": 18 rows

### Transform (raw to models.csv)

In order, as coded in `scripts/build_processed.py`:

1. Keep only notable models: rows where `Notability criteria` is filled
   (3,628 to 1,104 rows). This raises training compute coverage from 39% to 51%.
2. `org_all`: copy `Organization`, filling empty values with "Unknown".
3. `org_count`: number of commas in `org_all` plus one. 28% of notable models
   have more than one organisation.
4. `org`: take the first organisation in the list and strip spaces, then
   replace name variants using the merge table (section 3). Each model goes to
   one organisation, so compute is never counted twice.
5. `org_type`: split `Organization categorization` on commas. Industry and
   Academia both present gives industry-academia; only Industry gives industry;
   only Academia gives academia; anything else (research collective,
   government, empty) gives other.
6. `open_weights`: map Yes to yes, No to no, empty to unknown.
7. `compute_flops`: convert `Training compute (FLOP)` to a number; anything
   that does not parse becomes empty.
8. `publication_date`: parse as a date; drop rows with no valid date (0 notable
   rows dropped in this download).
9. Drop exact duplicates on model, org_all and publication_date (0 dropped).
10. Sort by publication_date and write the CSV.

The app then adds a `year` column at load time (`lib/load.py`,
year of `publication_date`). That column is not stored in the file.

---

## 3. Processed: org_merges.csv

**File location:** `data/processed/org_merges.csv`

**Produced by:** `scripts/build_processed.py`, written from the `ORG_MERGES`
dictionary in that script. It records which organisation names were merged,
so anyone can see the change without reading the code.

**Source / URL / licence:** names come from the `Organization` column of the
Epoch AI source sample (https://epoch.ai/data/ai-models, CC BY). The
mapping itself is the group's own decision.

**Rows / columns:** 7 rows, 2 columns.

**Primary key:** `raw_name`. Each name variant is merged into exactly one target.

**Time coverage:** not applicable. This is a lookup table, not time series data.

**Latest observation:** not applicable. Generated with models.csv from the
21 October 2026 download.

### Columns

| Column | Description | Units / format |
| ------ | ----------- | -------------- |
| raw_name | Organisation name as it appears in Epoch's `Organization` column | Text |
| merged_into | Name used in `models.csv` `org` | Text |

### Contents

| raw_name | merged_into |
| -------- | ----------- |
| DeepMind | Google |
| Facebook AI Research | Meta |
| Google Brain | Google |
| Google DeepMind | Google |
| Google Research | Google |
| Meta AI | Meta |
| Microsoft Research | Microsoft |

### Transform

The script turns the `ORG_MERGES` dictionary into a two-column table, sorts it
by `raw_name` and writes the CSV. Names are matched exactly (whole string,
case sensitive) against the first organisation listed for each model. The
merges group labs that belong to the same parent company, because the question
is about concentration between companies, not between research teams.

---

## 4. Data limitations

- Training compute is missing for about half of notable models (51.2% known),
  and coverage falls in recent years as labs stop publishing details. Compute
  shares are shares of known compute only.
- Epoch decides which models are "notable". Models outside that list, including
  many commercial models, are not counted.
- A model with several organisations is attributed to the first one listed.
  This can understate the role of partners.
- Model counts are not market share, and training compute alone does not show
  commercial dominance (revenue, users or prices are not in the data).
- `open_weights` describes the weights only, not licence terms or how widely a
  model is actually used.
- Epoch edits records over time. The numbers here match the frozen
  21 October 2026 download, not the live page.
