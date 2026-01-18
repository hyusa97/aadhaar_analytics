import os
import glob
import pandas as pd
from loguru import logger

RAW_DATA_DIR = r"C:\Users\hp\workspace\aadhaar_analytics\data\raw"
OUTPUT_TRAIN = "data/processed/master_train.csv"
OUTPUT_TEST = "data/processed/master_test.csv"
LOG_FILE = "logs/pipeline.log"

# configure logging
logger.add(LOG_FILE, rotation="10 MB")

def load_and_validate_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    if df.empty:
        logger.warning(f"Empty file skipped: {path}")
        return None

    df["source_file"] = os.path.basename(path)
    logger.info(f"Loaded {path} with {len(df)} rows")

    return df


def merge_monthly_csvs():
    csv_files = sorted(glob.glob(os.path.join(RAW_DATA_DIR, "*.csv")))
    print("Found CSVs:", csv_files)

    if len(csv_files) < 3:
        raise ValueError("Not enough CSV files for time-based split")

    dataframes = []

    for file in csv_files:
        df = load_and_validate_csv(file)
        if df is not None:
            dataframes.append(df)

    master_df = pd.concat(dataframes, ignore_index=True)
    logger.info(f"Merged dataset shape: {master_df.shape}")

    split_index = int(len(csv_files) * 0.8)
    train_files = csv_files[:split_index]
    test_files = csv_files[split_index:]

    train_df = master_df[master_df["source_file"].isin(
        [os.path.basename(f) for f in train_files]
    )]

    test_df = master_df[master_df["source_file"].isin(
        [os.path.basename(f) for f in test_files]
    )]

    train_df.to_csv(OUTPUT_TRAIN, index=False)
    test_df.to_csv(OUTPUT_TEST, index=False)

    logger.info(f"Train shape: {train_df.shape}")
    logger.info(f"Test shape: {test_df.shape}")


if __name__ == "__main__":
    merge_monthly_csvs()
