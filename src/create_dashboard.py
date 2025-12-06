"""
Weather Analysis Dashboard
==========================

This module creates a comprehensive multi-panel dashboard that combines
key visualizations into a single publication-quality figure.

The dashboard provides:
- Overview of yearly trends
- Monthly temperature patterns
- Seasonal comparisons
- Climate statistics

This is ideal for presentations and reports where a single figure
needs to convey the complete analysis.

Input: daily_weather.csv, yearly_max_temp.csv
Output: 00_analysis_dashboard.png in output/ directory

Usage:
    python create_dashboard.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import (
    ANOMALY_THRESHOLD_STD,
    DAILY_DATA_FILE,
    FIGURE_DPI,
    LOCATION_NAME,
    MONTH_NAMES,
    OUTPUT_DIR,
    SEASONS,
    YEARLY_MAX_TEMP_FILE,
)


def load_data():
    """Load all required datasets."""
    daily = pd.read_csv(DAILY_DATA_FILE)
    daily["date"] = pd.to_datetime(daily["date"])
    daily["month_name"] = daily["month"].map(MONTH_NAMES)

    yearly = pd.read_csv(YEARLY_MAX_TEMP_FILE)
    yearly["year"] = yearly["year"].astype(int)

    return daily, yearly


def create_dashboard():
    """Create comprehensive analysis dashboard."""
    print("=" * 70)
    print("Creating Weather Analysis Dashboard")
    print("=" * 70)

    # Load data
    print("\n[Loading] Reading datasets...")
    daily, yearly = load_data()

    # Create figure with 2x2 grid layout + stats panel
    fig = plt.figure(figsize=(18, 14))

    # Apply style
    plt.style.use("seaborn-v0_8-whitegrid")

    # =========================================================================
    # Panel 1: Yearly Temperature Trend (top-left, larger)
    # =========================================================================
    ax1 = fig.add_axes([0.05, 0.55, 0.55, 0.38])  # [left, bottom, width, height]

    years = yearly["year"].values
    temps = yearly["max_temperature"].values

    # Trend line
    slope, intercept = np.polyfit(years, temps, 1)
    trend_line = slope * years + intercept

    ax1.plot(
        years,
        temps,
        "o-",
        linewidth=2,
        markersize=8,
        color="#1f77b4",
        label="Yearly Max Temp",
    )
    ax1.plot(
        years,
        trend_line,
        "--",
        linewidth=2.5,
        color="#2ecc71",
        label=f"Trend ({slope*10:+.2f} C/decade)",
    )

    # Highlight anomalies
    mean_temp = temps.mean()
    std_temp = temps.std()
    threshold = mean_temp + ANOMALY_THRESHOLD_STD * std_temp
    anomalies = yearly[yearly["max_temperature"] > threshold]

    if not anomalies.empty:
        ax1.scatter(
            anomalies["year"],
            anomalies["max_temperature"],
            s=150,
            c="red",
            marker="*",
            zorder=5,
            label="Anomalies",
        )

    ax1.axhline(y=mean_temp, color="gray", linestyle=":", alpha=0.7)
    ax1.set_xlabel("Year", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Max Temperature (C)", fontsize=11, fontweight="bold")
    ax1.set_title(
        "Yearly Maximum Temperature Trend (2000-2024)", fontsize=13, fontweight="bold"
    )
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(True, alpha=0.3)

    # =========================================================================
    # Panel 2: Key Statistics Box (top-right)
    # =========================================================================
    ax2 = fig.add_axes([0.65, 0.55, 0.30, 0.38])
    ax2.axis("off")

    # Calculate statistics
    hottest_year = yearly.loc[yearly["max_temperature"].idxmax()]
    coolest_year = yearly.loc[yearly["max_temperature"].idxmin()]

    stats_text = f"""
    KEY STATISTICS
    ─────────────────────────

    Analysis Period
       2000 - 2024 ({len(yearly)} years)

    Temperature Summary
       Mean: {mean_temp:.1f}C
       Std Dev: {std_temp:.2f}C
       Range: {temps.min():.1f} - {temps.max():.1f}C

    Hottest Year
       {int(hottest_year['year'])}: {hottest_year['max_temperature']:.1f}C

    Coolest Year
       {int(coolest_year['year'])}: {coolest_year['max_temperature']:.1f}C

    Trend Analysis
       {slope*10:+.2f}C per decade
       {"[Warming Trend]" if slope > 0 else "[Cooling Trend]"}
    """

    ax2.text(
        0.1,
        0.95,
        stats_text,
        transform=ax2.transAxes,
        fontsize=11,
        verticalalignment="top",
        fontfamily="monospace",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="lightyellow",
            edgecolor="orange",
            alpha=0.9,
        ),
    )

    # =========================================================================
    # Panel 3: Monthly Temperature Pattern (bottom-left)
    # =========================================================================
    ax3 = fig.add_axes([0.05, 0.08, 0.28, 0.38])

    monthly = (
        daily.groupby("month")
        .agg({"max_temp": "mean", "min_temp": "mean"})
        .reset_index()
    )
    monthly["month_name"] = monthly["month"].map(MONTH_NAMES)

    x = np.arange(12)
    width = 0.35

    ax3.bar(
        x - width / 2,
        monthly["max_temp"],
        width,
        label="Max Temp",
        color="#e74c3c",
        alpha=0.8,
    )
    ax3.bar(
        x + width / 2,
        monthly["min_temp"],
        width,
        label="Min Temp",
        color="#3498db",
        alpha=0.8,
    )

    ax3.set_xticks(x)
    ax3.set_xticklabels(monthly["month_name"], rotation=45, ha="right", fontsize=8)
    ax3.set_ylabel("Temperature (C)", fontsize=10, fontweight="bold")
    ax3.set_title("Monthly Average Temperatures", fontsize=12, fontweight="bold")
    ax3.legend(fontsize=8)
    ax3.grid(True, alpha=0.3, axis="y")

    # =========================================================================
    # Panel 4: Rainfall Polar Plot (bottom-center)
    # =========================================================================
    ax4 = fig.add_axes([0.38, 0.08, 0.28, 0.38], polar=True)

    precip_monthly = daily.groupby("month")["precipitation"].mean()
    angles = np.linspace(0, 2 * np.pi, 12, endpoint=False).tolist()
    rainfall = precip_monthly.values.tolist()

    angles += angles[:1]
    rainfall += rainfall[:1]

    ax4.plot(angles, rainfall, "o-", linewidth=2, color="#3498db", markersize=6)
    ax4.fill(angles, rainfall, alpha=0.35, color="#3498db")
    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(list(MONTH_NAMES.values()), fontsize=8)
    ax4.set_theta_direction(-1)
    ax4.set_theta_offset(np.pi / 2)
    ax4.set_title("Monthly Rainfall Pattern", fontsize=12, fontweight="bold", pad=15)

    # =========================================================================
    # Panel 5: Decade Comparison (bottom-right)
    # =========================================================================
    ax5 = fig.add_axes([0.70, 0.08, 0.26, 0.38])

    yearly_copy = yearly.copy()
    yearly_copy["decade"] = (yearly_copy["year"] // 10) * 10
    yearly_copy["decade_label"] = yearly_copy["decade"].astype(str) + "s"

    decade_stats = yearly_copy.groupby("decade_label")["max_temperature"].agg(
        ["mean", "min", "max", "std"]
    )
    decade_stats = decade_stats.reset_index()

    x = np.arange(len(decade_stats))
    colors = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(decade_stats)))

    bars = ax5.bar(
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

    ax5.set_xticks(x)
    ax5.set_xticklabels(decade_stats["decade_label"], fontsize=10, fontweight="bold")
    ax5.set_xlabel("Decade", fontsize=10, fontweight="bold")
    ax5.set_ylabel("Avg Max Temp (°C)", fontsize=10, fontweight="bold")
    ax5.set_title("Decade Comparison", fontsize=12, fontweight="bold")

    # Add value labels on bars
    for bar, val in zip(bars, decade_stats["mean"]):
        height = bar.get_height()
        ax5.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.3,
            f"{val:.1f}°C",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
        )

    ax5.grid(True, alpha=0.3, axis="y")

    # =========================================================================
    # Main Title
    # =========================================================================
    fig.suptitle(
        f"Weather Data Analysis Dashboard - {LOCATION_NAME}\n"
        f"Distributed Processing Project | Map-Reduce Analysis | 2000-2024",
        fontsize=16,
        fontweight="bold",
        y=0.98,
    )

    # Save dashboard
    output_path = OUTPUT_DIR / "00_analysis_dashboard.png"
    plt.savefig(
        output_path,
        dpi=FIGURE_DPI,
        bbox_inches="tight",
        facecolor="white",
        edgecolor="none",
    )
    plt.close()

    print(f"\n  [OK] Dashboard saved: {output_path}")
    print("\n" + "=" * 70)
    print("[SUCCESS] Dashboard created successfully!")
    print("=" * 70)

    return str(output_path)


def main():
    """Main entry point."""
    create_dashboard()


if __name__ == "__main__":
    main()
