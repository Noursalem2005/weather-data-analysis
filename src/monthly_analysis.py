"""
Monthly Analysis and Visualization Module
==========================================

This module performs comprehensive monthly analysis of weather data,
providing insights into seasonal patterns and variations throughout
the year.

Analysis includes:
- Monthly temperature patterns (average max/min)
- Precipitation patterns
- Wind speed analysis
- Seasonal comparisons
- Climate heatmaps

Input: daily_weather.csv
Output: Various visualizations in output/ directory

Usage:
    python monthly_analysis.py
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

from config import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    DAILY_DATA_FILE,
    FIGURE_DPI,
    FIGURE_SIZE_HEATMAP,
    FIGURE_SIZE_SQUARE,
    FIGURE_SIZE_STANDARD,
    FIGURE_SIZE_WIDE,
    LOCATION_NAME,
    MONTH_FULL_NAMES,
    MONTH_NAMES,
    OUTPUT_DIR,
    SEASONS,
)


def load_daily_data() -> pd.DataFrame:
    """
    Load and prepare daily weather data.

    Returns:
        DataFrame with daily weather observations
    """
    df = pd.read_csv(DAILY_DATA_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df["month_name"] = df["month"].map(MONTH_NAMES)

    # Add season column
    def get_season(month):
        for season, months in SEASONS.items():
            if month in months:
                return season
        return "Unknown"

    df["season"] = df["month"].apply(get_season)

    return df


def compute_monthly_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly statistics across all years.

    Args:
        df: Daily weather DataFrame

    Returns:
        DataFrame with monthly averages
    """
    monthly = (
        df.groupby("month")
        .agg(
            {
                "max_temp": ["mean", "std", "min", "max"],
                "min_temp": ["mean", "std", "min", "max"],
                "precipitation": ["mean", "sum", "max"],
                "max_wind": ["mean", "max"],
            }
        )
        .reset_index()
    )

    # Flatten column names
    monthly.columns = ["_".join(col).strip("_") for col in monthly.columns]
    monthly["month_name"] = monthly["month"].map(MONTH_NAMES)

    return monthly


def print_monthly_report(monthly: pd.DataFrame, df: pd.DataFrame) -> None:
    """
    Print a formatted monthly analysis report.

    Args:
        monthly: Monthly statistics DataFrame
        df: Original daily DataFrame
    """
    print("=" * 70)
    print(f"MONTHLY CLIMATE ANALYSIS - {LOCATION_NAME}")
    print("=" * 70)

    print("\n📊 MONTHLY TEMPERATURE AVERAGES")
    print("-" * 70)
    print(f"{'Month':<10} {'Avg Max (°C)':<15} {'Avg Min (°C)':<15} {'Range (°C)':<15}")
    print("-" * 55)

    for _, row in monthly.iterrows():
        month = row["month_name"]
        max_t = row["max_temp_mean"]
        min_t = row["min_temp_mean"]
        range_t = max_t - min_t
        print(f"{month:<10} {max_t:>10.1f}     {min_t:>10.1f}     {range_t:>10.1f}")

    # Find extremes
    hottest = monthly.loc[monthly["max_temp_mean"].idxmax()]
    coldest = monthly.loc[monthly["max_temp_mean"].idxmin()]
    wettest = monthly.loc[monthly["precipitation_mean"].idxmax()]
    driest = monthly.loc[monthly["precipitation_mean"].idxmin()]
    windiest = monthly.loc[monthly["max_wind_mean"].idxmax()]

    print("\n🌡️ CLIMATE EXTREMES BY MONTH")
    print("-" * 70)
    print(
        f"  🔥 Hottest Month: {hottest['month_name']} (Avg Max: {hottest['max_temp_mean']:.1f}°C)"
    )
    print(
        f"  ❄️  Coldest Month: {coldest['month_name']} (Avg Max: {coldest['max_temp_mean']:.1f}°C)"
    )
    print(
        f"  🌧️  Wettest Month: {wettest['month_name']} (Avg Precip: {wettest['precipitation_mean']:.1f}mm)"
    )
    print(
        f"  ☀️  Driest Month: {driest['month_name']} (Avg Precip: {driest['precipitation_mean']:.2f}mm)"
    )
    print(
        f"  💨 Windiest Month: {windiest['month_name']} (Avg Max Wind: {windiest['max_wind_mean']:.1f}km/h)"
    )

    # Seasonal analysis
    print("\n🍂 SEASONAL SUMMARY")
    print("-" * 70)
    seasonal = (
        df.groupby("season")
        .agg({"max_temp": "mean", "min_temp": "mean", "precipitation": "mean"})
        .round(1)
    )

    for season in ["Winter", "Spring", "Summer", "Autumn"]:
        if season in seasonal.index:
            s = seasonal.loc[season]
            print(
                f"  {season:<10}: Max {s['max_temp']:.1f}°C, Min {s['min_temp']:.1f}°C, Precip {s['precipitation']:.1f}mm/day"
            )

    print("=" * 70)


