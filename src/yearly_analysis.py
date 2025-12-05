"""
Yearly Analysis and Visualization Module
=========================================

This module performs comprehensive yearly analysis of weather data,
including:
- Statistical summary of yearly maximum temperatures
- Trend analysis using linear regression
- Anomaly detection using statistical thresholds
- Professional visualizations

The analysis helps identify:
- Long-term climate trends (warming/cooling)
- Unusually hot or cold years (anomalies)
- Overall climate patterns for the region

Input: yearly_max_temp.csv
Output: Various visualizations in output/ directory

Usage:
    python yearly_analysis.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator

from config import (
    ANOMALY_THRESHOLD_STD,
    COLOR_ACCENT,
    COLOR_PRIMARY,
    FIGURE_DPI,
    FIGURE_SIZE_STANDARD,
    FIGURE_SIZE_WIDE,
    LOCATION_NAME,
    OUTPUT_DIR,
    YEARLY_MAX_TEMP_FILE,
)


def load_yearly_data() -> pd.DataFrame:
    """
    Load and prepare yearly maximum temperature data.

    Returns:
        DataFrame with year and max_temperature columns
    """
    df = pd.read_csv(YEARLY_MAX_TEMP_FILE)
    df["year"] = df["year"].astype(int)
    df["max_temperature"] = df["max_temperature"].astype(float)
    df = df.sort_values("year").reset_index(drop=True)
    return df


def compute_statistics(df: pd.DataFrame) -> dict:
    """
    Compute statistical summary of yearly temperatures.

    Args:
        df: DataFrame with yearly temperature data

    Returns:
        Dictionary containing various statistics
    """
    temps = df["max_temperature"].values
    years = df["year"].values

    # Basic statistics
    stats = {
        "count": len(df),
        "mean": temps.mean(),
        "std": temps.std(),
        "min": temps.min(),
        "max": temps.max(),
        "range": temps.max() - temps.min(),
        "year_start": years.min(),
        "year_end": years.max(),
    }

    # Find extreme years
    stats["hottest_year"] = df.loc[df["max_temperature"].idxmax(), "year"]
    stats["coolest_year"] = df.loc[df["max_temperature"].idxmin(), "year"]

    # Trend analysis (linear regression)
    slope, intercept = np.polyfit(years, temps, 1)
    stats["trend_slope"] = slope
    stats["trend_intercept"] = intercept
    stats["trend_per_decade"] = slope * 10

    # Anomaly detection
    threshold = stats["mean"] + ANOMALY_THRESHOLD_STD * stats["std"]
    df["is_anomaly"] = df["max_temperature"] > threshold
    stats["anomaly_threshold"] = threshold
    stats["anomaly_count"] = df["is_anomaly"].sum()

    return stats, df


def print_analysis_report(stats: dict, df: pd.DataFrame) -> str:
    """
    Print and return a formatted analysis report.

    Args:
        stats: Dictionary of computed statistics
        df: DataFrame with anomaly flags

    Returns:
        Formatted report string
    """
    report = []
    report.append("=" * 70)
    report.append(f"YEARLY TEMPERATURE ANALYSIS - {LOCATION_NAME}")
    report.append("=" * 70)

    report.append("\n📊 STATISTICAL SUMMARY")
    report.append("-" * 70)
    report.append(
        f"  Analysis Period: {stats['year_start']} - {stats['year_end']} ({stats['count']} years)"
    )
    report.append(f"  Mean Maximum Temperature: {stats['mean']:.2f}°C")
    report.append(f"  Standard Deviation: {stats['std']:.2f}°C")
    report.append(
        f"  Temperature Range: {stats['min']:.1f}°C - {stats['max']:.1f}°C (Δ{stats['range']:.1f}°C)"
    )

    report.append("\n🌡️ EXTREME YEARS")
    report.append("-" * 70)
    report.append(f"  🔥 Hottest Year: {stats['hottest_year']} ({stats['max']:.1f}°C)")
    report.append(f"  ❄️  Coolest Year: {stats['coolest_year']} ({stats['min']:.1f}°C)")

    report.append("\n📈 TREND ANALYSIS")
    report.append("-" * 70)
    report.append(f"  Slope: {stats['trend_slope']:.4f}°C per year")
    report.append(f"  Change per Decade: {stats['trend_per_decade']:+.2f}°C")

    if stats["trend_slope"] > 0.01:
        report.append("  📍 Interpretation: Clear WARMING trend detected")
    elif stats["trend_slope"] < -0.01:
        report.append("  📍 Interpretation: Clear COOLING trend detected")
    else:
        report.append("  📍 Interpretation: No significant trend")

    report.append("\n⚠️ ANOMALY DETECTION")
    report.append("-" * 70)
    report.append(f"  Method: Values > mean + {ANOMALY_THRESHOLD_STD}σ")
    report.append(f"  Threshold: {stats['anomaly_threshold']:.2f}°C")
    report.append(f"  Anomalies Found: {stats['anomaly_count']}")

    if stats["anomaly_count"] > 0:
        anomalies = df[df["is_anomaly"]]
        for _, row in anomalies.iterrows():
            report.append(f"    • {int(row['year'])}: {row['max_temperature']:.1f}°C")
    else:
        report.append("    No significant anomalies detected")

    report.append("=" * 70)

    report_text = "\n".join(report)
    print(report_text)
    return report_text


def plot_yearly_trend(df: pd.DataFrame, stats: dict) -> str:
    """
    Create a comprehensive yearly trend visualization.

    Args:
        df: DataFrame with yearly data and anomaly flags
        stats: Dictionary of computed statistics

    Returns:
        Path to saved figure
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

    years = df["year"].values
    temps = df["max_temperature"].values

    # Calculate trend line
    trend_line = stats["trend_slope"] * years + stats["trend_intercept"]

    # Plot main temperature line
    ax.plot(
        years,
        temps,
        marker="o",
        markersize=8,
        linewidth=2,
        color=COLOR_PRIMARY,
        label="Yearly Max Temperature",
        zorder=3,
    )

    # Plot trend line
    ax.plot(
        years,
        trend_line,
        linestyle="--",
        linewidth=2.5,
        color="#2ecc71",
        label=f'Trend ({stats["trend_per_decade"]:+.2f}°C/decade)',
        zorder=2,
    )

    # Highlight anomalies
    anomalies = df[df["is_anomaly"]]
    if not anomalies.empty:
        ax.scatter(
            anomalies["year"],
            anomalies["max_temperature"],
            s=200,
            c=COLOR_ACCENT,
            marker="*",
            edgecolors="black",
            linewidth=1.5,
            label="Anomaly (Unusually Hot)",
            zorder=4,
        )

    # Add mean line
    ax.axhline(
        y=stats["mean"],
        color="gray",
        linestyle=":",
        alpha=0.7,
        label=f'Mean ({stats["mean"]:.1f}°C)',
    )

    # Add anomaly threshold line
    ax.axhline(
        y=stats["anomaly_threshold"],
        color=COLOR_ACCENT,
        linestyle=":",
        alpha=0.5,
        label=f'Anomaly Threshold ({stats["anomaly_threshold"]:.1f}°C)',
    )

    # Styling
    ax.set_xlabel("Year", fontsize=12, fontweight="bold")
    ax.set_ylabel("Maximum Temperature (°C)", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Yearly Maximum Temperature Analysis - {LOCATION_NAME}\n(2000-2024)",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )

    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=12))
    ax.grid(True, alpha=0.3, linestyle="-")
    ax.legend(loc="upper left", framealpha=0.95, fontsize=10)

    # Add annotation for hottest year
    hottest_idx = df["max_temperature"].idxmax()
    ax.annotate(
        f'Hottest: {int(df.loc[hottest_idx, "year"])}\n{df.loc[hottest_idx, "max_temperature"]:.1f}°C',
        xy=(df.loc[hottest_idx, "year"], df.loc[hottest_idx, "max_temperature"]),
        xytext=(10, 10),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2"),
    )

    plt.tight_layout()

    output_path = OUTPUT_DIR / "01_yearly_temperature_trend.png"
    plt.savefig(
        output_path,
        dpi=FIGURE_DPI,
        bbox_inches="tight",
        facecolor="white",
        edgecolor="none",
    )
    plt.close()

    print(f"  ✓ Saved: {output_path}")
    return str(output_path)


