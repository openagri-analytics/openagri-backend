"""
OpenAgri Analytics — Data Cleaning Pipeline
============================================
Cleans raw agricultural CSV data and writes a validated output file.

Usage:
    python cleaning.py
    python cleaning.py --input ../../data/sample/agriculture.csv --output ../../data/cleaned/agriculture_clean.csv
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

VALID_CROPS = {
    "Maize", "Rice", "Cassava", "Yam", "Sorghum",
    "Soybean", "Groundnut", "Millet", "Cowpea", "Wheat",
}

REQUIRED_COLUMNS = [
    "farmer_id", "state", "crop", "farm_size_hectares",
    "yield_tons", "irrigation", "rainfall_mm",
    "production_cost", "revenue", "profit",
]


def load(path: str | Path) -> pd.DataFrame:
    """Load the raw CSV file."""
    df = pd.read_csv(path)
    log.info("Loaded %d records from %s", len(df), path)
    return df


def check_required_columns(df: pd.DataFrame) -> None:
    """Raise ValueError if required columns are missing."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def missing_value_report(df: pd.DataFrame) -> pd.Series:
    """Return percentage of missing values per column, sorted descending."""
    report = df.isnull().mean().mul(100).round(2).sort_values(ascending=False)
    report = report[report > 0]
    if report.empty:
        log.info("No missing values found.")
    else:
        log.info("Missing value report (%%%):\n%s", report.to_string())
    return report


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed:
        log.warning("Removed %d exact duplicate rows.", removed)
    return df


def drop_invalid_farm_size(df: pd.DataFrame) -> pd.DataFrame:
    """Drop records with non-positive farm size."""
    mask = df["farm_size_hectares"] > 0
    dropped = (~mask).sum()
    if dropped:
        log.warning("Dropped %d records with non-positive farm_size_hectares.", dropped)
    return df[mask].copy()


def drop_invalid_yield(df: pd.DataFrame) -> pd.DataFrame:
    """Drop records with negative yield (nulls are kept — use fill_missing for those)."""
    mask = df["yield_tons"].isna() | (df["yield_tons"] >= 0)
    dropped = (~mask).sum()
    if dropped:
        log.warning("Dropped %d records with negative yield_tons.", dropped)
    return df[mask].copy()


def validate_crop_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise crop names to title-case and flag unknowns."""
    df["crop"] = df["crop"].str.strip().str.title()
    unknown = df.loc[~df["crop"].isin(VALID_CROPS), "crop"].unique()
    if len(unknown):
        log.warning("Unknown crop names (kept but flagged): %s", list(unknown))
    return df


def fix_irrigation_column(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise irrigation to boolean."""
    if df["irrigation"].dtype == object:
        df["irrigation"] = df["irrigation"].str.strip().str.lower().map(
            {"yes": True, "no": False, "true": True, "false": False, "1": True, "0": False}
        )
    return df


def fill_missing_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing numeric values with column median (per crop)."""
    numeric_cols = ["yield_tons", "rainfall_mm", "market_price"]
    for col in numeric_cols:
        if col not in df.columns:
            continue
        missing_before = df[col].isna().sum()
        if missing_before:
            df[col] = df.groupby("crop")[col].transform(
                lambda x: x.fillna(x.median())
            )
            # Fall back to global median for crops with no non-null values
            df[col] = df[col].fillna(df[col].median())
            log.info("Filled %d missing '%s' values with crop/global median.", missing_before, col)
    return df


def recalculate_profit(df: pd.DataFrame) -> pd.DataFrame:
    """Recalculate profit = revenue - production_cost for consistency."""
    if {"revenue", "production_cost"}.issubset(df.columns):
        calculated = df["revenue"] - df["production_cost"]
        mismatch = (df["profit"] - calculated).abs() > 1
        if mismatch.sum():
            log.warning(
                "%d records have profit inconsistent with revenue - cost. Recalculating.",
                mismatch.sum()
            )
            df.loc[mismatch, "profit"] = calculated[mismatch]
    return df


def clean(path: str | Path) -> pd.DataFrame:
    """Run the full cleaning pipeline and return a clean DataFrame."""
    df = load(path)
    check_required_columns(df)
    missing_value_report(df)
    df = remove_duplicates(df)
    df = drop_invalid_farm_size(df)
    df = drop_invalid_yield(df)
    df = validate_crop_names(df)
    df = fix_irrigation_column(df)
    df = fill_missing_numeric(df)
    df = recalculate_profit(df)
    log.info("Cleaning complete. %d records remain.", len(df))
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean agricultural CSV data")
    parser.add_argument(
        "--input",
        default="../../data/sample/agriculture.csv",
        help="Path to raw input CSV",
    )
    parser.add_argument(
        "--output",
        default="../../data/cleaned/agriculture_clean.csv",
        help="Path to write cleaned CSV",
    )
    args = parser.parse_args()

    df = clean(args.input)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    log.info("Saved cleaned data to %s", out_path)


if __name__ == "__main__":
    main()
