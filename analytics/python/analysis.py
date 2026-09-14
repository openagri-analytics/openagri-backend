"""
OpenAgri Analytics — Analysis Pipeline
=======================================
Runs statistical analysis on the cleaned agricultural dataset.

Usage:
    python analysis.py
    python analysis.py --input ../../data/cleaned/agriculture_clean.csv
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def load(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    log.info("Loaded %d records for analysis.", len(df))
    return df


# ── Yield Analysis ─────────────────────────────────────────────────────────────

def yield_by_crop(df: pd.DataFrame) -> pd.DataFrame:
    """Average yield per crop, sorted descending."""
    result = (
        df.groupby("crop")["yield_tons"]
        .agg(average_yield=("mean"), total_records="count")
        .round({"average_yield": 2})
        .sort_values("average_yield", ascending=False)
        .reset_index()
    )
    return result


def yield_by_state(df: pd.DataFrame) -> pd.DataFrame:
    """Average yield per state."""
    return (
        df.groupby("state")["yield_tons"]
        .mean()
        .round(2)
        .sort_values(ascending=False)
        .reset_index(name="average_yield")
    )


def irrigation_impact(df: pd.DataFrame) -> pd.DataFrame:
    """Compare average yield between irrigated and non-irrigated farms."""
    return (
        df.groupby(["crop", "irrigation"])["yield_tons"]
        .mean()
        .round(2)
        .reset_index(name="average_yield")
        .sort_values(["crop", "irrigation"])
    )


# ── Profit Analysis ────────────────────────────────────────────────────────────

def profit_by_crop(df: pd.DataFrame) -> pd.DataFrame:
    """Total revenue, cost, and profit per crop."""
    return (
        df.groupby("crop")
        .agg(
            total_revenue=("revenue", "sum"),
            total_cost=("production_cost", "sum"),
            total_profit=("profit", "sum"),
            average_profit=("profit", "mean"),
        )
        .round(2)
        .sort_values("total_profit", ascending=False)
        .reset_index()
    )


def profit_by_state(df: pd.DataFrame) -> pd.DataFrame:
    """Total profit per state."""
    return (
        df.groupby("state")["profit"]
        .agg(total_profit="sum", average_profit="mean")
        .round(2)
        .sort_values("total_profit", ascending=False)
        .reset_index()
    )


def profit_margin_by_crop(df: pd.DataFrame) -> pd.DataFrame:
    """Profit margin (profit / revenue) per crop."""
    grp = df.groupby("crop").agg(
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
    )
    grp["profit_margin_pct"] = (
        grp["total_profit"] / grp["total_revenue"].replace(0, pd.NA) * 100
    ).round(1)
    return grp.sort_values("profit_margin_pct", ascending=False).reset_index()


# ── Input Factor Analysis ──────────────────────────────────────────────────────

def rainfall_vs_yield(df: pd.DataFrame) -> pd.DataFrame:
    """Average rainfall and yield per crop."""
    return (
        df.groupby("crop")
        .agg(avg_rainfall=("rainfall_mm", "mean"), avg_yield=("yield_tons", "mean"))
        .round(2)
        .sort_values("avg_yield", ascending=False)
        .reset_index()
    )


def fertilizer_impact(df: pd.DataFrame) -> pd.DataFrame:
    """Average yield per fertilizer type."""
    return (
        df.groupby("fertilizer_used")["yield_tons"]
        .mean()
        .round(2)
        .sort_values(ascending=False)
        .reset_index(name="average_yield")
    )


# ── Runner ─────────────────────────────────────────────────────────────────────

def run_all(path: str | Path) -> None:
    df = load(path)

    sections = [
        ("Yield by Crop",          yield_by_crop(df)),
        ("Yield by State",         yield_by_state(df)),
        ("Irrigation Impact",      irrigation_impact(df)),
        ("Profit by Crop",         profit_by_crop(df)),
        ("Profit by State",        profit_by_state(df)),
        ("Profit Margin by Crop",  profit_margin_by_crop(df)),
        ("Rainfall vs Yield",      rainfall_vs_yield(df)),
        ("Fertilizer Impact",      fertilizer_impact(df)),
    ]

    for title, result in sections:
        print(f"\n{'─' * 60}")
        print(f"  {title}")
        print(f"{'─' * 60}")
        print(result.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run agricultural data analysis")
    parser.add_argument(
        "--input",
        default="../../data/sample/agriculture.csv",
        help="Path to CSV file (raw or cleaned)",
    )
    args = parser.parse_args()
    run_all(args.input)


if __name__ == "__main__":
    main()
