import pandas as pd
import numpy as np
from loguru import logger
from pathlib import Path

# =========================
# Paths & Logging
# =========================
INPUT_TRAIN = Path("data/processed/master_train_clean.csv")
INPUT_TEST = Path("data/processed/master_test_clean.csv")

OUTPUT_FILE = Path("data/processed/state_monthly.csv")

LOG_FILE = "logs/pipeline.log"
logger.add(LOG_FILE, rotation="10 MB")


# =========================
# Core Aggregation Logic
# =========================
def add_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df


def add_age_group(df: pd.DataFrame) -> pd.DataFrame:
    df["age_group"] = np.where(df["age"] < 17, "<17", ">=17")
    return df


def aggregate_core(df: pd.DataFrame) -> pd.DataFrame:
    base = (
        df.groupby(["state", "year", "month"], as_index=False)
        .agg(
            under_17=("age_5_17", "sum"),
            over_17=("age_18_greater", "sum"),
        )
    )

    under_17 = base[["state", "year", "month", "under_17"]].copy()
    under_17["age_group"] = "<17"
    under_17.rename(columns={"under_17": "total_activity"}, inplace=True)

    over_17 = base[["state", "year", "month", "over_17"]].copy()
    over_17["age_group"] = ">=17"
    over_17.rename(columns={"over_17": "total_activity"}, inplace=True)

    all_age = base.copy()
    all_age["total_activity"] = all_age["under_17"] + all_age["over_17"]
    all_age["age_group"] = "ALL"
    all_age = all_age[["state", "year", "month", "age_group", "total_activity"]]

    return pd.concat([under_17, over_17, all_age], ignore_index=True)



def add_pct_of_india(df: pd.DataFrame) -> pd.DataFrame:
    india_totals = (
        df.groupby(["year", "month", "age_group"], as_index=False)
        .agg(india_total=("total_activity", "sum"))
    )

    df = df.merge(
        india_totals,
        on=["year", "month", "age_group"],
        how="left"
    )

    df["pct_of_india"] = (df["total_activity"] / df["india_total"]) * 100
    df.drop(columns=["india_total"], inplace=True)

    return df



def add_mom_change_pct(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["state", "age_group", "year", "month"])

    df["mom_change_pct"] = (
        df.groupby(["state", "age_group"])["total_activity"]
          .pct_change() * 100
    )

    return df



# =========================
# Runner
# =========================
def run():
    logger.info("Loading master datasets")
    train_df = pd.read_csv(INPUT_TRAIN)
    test_df = pd.read_csv(INPUT_TEST)

    df = pd.concat([train_df, test_df], ignore_index=True)

    def clean_state_column(df: pd.DataFrame) -> pd.DataFrame:
    # drop null states
        df = df.dropna(subset=["state"])

    # force string
        df["state"] = df["state"].astype(str).str.strip()

    # remove numeric-only garbage (e.g. pincode leakage like "100000")
        df = df[~df["state"].str.match(r"^\d+$")]

    # remove very short junk like "0", "NA"
        df = df[df["state"].str.len() > 2]

        return df
    df = clean_state_column(df)



    logger.info("Adding time and age features")
    df = add_time_columns(df)
    #df = add_age_group(df)

    logger.info("Aggregating state-month data")
    agg = aggregate_core(df)

    

    logger.info("Computing pct_of_india")
    agg = add_pct_of_india(agg)

    logger.info("Computing MoM change")
    agg = add_mom_change_pct(agg)

    logger.info(f"Final state_monthly shape: {agg.shape}")
    agg.to_csv(OUTPUT_FILE, index=False)
    logger.info(f"Saved aggregated file to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
