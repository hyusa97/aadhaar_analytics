import pandas as pd
from loguru import logger

INPUT_TRAIN = r"C:\Users\hp\workspace\aadhaar_analytics\data\processed\state_monthly_train.csv" #"data/processed/state_monthly_train.csv"
INPUT_TEST = r"C:\Users\hp\workspace\aadhaar_analytics\data\processed\state_monthly_test.csv" #"data/processed/state_monthly_test.csv"

OUTPUT_TRAIN = "data/processed/state_monthly_features_train.csv"
OUTPUT_TEST = "data/processed/state_monthly_features_test.csv"

LOG_FILE = "logs/pipeline.log"
logger.add(LOG_FILE, rotation="10 MB")


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["year_month"] = pd.to_datetime(df["year_month"])
    df = df.sort_values(["state", "year_month"])

    # lag features
    df["lag_1"] = df.groupby("state")["total_records"].shift(1)
    df["lag_2"] = df.groupby("state")["total_records"].shift(2)

    # month-over-month growth
    df["mom_growth"] = (
        df["total_records"] - df["lag_1"]
    ) / df["lag_1"]

    # rolling features
    df["roll_mean_3"] = (
        df.groupby("state")["total_records"]
        .rolling(3)
        .mean()
        .reset_index(level=0, drop=True)
    )

    df["roll_std_3"] = (
        df.groupby("state")["total_records"]
        .rolling(3)
        .std()
        .reset_index(level=0, drop=True)
    )

    # national share
    df["national_total"] = df.groupby("year_month")["total_records"].transform("sum")
    df["state_share"] = df["total_records"] / df["national_total"]

    return df


def run():
    train_df = pd.read_csv(INPUT_TRAIN)
    test_df = pd.read_csv(INPUT_TEST)

    train_features = add_features(train_df)
    test_features = add_features(test_df)

    train_features.to_csv(OUTPUT_TRAIN, index=False)
    test_features.to_csv(OUTPUT_TEST, index=False)

    logger.info(f"Feature train shape: {train_features.shape}")
    logger.info(f"Feature test shape: {test_features.shape}")


if __name__ == "__main__":
    run()
