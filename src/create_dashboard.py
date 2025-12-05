"""
Weather Analysis Dashboard
==========================

This module creates a comprehensive multi-panel dashboard that combines
all key visualizations into a single publication-quality figure.

The dashboard provides:
- Overview of yearly trends
- Monthly temperature patterns
- Seasonal comparisons
- Climate statistics

This is ideal for presentations and reports where a single figure
needs to convey the complete analysis.

Input: daily_weather.csv, yearly_max_temp.csv
Output: dashboard.png in output/ directory

Usage:
    python create_dashboard.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec

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
    print("\n📂 Loading data...")
    daily, yearly = load_data()

    # Create figure with grid layout
    fig = plt.figure(figsize=(20, 16))
    gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

    # Apply style
    plt.style.use("seaborn-v0_8-whitegrid")

    # =========================================================================
    # Panel 1: Yearly Temperature Trend (spanning 2 columns)
    # =========================================================================
    ax1 = fig.add_subplot(gs[0, :2])

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
        label=f"Trend ({slope*10:+.2f}°C/decade)",
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
    ax1.set_ylabel("Max Temperature (°C)", fontsize=11, fontweight="bold")
    ax1.set_title(
        "Yearly Maximum Temperature Trend (2000-2024)", fontsize=13, fontweight="bold"
    )
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(True, alpha=0.3)

    # =========================================================================
    # Panel 2: Key Statistics Box
    # =========================================================================
    ax2 = fig.add_subplot(gs[0, 2])
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
       Mean: {mean_temp:.1f}°C
       Std Dev: {std_temp:.2f}°C
       Range: {temps.min():.1f} - {temps.max():.1f}°C
    
    Hottest Year
       {int(hottest_year['year'])}: {hottest_year['max_temperature']:.1f}°C
    
    Coolest Year
       {int(coolest_year['year'])}: {coolest_year['max_temperature']:.1f}°C
    
    Trend Analysis
       {slope*10:+.2f}°C per decade
       {"Warming Trend" if slope > 0 else "Cooling Trend"}
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
    # Panel 3: Monthly Temperature Pattern
    # =========================================================================
    ax3 = fig.add_subplot(gs[1, 0])

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
    ax3.set_xticklabels(monthly["month_name"], rotation=45, ha="right", fontsize=9)
    ax3.set_ylabel("Temperature (°C)", fontsize=10, fontweight="bold")
    ax3.set_title("Monthly Average Temperatures", fontsize=12, fontweight="bold")
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, axis="y")

    # =========================================================================
    # Panel 4: Rainfall Polar Plot
    # =========================================================================
    ax4 = fig.add_subplot(gs[1, 1], polar=True)

    precip_monthly = daily.groupby("month")["precipitation"].mean()
    angles = np.linspace(0, 2 * np.pi, 12, endpoint=False).tolist()
    rainfall = precip_monthly.values.tolist()

    angles += angles[:1]
    rainfall += rainfall[:1]

    ax4.plot(angles, rainfall, "o-", linewidth=2, color="#3498db", markersize=6)
    ax4.fill(angles, rainfall, alpha=0.35, color="#3498db")
    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(list(MONTH_NAMES.values()), fontsize=9)
    ax4.set_theta_direction(-1)
    ax4.set_theta_offset(np.pi / 2)
    ax4.set_title("Monthly Rainfall Pattern", fontsize=12, fontweight="bold", pad=15)

    # =========================================================================
    # Panel 5: Seasonal Box Plot
    # =========================================================================
    ax5 = fig.add_subplot(gs[1, 2])

    def get_season(month):
        for season, months in SEASONS.items():
            if month in months:
                return season
        return "Unknown"

    daily_copy = daily.copy()
    daily_copy["season"] = daily_copy["month"].apply(get_season)

    season_order = ["Winter", "Spring", "Summer", "Autumn"]
    colors = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]

    box_data = [
        daily_copy[daily_copy["season"] == s]["max_temp"].dropna() for s in season_order
    ]
    bp = ax5.boxplot(box_data, patch_artist=True, labels=season_order)

    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax5.set_ylabel("Max Temperature (°C)", fontsize=10, fontweight="bold")
    ax5.set_title("Temperature by Season", fontsize=12, fontweight="bold")
    ax5.grid(True, alpha=0.3, axis="y")

    # =========================================================================
    # Panel 6: Temperature Heatmap
    # =========================================================================
    ax6 = fig.add_subplot(gs[2, :2])

    temp_pivot = daily.pivot_table(
        values="max_temp", index="year", columns="month", aggfunc="mean"
    )
    temp_pivot.columns = [MONTH_NAMES[m] for m in temp_pivot.columns]

    sns.heatmap(
        temp_pivot,
        cmap="RdYlBu_r",
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        cbar_kws={"label": "Avg Max Temp (°C)"},
        ax=ax6,
        annot_kws={"size": 8},
    )

    ax6.set_xlabel("Month", fontsize=11, fontweight="bold")
    ax6.set_ylabel("Year", fontsize=11, fontweight="bold")
    ax6.set_title(
        "Temperature Climate Matrix (Year × Month)", fontsize=12, fontweight="bold"
    )

    # =========================================================================
    # Panel 7: Correlation Matrix
    # =========================================================================
    ax7 = fig.add_subplot(gs[2, 2])

    numeric_cols = ["max_temp", "min_temp", "precipitation", "max_wind"]
    col_labels = ["Max T", "Min T", "Precip", "Wind"]
    corr_matrix = daily[numeric_cols].corr()

    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=1,
        square=True,
        xticklabels=col_labels,
        yticklabels=col_labels,
        annot_kws={"size": 11, "weight": "bold"},
        ax=ax7,
    )

    ax7.set_title("Variable Correlations", fontsize=12, fontweight="bold")

    # =========================================================================
    # Main Title
    # =========================================================================
    fig.suptitle(
        f"Weather Data Analysis Dashboard - {LOCATION_NAME}\n"
        f"Distributed Processing Project | 2000-2024",
        fontsize=18,
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

    print(f"\n  ✓ Dashboard saved: {output_path}")
    print("\n" + "=" * 70)
    print("✅ Dashboard created successfully!")
    print("=" * 70)

    return str(output_path)


def main():
    """Main entry point."""
    create_dashboard()


if __name__ == "__main__":
    main()
