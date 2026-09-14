"""
OpenAgri Analytics — Visualization Pipeline
============================================
Generates charts from agricultural data and saves them as PNG files.

Usage:
    python visualization.py
    python visualization.py --input ../../data/sample/agriculture.csv --output ../../data/charts/
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — no display required

import matplotlib.pyplot as plt
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# Consistent colour palette for crops
CROP_COLOURS = [
    "#2e7d32", "#43a047", "#66bb6a", "#a5d6a7",
    "#1b5e20", "#388e3c", "#81c784", "#c8e6c9",
]


def _savefig(fig: plt.Figure, output_dir: Path, name: str) -> None:
    path = output_dir / f"{name}.png"
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    log.info("Saved chart: %s", path)


def plot_yield_by_crop(df: pd.DataFrame, output_dir: Path) -> None:
    """Horizontal bar chart — average yield by crop."""
    data = (
        df.groupby("crop")["yield_tons"]
        .mean()
        .sort_values()
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(data.index, data.values, color=CROP_COLOURS[: len(data)])
    ax.set_xlabel("Average Yield (tons)")
    ax.set_title("Average Crop Yield", fontweight="bold")
    ax.bar_label(bars, fmt="%.2f", padding=4)
    ax.set_xlim(0, data.values.max() * 1.15)
    fig.tight_layout()
    _savefig(fig, output_dir, "yield_by_crop")


def plot_profit_by_crop(df: pd.DataFrame, output_dir: Path) -> None:
    """Horizontal bar chart — total profit by crop."""
    data = (
        df.groupby("crop")["profit"]
        .sum()
        .sort_values()
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(data.index, data.values / 1_000, color=CROP_COLOURS[: len(data)])
    ax.set_xlabel("Total Profit (₦ thousands)")
    ax.set_title("Total Profit by Crop", fontweight="bold")
    ax.bar_label(bars, fmt="%.0fk", padding=4)
    ax.set_xlim(0, data.values.max() / 1_000 * 1.15)
    fig.tight_layout()
    _savefig(fig, output_dir, "profit_by_crop")


def plot_revenue_by_state(df: pd.DataFrame, output_dir: Path) -> None:
    """Horizontal bar chart — total revenue by state."""
    data = (
        df.groupby("state")["revenue"]
        .sum()
        .sort_values()
    )
    fig, ax = plt.subplots(figsize=(9, max(5, len(data) * 0.5)))
    ax.barh(data.index, data.values / 1_000, color="#43a047")
    ax.set_xlabel("Total Revenue (₦ thousands)")
    ax.set_title("Total Revenue by State", fontweight="bold")
    ax.set_xlim(0, data.values.max() / 1_000 * 1.15)
    fig.tight_layout()
    _savefig(fig, output_dir, "revenue_by_state")


def plot_rainfall_vs_yield(df: pd.DataFrame, output_dir: Path) -> None:
    """Scatter plot — rainfall vs yield, coloured by crop."""
    crops = df["crop"].unique()
    fig, ax = plt.subplots(figsize=(9, 6))
    for i, crop in enumerate(sorted(crops)):
        subset = df[df["crop"] == crop]
        ax.scatter(
            subset["rainfall_mm"],
            subset["yield_tons"],
            label=crop,
            alpha=0.75,
            color=CROP_COLOURS[i % len(CROP_COLOURS)],
            s=60,
        )
    ax.set_xlabel("Rainfall (mm)")
    ax.set_ylabel("Yield (tons)")
    ax.set_title("Rainfall vs Yield by Crop", fontweight="bold")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    _savefig(fig, output_dir, "rainfall_vs_yield")


def plot_irrigation_impact(df: pd.DataFrame, output_dir: Path) -> None:
    """Grouped bar chart — irrigated vs non-irrigated average yield per crop."""
    pivot = (
        df.groupby(["crop", "irrigation"])["yield_tons"]
        .mean()
        .unstack("irrigation")
        .rename(columns={True: "Irrigated", False: "Not Irrigated"})
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(kind="bar", ax=ax, color=["#2e7d32", "#a5d6a7"], edgecolor="white")
    ax.set_xlabel("Crop")
    ax.set_ylabel("Average Yield (tons)")
    ax.set_title("Irrigation Impact on Yield by Crop", fontweight="bold")
    ax.legend(title="Irrigation")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    _savefig(fig, output_dir, "irrigation_impact")


def run_all(input_path: str | Path, output_dir: str | Path) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    log.info("Loaded %d records for visualization.", len(df))

    # Normalise boolean column
    if df["irrigation"].dtype == object:
        df["irrigation"] = df["irrigation"].str.strip().str.lower().map(
            {"yes": True, "no": False}
        )

    plot_yield_by_crop(df, out)
    plot_profit_by_crop(df, out)
    plot_revenue_by_state(df, out)
    plot_rainfall_vs_yield(df, out)
    plot_irrigation_impact(df, out)

    log.info("All charts saved to %s", out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate agricultural data charts")
    parser.add_argument(
        "--input",
        default="../../data/sample/agriculture.csv",
        help="Path to CSV file",
    )
    parser.add_argument(
        "--output",
        default="../../data/charts",
        help="Output directory for PNG charts",
    )
    args = parser.parse_args()
    run_all(args.input, args.output)


if __name__ == "__main__":
    main()
