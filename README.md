# Aadhaar  Analytics

State-Level Aadhaar Activity Analysis, Anomaly Detection, and Visualization

---

## Project Overview

Aadhaar Pulse Analytics is an end-to-end data science project focused on analyzing Aadhaar service activity at a state level.  
The system is designed to handle large-scale raw data **offline**, while exposing insights through a **lightweight Streamlit-based analytical interface** over aggregated outputs.

The project emphasizes:
- reproducibility
- interpretability
- structured data engineering
- clear analytical reasoning

---

## Objectives

- Build a reproducible data science pipeline for Aadhaar activity analysis  
- Detect unusual spikes and drops in state-level activity  
- Provide interpretable, non–black-box anomaly detection  
- Demonstrate end-to-end ownership: raw data → insights → visualization  

---

## Key Features

- Robust data cleaning and validation  
- State-level feature aggregation  
- Month-over-Month (MoM) anomaly detection  
- Interactive visualization using Streamlit (local execution)  
- Clear separation between offline computation and visualization layer  

---

## Project Structure

```
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
```

---

## Data Description

### Raw Data (Required to Run Full Pipeline)

To reproduce the complete pipeline, **12 raw CSV files** (monthly Aadhaar datasets) are required.

These files are **not included in the repository** and must be placed manually in:

```
data/raw/
```

### Expected File Naming Convention (Example)

```
api_data_aadhaar_biometric_500000_1000000.csv
api_data_aadhaar_biometric_1000000_1500000.csv
api_data_aadhaar_biometric_1500000_1810168.csv

api_data_aadhaar_demographic_500000_1000000.csv
api_data_aadhaar_demographic_1000000_1500000.csv
api_data_aadhaar_demographic_1500000_2000000.csv
api_data_aadhaar_demographic_2000000_2071706.csv

api_data_aadhaar_enrolment_500000_1000000.csv
api_data_aadhaar_enrolment_1000000_1006029.csv
```

Raw data is intentionally excluded from version control due to size and sensitivity.

---

## GeoJSON Requirement (Mandatory)

The Streamlit visualization requires an India **state-level GeoJSON** file.

### File Location

```
app/geo/india_states.geojson
```

### Source Repository

Download the GeoJSON file from:

```
https://github.com/geohacker/india
```

File name in repository:
```
states_india.geojson
```

Rename the file to:
```
india_states.geojson
```

### GeoJSON Property Used

State mapping is performed using the following property:

```
properties.NAME_1
```

Ensure that state names in processed CSV files align exactly with this property.

---

## Analytical Pipeline

### Phase 1: Data Ingestion
- Merge multiple monthly CSV files
- Schema validation
- Deduplication

### Phase 2: Data Cleaning
- Column standardization
- Missing value handling
- Date parsing and validation

### Phase 3: Feature Engineering
- State-level monthly aggregation
- Metric consolidation
- Train/test dataset preparation

### Phase 3.5: Visualization Layer
- State-wise choropleth map
- Metric filtering
- Temporal slicing

### Phase 4: Anomaly Detection
- Month-over-Month absolute change
- Month-over-Month percentage change
- State-specific statistical baselines
- Anomaly flags: SPIKE, DROP, NORMAL

---

## Anomaly Detection Logic (Summary)

For each state:
1. Compute Month-over-Month percentage change
2. Calculate state-level mean and standard deviation
3. Apply statistical thresholds:

```
SPIKE: MoM > mean + 2 × std
DROP : MoM < mean - 2 × std
```

This approach ensures transparency and avoids black-box modeling.

---

## Streamlit Application (Local Execution)

The Streamlit app serves as a **local analytical interface** for exploring aggregated outputs.

It is intentionally not deployed to the cloud due to:
- dataset size
- memory constraints
- offline-first pipeline design

### Running Locally

1. Create a virtual environment:
```
python -m venv .venv
```

2. Activate the environment:
```
.venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Ensure required files exist:
```
data/processed/state_monthly.csv
data/processed/state_monthly_anomalies.csv
app/geo/india_states.geojson
```

5. Run Streamlit:
```
streamlit run app/app.py
```

---

## Version Control and Reproducibility

- The entire pipeline is maintained under Git version control
- Raw Aadhaar data is intentionally excluded
- The repository serves as:
  - methodological reference
  - reproducibility artifact
  - portfolio demonstration

---

## Limitations

- Raw datasets are processed offline
- Streamlit application operates on aggregated outputs only
- Cloud deployment is intentionally avoided
- Forecasting components are exploratory

---

## Future Enhancements

- Cloud-based storage using Parquet and DuckDB
- Automated pipeline orchestration
- Anomaly explainability layers
- Policy and event overlays on trends

---

## License and Usage

This project is intended for academic, hackathon, and portfolio use.

Usage of Aadhaar-related data must comply with applicable UIDAI data policies.
