
# Data Dictionary

## 1. Project Dataset

The project uses AI model data to investigate the growth of artificial intelligence, organisation participation, training compute and open-weight model availability.

## 2. Processed Dataset: models.csv

**File location:** `data/processed/models.csv`



**Source:** Epoch AI (verify the exact dataset/release used).



**Source URL:** [INSERT THE DIRECT SOURCE DATASET URL]



**Licence:** [INSERT THE ACTUAL LICENCE OR REUSE CONDITIONS]



**Primary key:** The `model` column should be checked for uniqueness. If model names are not unique, document the actual record identifier or state that no unique primary key is available.

### Columns

| Column           | Description                                       | Units / Format     |
| ---------------- | ------------------------------------------------- | ------------------ |
| model            | Name of the AI model                              | Text               |
| org_all          | Organisations associated with the model           | Text               |
| org_count        | Number of organisations associated with the model | Count              |
| org              | Main organisation associated with the model       | Text               |
| org_type         | Classification of the organisation                | Category           |
| open_weights     | Whether the model has open weights                | Yes / No / Unknown |
| compute_flops    | Estimated training compute                        | FLOPs              |
| publication_date | Model publication date                            | YYYY-MM-DD         |

### Time Coverage

Start date: [INSERT EARLIEST PUBLICATION DATE]



End date: [INSERT LATEST PUBLICATION DATE]



Latest observation: [INSERT LATEST DATE PRESENT IN THE DATASET]

### Processing and Transformations

The processed dataset is used by the Streamlit application and its chart modules.



Documented processing includes:

- Cleaning and standardising organisation information.
- Using organisation information to support organisation-level analysis.
- Converting publication dates into years for yearly analysis.
- Grouping models by publication year.
- Counting newly appearing organisations based on their first recorded publication year.
- Calculating the percentage of models with open weights using records classified as Yes and No.
- Handling unknown or missing values appropriately in relevant calculations.

The exact processing steps should be checked against the scripts used to generate the processed dataset.

## 3. Processed Dataset: org_merges.csv

**File location:** `data/processed/org_merges.csv`



**Source:** Derived from the project's original AI model organisation data.



**Source URL:** [INSERT ORIGINAL SOURCE URL]



**Licence:** [INSERT ACTUAL LICENCE OR REUSE CONDITIONS]



**Purpose:** Stores organisation merging or standardisation information used during data preparation.

### Columns

[INSERT ALL ACTUAL COLUMN NAMES FROM org_merges.csv]

### Primary Key

[IDENTIFY THE UNIQUE ORGANISATION FIELD OR STATE THAT NO UNIQUE PRIMARY KEY EXISTS]

### Time Coverage

[STATE WHETHER THIS FILE IS TIME-BASED OR NOT APPLICABLE]

### Latest Observation

[STATE THE LATEST OBSERVATION IF APPLICABLE]

### Transformations

Document how organisation names were matched, merged or standardised. Include the script or process that generated this file.

## 4. Original Source Data

**Folder:** `data/raw/`



The raw folder contains the original source data used to prepare the processed datasets.



For each raw file, document:

- Filename
- Original publisher
- Direct source URL
- Licence or reuse conditions
- Retrieval date
- Columns and units
- Primary key
- Time coverage
- Latest observation
- Any processing applied to produce the processed dataset

## 5. Data Limitations

- Some models have unknown or missing training compute values.
- Organisation names and affiliations may require standardisation.
- Model counts do not necessarily represent market share.
- Training compute alone does not establish commercial dominance.
- Open-weight classification does not measure the full accessibility or commercial impact of a model.

can u help me with this?tell me what u need i will give u that then u can update it