def plot_decade_comparison(df: pd.DataFrame) -> str:
    """
    Create a decade-by-decade comparison visualization.

    Args:
        df: DataFrame with yearly data

    Returns:
        Path to saved figure
    """
    df = df.copy()
    df["decade"] = (df["year"] // 10) * 10
    df["decade_label"] = df["decade"].astype(str) + "s"

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_STANDARD)

    decade_stats = df.groupby("decade_label")["max_temperature"].agg(
        ["mean", "min", "max", "std"]
    )
    decade_stats = decade_stats.reset_index()

    x = range(len(decade_stats))
    colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(decade_stats)))

    bars = ax.bar(
        x,
        decade_stats["mean"],
        color=colors,
        edgecolor="black",
        linewidth=1.5,
        alpha=0.8,
        yerr=decade_stats["std"],
        capsize=5,
        error_kw={"linewidth": 2},
    )

    ax.set_xticks(x)
    ax.set_xticklabels(decade_stats["decade_label"], fontsize=11, fontweight="bold")
    ax.set_xlabel("Decade", fontsize=12, fontweight="bold")
    ax.set_ylabel("Average Maximum Temperature (°C)", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Decade Comparison of Maximum Temperatures - {LOCATION_NAME}",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )

    # Add value labels on bars
    for bar, val in zip(bars, decade_stats["mean"]):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.5,
            f"{val:.1f}°C",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    ax.grid(True, alpha=0.3, axis="y")
    ax.set_ylim(bottom=38)

    plt.tight_layout()

    output_path = OUTPUT_DIR / "03_decade_comparison.png"
    plt.savefig(
        output_path,
        dpi=FIGURE_DPI,
        bbox_inches="tight",
        facecolor="white",
        edgecolor="none",
    )
    plt.close()

    print(f"  ✓ Saved: {output_path}")
    return str(output_path)


def main():
    """Main entry point for yearly analysis."""
    print("=" * 70)
    print("Starting Yearly Analysis")
    print("=" * 70)

    # Load data
    print("\n📂 Loading data...")
    df = load_yearly_data()
    print(f"  ✓ Loaded {len(df)} years of data")

    # Compute statistics
    print("\n📊 Computing statistics...")
    stats, df = compute_statistics(df)

    # Print report
    print("\n")
    report = print_analysis_report(stats, df)

    # Generate visualizations
    print("\n🎨 Generating visualizations...")
    plot_yearly_trend(df, stats)
    plot_decade_comparison(df)

    print("\n" + "=" * 70)
    print("✅ Yearly analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
