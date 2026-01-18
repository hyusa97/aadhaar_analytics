📌 Project Overview

This project performs large-scale analysis of Aadhaar service activity data with a focus on:

Structured data ingestion from monthly CSV dumps

Robust data cleaning and validation

State-level feature aggregation

Month-over-Month (MoM) anomaly detection

Interactive visualization using Streamlit (local execution)

The pipeline is designed to handle high-volume raw data offline, while the Streamlit application serves as a lightweight analytical interface over aggregated outputs.

🎯 Objectives

Build a reproducible data science pipeline for Aadhaar activity analysis

Detect unusual spikes and drops in state-level activity

Provide interpretable, non–black-box anomaly detection

Demonstrate end-to-end ownership: raw data → insights → visualization

📂 Project Structure
aadhaar_analytics/
│
├── app/
│   ├── app.py                     # Streamlit application
│   └── geo/
│       └── india_states.geojson   # India state boundaries (GeoJSON)
│
├── data/
│   ├── raw/                       # Original Aadhaar CSV datasets (NOT committed)
│   ├── interim/                   # Intermediate cleaned files
│   └── processed/                 # Final aggregated datasets
│       ├── state_monthly.csv
│       ├── state_monthly_anomalies.csv
│       ├── master_train.csv
│       ├── master_test.csv
│       └── other derived outputs
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_anomaly_detection.ipynb
│   ├── 05_forecasting.ipynb
│   └── validation.ipynb
│
├── src/
│   ├── ingestion/
│   │   └── merge_csvs.py
│   ├── cleaning/
│   │   └── clean_data.py
│   ├── features/
│   │   ├── aggregate_state_monthly.py
│   │   └── build_features.py
│   ├── models/
│   │   ├── anomaly.py
│   │   └── forecast.py
│   └── utils/
│       └── helpers.py
│
├── reports/
│   └── aadhaar_pulse_report.docx
│
├── requirements.txt
├── README.md
└── .gitignore

📊 Data Description
Raw Data (Required to Run Full Pipeline)

To reproduce the complete pipeline, you must provide 12 raw CSV files (monthly Aadhaar datasets).

These files are NOT included in the repository and must be placed manually in:

data/raw/

Expected file naming convention (example)
api_data_aadhaar_biometric_500000_1000000.csv
api_data_aadhaar_biometric_1000000_1500000.csv
api_data_aadhaar_biometric_1500000_1810168.csv

api_data_aadhaar_demographic_500000_1000000.csv
api_data_aadhaar_demographic_1000000_1500000.csv
api_data_aadhaar_demographic_1500000_2000000.csv
api_data_aadhaar_demographic_2000000_2071706.csv

api_data_aadhaar_enrolment_500000_1000000.csv
api_data_aadhaar_enrolment_1000000_1006029.csv


⚠️ Important

Filenames are expected as-is

Schema must be consistent across files

Large file sizes are expected and handled offline

🗺️ GeoJSON Requirement (Mandatory)

The Streamlit map requires an India state-level GeoJSON file.

Required file location
app/geo/india_states.geojson

Source (verified & stable)

Download from the following repository:

GeoJSON Source
https://github.com/geohacker/india

Direct file:

states_india.geojson


Rename it to:

india_states.geojson

GeoJSON property used

The application maps states using:

properties.NAME_1


Ensure your CSV state values align with these names.

🧠 Analytical Pipeline
Phase 1: Data Ingestion

Merge multiple monthly CSVs

Schema validation

Deduplication

Phase 2: Data Cleaning

Column normalization

Missing value handling

Date parsing

Phase 3: Feature Engineering

State-level monthly aggregation

Train/test splits

Metric consolidation

Phase 3.5: Visualization Layer

Choropleth map (state-wise)

Metric filters

Temporal slicing

Phase 4: Anomaly Detection

Month-over-Month absolute change

Month-over-Month percentage change

State-wise statistical thresholds

Flags: SPIKE, DROP, NORMAL

🚨 Anomaly Detection Logic (Summary)

For each state:

Compute MoM percentage change

Calculate state-specific mean and standard deviation

Flag anomalies using:

SPIKE: MoM > mean + 2 × std
DROP : MoM < mean - 2 × std


This approach ensures:

Interpretability

No black-box models

Report-friendly justification

🖥️ Streamlit Application (Local)
Purpose

Visual inspection

Insight communication

Demonstration of outputs

⚠️ Not designed for large-scale cloud execution

How to Run Locally
1️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Ensure required files exist

data/processed/state_monthly.csv

data/processed/state_monthly_anomalies.csv

app/geo/india_states.geojson

4️⃣ Run Streamlit
streamlit run app/app.py

🔒 Version Control & Reproducibility

Entire pipeline is version-controlled using Git

Raw Aadhaar data is intentionally excluded

Repository serves as:

methodological reference

reproducibility artifact

portfolio evidence

⚠️ Limitations

Raw datasets are processed offline

Streamlit app uses aggregated outputs only

Cloud deployment is intentionally avoided due to data scale

Forecasting module is experimental and not production-tuned

🔮 Future Enhancements

Cloud-based storage (Parquet + DuckDB)

Automated pipeline orchestration

Advanced anomaly explainability

Policy/event overlay on trends

📄 License & Usage

This project is intended for:

academic use

hackathons

portfolio demonstration

Raw Aadhaar data usage must comply with UIDAI data policies.