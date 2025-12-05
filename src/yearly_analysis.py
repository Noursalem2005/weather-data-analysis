import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

INPUT_FILE = "yearly_max_temp.csv"
PLOT_FILE = "yearly_max_temp_trend_anomalies.png"


def main():
    df = pd.read_csv(INPUT_FILE)
    df["year"] = df["year"].astype(int)
    df["max_temperature"] = df["max_temperature"].astype(float)

    df = df.sort_values("year")

    years = df["year"].values
    temps = df["max_temperature"].values

    overall_max_temp = temps.max()
    overall_min_temp = temps.min()
    mean_max_temp = temps.mean()

    year_hottest = df.loc[df["max_temperature"].idxmax(), "year"]
    year_coolest = df.loc[df["max_temperature"].idxmin(), "year"]

    print("\n=== Summary Statistics ===")
    print(f"Number of years: {len(df)}")
    print(f"Hottest year: {year_hottest} with max temp = {overall_max_temp:.2f}°C")
    print(f"Coolest year: {year_coolest} with max temp = {overall_min_temp:.2f}°C")
    print(f"Average of yearly max temperatures: {mean_max_temp:.2f}°C")

    #Trend Analysis 
    slope, intercept = np.polyfit(years, temps, 1)
    trend_line = slope * years + intercept

    print("\n=== Trend Analysis ===")
    print(f"Slope: {slope:.4f} °C per year")
    if slope > 0:
        print("Interpretation: There is a general trend of increasing temperatures over the years.")
    elif slope < 0:
        print("Interpretation: There is a general trend of decreasing temperatures over the years.")
    else:
        print("Interpretation: No clear trend (slope ≈ 0).")

    # Anomalies
    mean_temp = temps.mean()
    std_temp = temps.std()
    threshold = mean_temp + 1.5 * std_temp

    df["is_anomaly"] = df["max_temperature"] > threshold
    anomalies = df[df["is_anomaly"]]

    print("\n=== Anomaly Detection ===")
    print(f"Mean of yearly max temperatures: {mean_temp:.2f} °C")
    print(f"Standard deviation: {std_temp:.2f} °C")
    print(f"Anomaly threshold: > {threshold:.2f} °C")
    if anomalies.empty:
        print("No strong anomalies detected based on this threshold.")
    else:
        print("Years detected as unusually hot (anomalies):")
        for _, row in anomalies.iterrows():
            print(f"  Year {int(row['year'])}: {row['max_temperature']:.2f} °C")

    # Plot: Temps + Trend + Anomalies 
    plt.figure(figsize=(10, 6))
    plt.plot(years, temps, marker="o", label="Yearly Max Temp")
    plt.plot(years, trend_line, linestyle="--", label="Trend Line")

    if not anomalies.empty:
        plt.scatter(
            anomalies["year"],
            anomalies["max_temperature"],
            s=80,
            label="Anomaly (Unusually Hot)",
        )

    plt.xlabel("Year")
    plt.ylabel("Maximum Temperature (°C)")
    plt.title("Yearly Maximum Temperature – Trend & Anomalies")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_FILE)


if __name__ == "__main__":
    main()
