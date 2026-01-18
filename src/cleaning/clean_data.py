import pandas as pd
from loguru import logger

TRAIN_PATH = r"C:\Users\hp\workspace\aadhaar_analytics\data\processed\master_train.csv"#"data/processed/master_train.csv"
TEST_PATH = r"C:\Users\hp\workspace\aadhaar_analytics\data\processed\master_test.csv"#"data/processed/master_test.csv"

CLEAN_TRAIN_PATH = "data/processed/master_train_clean.csv"
CLEAN_TEST_PATH = "data/processed/master_test_clean.csv"

LOG_FILE = "logs/pipeline.log"
logger.add(LOG_FILE, rotation="10 MB")


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    initial_shape = df.shape

    # standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # drop fully empty rows
    df.dropna(how="all", inplace=True)

    # remove duplicates
    df.drop_duplicates(inplace=True)

    logger.info(f"Cleaned from {initial_shape} to {df.shape}")

    return df


def validate_critical_columns(df: pd.DataFrame, cols: list):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing critical columns: {missing}")


def run_cleaning():
    train_df = pd.read_csv(TRAIN_PATH)
    test_df = pd.read_csv(TEST_PATH)

    critical_cols = ["state", "date"]
    validate_critical_columns(train_df, critical_cols)
    validate_critical_columns(test_df, critical_cols)

    train_df = basic_cleaning(train_df)
    test_df = basic_cleaning(test_df)

    # parse date column
    train_df["date"] = pd.to_datetime(train_df["date"], errors="coerce")
    test_df["date"] = pd.to_datetime(test_df["date"], errors="coerce")

    # drop invalid dates
    train_df = train_df.dropna(subset=["date"])
    test_df = test_df.dropna(subset=["date"])

    train_df.to_csv(CLEAN_TRAIN_PATH, index=False)
    test_df.to_csv(CLEAN_TEST_PATH, index=False)

    logger.info("Cleaning completed successfully")


if __name__ == "__main__":
    run_cleaning()
