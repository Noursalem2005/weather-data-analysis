import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "./data/daily_weather.csv"

MONTH_NAMES = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "Jun", 7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

def main():
    df = pd.read_csv(INPUT_FILE)

    # ===== Monthly averages across all years =====
    monthly = df.groupby("month").agg({
        "max_temp": "mean",
        "min_temp": "mean",
        "precipitation": "mean",
        "max_wind": "mean"
    }).reset_index()

    monthly["month_name"] = monthly["month"].map(MONTH_NAMES)

    print("\n=== Monthly Temperature Summary ===")
    print(monthly[["month_name", "max_temp", "min_temp"]])

    hottest_month = monthly.loc[monthly["max_temp"].idxmax()]
    coldest_month = monthly.loc[monthly["max_temp"].idxmin()]

    print(f"\nHottest Month: {hottest_month['month_name']} ({hottest_month['max_temp']:.2f}°C)")
    print(f"Coldest Month: {coldest_month['month_name']} ({coldest_month['max_temp']:.2f}°C)")

    # ===== GRAPH 1 — Temperature per Month =====
    plt.figure(figsize=(10, 5))
    plt.plot(monthly["month_name"], monthly["max_temp"], marker="o", label="Max Temp (Avg)")
    plt.plot(monthly["month_name"], monthly["min_temp"], marker="s", label="Min Temp (Avg)")
    plt.title("Average Monthly Temperatures")
    plt.xlabel("Month")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("monthly_temperature.png")

    # ===== GRAPH 2 — Rainfall Polar Plot =====
    print("Generating Rainfall Polar Plot ...")
    plt.figure(figsize=(8, 8), facecolor="white")

    angles = (monthly["month"] - 1) * (2 * 3.14159 / 12)
    rainfall = monthly["precipitation"].values

    ax = plt.subplot(111, polar=True)
    ax.plot(angles, rainfall, linewidth=2)
    ax.fill(angles, rainfall, alpha=0.3)

    ax.set_theta_direction(-1)     # اتجاه عقارب الساعة
    ax.set_theta_offset(3.14159/2) # يناير فوق

    ax.set_xticks(angles)
    ax.set_xticklabels(monthly["month_name"].values)

    ax.set_title("Monthly Rainfall (Polar Plot)", fontsize=14)
    plt.tight_layout()
    plt.savefig("rainfall_polar_plot.png", dpi=300)

    # ===== GRAPH 3 — Wind Speed Climate Heatmap (Year vs Month) =====
    print("Generating Wind Speed Heatmap ...")

    wind_grouped = df.groupby(["year", "month"])["max_wind"].mean().reset_index()
    wind_pivot = wind_grouped.pivot(index="year", columns="month", values="max_wind")
    wind_pivot = wind_pivot.sort_index(axis=1)

    col_labels = [MONTH_NAMES.get(m, str(m)) for m in wind_pivot.columns]
    wind_pivot.columns = col_labels

    plt.figure(figsize=(10, 6))
    img = plt.imshow(wind_pivot, aspect="auto")
    plt.colorbar(img, label="Avg Max Wind Speed (km/h)")

    plt.title("Wind Speed Climate Heatmap (Year vs Month)")
    plt.xlabel("Month")
    plt.ylabel("Year")

    plt.xticks(ticks=range(len(wind_pivot.columns)), labels=wind_pivot.columns)
    plt.yticks(ticks=range(len(wind_pivot.index)), labels=wind_pivot.index)

    plt.tight_layout()
    plt.savefig("wind_heatmap.png", dpi=300)

    print("\n✅ Monthly analysis completed!")


if __name__ == "__main__":
    main()