def plot_monthly_temperature(monthly: pd.DataFrame) -> str:
    """
    Create monthly temperature visualization with range.

    Args:
        monthly: Monthly statistics DataFrame

    Returns:
        Path to saved figure
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

    months = monthly["month_name"]
    x = np.arange(len(months))
    width = 0.35

    # Plot max and min temperature bars
    bars1 = ax.bar(
        x - width / 2,
        monthly["max_temp_mean"],
        width,
        label="Avg Max Temp",
        color="#e74c3c",
        alpha=0.8,
        yerr=monthly["max_temp_std"],
        capsize=3,
    )
    bars2 = ax.bar(
        x + width / 2,
        monthly["min_temp_mean"],
        width,
        label="Avg Min Temp",
        color="#3498db",
        alpha=0.8,
        yerr=monthly["min_temp_std"],
        capsize=3,
    )

    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 1,
            f"{height:.0f}°",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    for bar in bars2:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 1,
            f"{height:.0f}°",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    ax.set_xlabel("Month", fontsize=12, fontweight="bold")
    ax.set_ylabel("Temperature (°C)", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Monthly Average Temperatures - {LOCATION_NAME}",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=10)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, alpha=0.3, axis="y")
    ax.set_ylim(0, monthly["max_temp_mean"].max() + 10)

    plt.tight_layout()

    output_path = OUTPUT_DIR / "04_monthly_temperature.png"
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


def plot_temperature_line_chart(monthly: pd.DataFrame) -> str:
    """
    Create line chart showing temperature variation through the year.

    Args:
        monthly: Monthly statistics DataFrame

    Returns:
        Path to saved figure
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

    months = monthly["month_name"]

    # Plot lines with shaded area between max and min
    ax.fill_between(
        months,
        monthly["max_temp_mean"],
        monthly["min_temp_mean"],
        alpha=0.3,
        color="#9b59b6",
        label="Temperature Range",
    )

    ax.plot(
        months,
        monthly["max_temp_mean"],
        marker="o",
        markersize=10,
        linewidth=3,
        color="#e74c3c",
        label="Avg Max Temperature",
    )
    ax.plot(
        months,
        monthly["min_temp_mean"],
        marker="s",
        markersize=8,
        linewidth=3,
        color="#3498db",
        label="Avg Min Temperature",
    )

    # Add average line
    avg_temp = (monthly["max_temp_mean"] + monthly["min_temp_mean"]) / 2
    ax.plot(
        months,
        avg_temp,
        linestyle="--",
        linewidth=2,
        color="#2ecc71",
        label="Mean Temperature",
    )

    ax.set_xlabel("Month", fontsize=12, fontweight="bold")
    ax.set_ylabel("Temperature (°C)", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Annual Temperature Cycle - {LOCATION_NAME}",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.legend(loc="lower right", fontsize=10)
    ax.grid(True, alpha=0.3)

    # Rotate x-labels for better readability
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = OUTPUT_DIR / "05_temperature_cycle.png"
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


def plot_rainfall_polar(monthly: pd.DataFrame) -> str:
    """
    Create polar/radar chart for rainfall distribution.

    Args:
        monthly: Monthly statistics DataFrame

    Returns:
        Path to saved figure
    """
    fig = plt.figure(figsize=FIGURE_SIZE_SQUARE)
    ax = fig.add_subplot(111, polar=True)

    # Calculate angles for each month
    angles = np.linspace(0, 2 * np.pi, 12, endpoint=False).tolist()
    rainfall = monthly["precipitation_mean"].values.tolist()

    # Close the plot
    angles += angles[:1]
    rainfall += rainfall[:1]

    # Plot
    ax.plot(angles, rainfall, "o-", linewidth=2, color="#3498db", markersize=8)
    ax.fill(angles, rainfall, alpha=0.35, color="#3498db")

    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(list(MONTH_NAMES.values()), fontsize=11, fontweight="bold")

    # Set direction and offset
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi / 2)

    ax.set_title(
        f"Monthly Rainfall Distribution - {LOCATION_NAME}",
        fontsize=14,
        fontweight="bold",
        pad=20,
        y=1.08,
    )

    plt.tight_layout()

    output_path = OUTPUT_DIR / "06_rainfall_polar.png"
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


