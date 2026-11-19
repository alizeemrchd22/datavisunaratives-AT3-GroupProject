# Data and AI Disclosure Statement

## 1. Data Sources

This project uses publicly available data about artificial intelligence models and their associated organisations.

The dataset includes information such as model names, organisation details, organisation types, open-weight classifications, estimated training compute and publication dates.

The data is used to investigate AI industry growth, organisation participation, computing power concentration and open-weight model development.

The original source files and processed datasets are stored in the repository's `data/` folder.

Further details about the datasets, their sources, licences, columns and transformations are provided in `DATA_DICTIONARY.md`.

## 2. Data Processing

The project uses processed data to prepare the visualisations displayed in the Streamlit application.

Data preparation includes organisation-name standardisation, publication-year grouping, counting newly appearing organisations and calculating open-weight model percentages.

Missing and unknown values are considered when performing calculations so that unavailable information is not treated as a confirmed measurement.

## 3. Use of Artificial Intelligence

AI tools, including ChatGPT and Claude, were used to assist group members with selected tasks during project development.

These tasks included coding assistance, debugging, chart development, integration and improving written explanations.

Group members reviewed the generated suggestions and remained responsible for the final code, calculations, visualisations and interpretations.

The specific AI-assisted tasks and their verification steps are documented in `AI_PROVENANCE.md`.

## 4. Limitations

The dataset provides information about AI models and their associated organisations, but it does not represent every aspect of the AI market.

Training compute and model counts cannot independently establish whether an organisation has a monopoly.

The dataset does not directly measure company revenue, sales, customer numbers, market share, commercial access or the full cost of entering the AI industry.

Some models have missing training compute information, and organisation affiliations may require interpretation or standardisation.

Open-weight classifications also do not necessarily represent the complete accessibility or commercial impact of a model.

## 5. Conclusion

The project explores how the answer to the research question can change depending on the measure used.

A small number of organisations may account for a substantial share of known training compute, while the number of organisations contributing AI models may also increase.

Therefore, the findings should be treated as indicators of possible industry concentration and changing participation, rather than proof of a monopoly.