def plot_precipitation_bar(monthly: pd.DataFrame) -> str:
    """
    Create bar chart for monthly precipitation.

    Args:
        monthly: Monthly statistics DataFrame

    Returns:
        Path to saved figure
    """
    fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

    months = monthly["month_name"]
    precipitation = monthly["precipitation_mean"]

    # Create gradient colors based on precipitation
    colors = plt.cm.Blues(precipitation / precipitation.max() * 0.8 + 0.2)

    bars = ax.bar(months, precipitation, color=colors, edgecolor="navy", linewidth=1.5)

    # Add value labels
    for bar, val in zip(bars, precipitation):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 0.05,
            f"{val:.2f}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_xlabel("Month", fontsize=12, fontweight="bold")
    ax.set_ylabel("Average Precipitation (mm/day)", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Monthly Average Precipitation - {LOCATION_NAME}",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )
    ax.grid(True, alpha=0.3, axis="y")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    output_path = OUTPUT_DIR / "07_precipitation_monthly.png"
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


def plot_wind_heatmap(df: pd.DataFrame) -> str:
    """
    Create heatmap of wind speeds across years and months.

    Args:
        df: Daily weather DataFrame

    Returns:
        Path to saved figure
    """
    # Aggregate wind data by year and month
    wind_pivot = df.pivot_table(
        values="max_wind", index="year", columns="month", aggfunc="mean"
    )

    # Rename columns to month names
    wind_pivot.columns = [MONTH_NAMES[m] for m in wind_pivot.columns]

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_HEATMAP)

    # Create custom colormap
    cmap = LinearSegmentedColormap.from_list(
        "wind_cmap", ["#f7fbff", "#4292c6", "#08306b"]
    )

    sns.heatmap(
        wind_pivot,
        cmap=cmap,
        annot=True,
        fmt=".1f",
        linewidths=0.5,
        cbar_kws={"label": "Avg Max Wind Speed (km/h)"},
        ax=ax,
    )

    ax.set_xlabel("Month", fontsize=12, fontweight="bold")
    ax.set_ylabel("Year", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Wind Speed Climate Heatmap - {LOCATION_NAME}",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )

    plt.tight_layout()

    output_path = OUTPUT_DIR / "08_wind_heatmap.png"
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


def plot_temperature_heatmap(df: pd.DataFrame) -> str:
    """
    Create heatmap of temperatures across years and months.

    Args:
        df: Daily weather DataFrame

    Returns:
        Path to saved figure
    """
    # Aggregate temperature data by year and month
    temp_pivot = df.pivot_table(
        values="max_temp", index="year", columns="month", aggfunc="mean"
    )

    # Rename columns to month names
    temp_pivot.columns = [MONTH_NAMES[m] for m in temp_pivot.columns]

    fig, ax = plt.subplots(figsize=FIGURE_SIZE_HEATMAP)

    # Create custom colormap (cool to warm)
    cmap = LinearSegmentedColormap.from_list(
        "temp_cmap", ["#2166ac", "#f7f7f7", "#b2182b"]
    )

    sns.heatmap(
        temp_pivot,
        cmap=cmap,
        annot=True,
        fmt=".1f",
        linewidths=0.5,
        cbar_kws={"label": "Avg Max Temperature (°C)"},
        ax=ax,
        center=temp_pivot.values.mean(),
    )

    ax.set_xlabel("Month", fontsize=12, fontweight="bold")
    ax.set_ylabel("Year", fontsize=12, fontweight="bold")
    ax.set_title(
        f"Temperature Climate Heatmap - {LOCATION_NAME}",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )

    plt.tight_layout()

    output_path = OUTPUT_DIR / "09_temperature_heatmap.png"
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


def plot_seasonal_boxplot(df: pd.DataFrame) -> str:
    """
    Create seasonal comparison boxplots.

    Args:
        df: Daily weather DataFrame

    Returns:
        Path to saved figure
    """
    fig, axes = plt.subplots(1, 2, figsize=FIGURE_SIZE_WIDE)

    season_order = ["Winter", "Spring", "Summer", "Autumn"]
    colors = {
        "Winter": "#3498db",
        "Spring": "#2ecc71",
        "Summer": "#e74c3c",
        "Autumn": "#f39c12",
    }

    # Temperature boxplot
    ax1 = axes[0]
    box_data = [df[df["season"] == s]["max_temp"].dropna() for s in season_order]
    bp = ax1.boxplot(box_data, patch_artist=True, labels=season_order)

    for patch, season in zip(bp["boxes"], season_order):
        patch.set_facecolor(colors[season])
        patch.set_alpha(0.7)

    ax1.set_ylabel("Max Temperature (°C)", fontsize=11, fontweight="bold")
    ax1.set_title("Temperature by Season", fontsize=12, fontweight="bold")
    ax1.grid(True, alpha=0.3, axis="y")

    # Precipitation boxplot
    ax2 = axes[1]
    box_data = [df[df["season"] == s]["precipitation"].dropna() for s in season_order]
    bp = ax2.boxplot(box_data, patch_artist=True, labels=season_order)

    for patch, season in zip(bp["boxes"], season_order):
        patch.set_facecolor(colors[season])
        patch.set_alpha(0.7)

    ax2.set_ylabel("Precipitation (mm)", fontsize=11, fontweight="bold")
    ax2.set_title("Precipitation by Season", fontsize=12, fontweight="bold")
    ax2.grid(True, alpha=0.3, axis="y")

    plt.suptitle(
        f"Seasonal Climate Comparison - {LOCATION_NAME}",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()

    output_path = OUTPUT_DIR / "10_seasonal_comparison.png"
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


def plot_correlation_matrix(df: pd.DataFrame) -> str:
    """
    Create correlation matrix heatmap for weather variables.

    Args:
        df: Daily weather DataFrame

    Returns:
        Path to saved figure
    """
    # Select numeric columns for correlation
    numeric_cols = ["max_temp", "min_temp", "precipitation", "max_wind"]
    col_labels = ["Max Temp", "Min Temp", "Precipitation", "Max Wind"]

    corr_matrix = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))

    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

    sns.heatmap(
        corr_matrix,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="RdYlBu_r",
        center=0,
        linewidths=2,
        square=True,
        cbar_kws={"label": "Correlation Coefficient"},
        xticklabels=col_labels,
        yticklabels=col_labels,
        annot_kws={"size": 14, "weight": "bold"},
    )

    ax.set_title(
        f"Weather Variables Correlation Matrix - {LOCATION_NAME}",
        fontsize=14,
        fontweight="bold",
        pad=15,
    )

    plt.tight_layout()

    output_path = OUTPUT_DIR / "11_correlation_matrix.png"
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
    """Main entry point for monthly analysis."""
    print("=" * 70)
    print("Starting Monthly Climate Analysis")
    print("=" * 70)

    # Load data
    print("\n📂 Loading data...")
    df = load_daily_data()
    print(f"  ✓ Loaded {len(df):,} daily observations")

    # Compute monthly statistics
    print("\n📊 Computing monthly statistics...")
    monthly = compute_monthly_statistics(df)

    # Print report
    print("\n")
    print_monthly_report(monthly, df)

    # Generate visualizations
    print("\n🎨 Generating visualizations...")
    plot_monthly_temperature(monthly)
    plot_temperature_line_chart(monthly)
    plot_rainfall_polar(monthly)
    plot_precipitation_bar(monthly)
    plot_wind_heatmap(df)
    plot_temperature_heatmap(df)
    plot_seasonal_boxplot(df)
    plot_correlation_matrix(df)

    print("\n" + "=" * 70)
    print("✅ Monthly analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
