import json
import pandas as pd

RAW_FILE = "weather_raw.jsonl"
OUTPUT_FILE = "daily_weather.csv"

def main():
    rows = []
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue
            daily = data.get("daily", {})
            dates = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            precips = daily.get("precipitation_sum", [])
            max_winds = daily.get("windspeed_10m_max", [])
            
            for d, tmax, tmin, p, w in zip(dates, max_temps, min_temps, precips, max_winds):
                year = int(d.split("-")[0])
                month = int(d.split("-")[1])
                rows.append({
                    "date": d,
                    "year": year,
                    "month": month,
                    "max_temp": float(tmax) if tmax is not None else None,
                    "min_temp": float(tmin) if tmin is not None else None,
                    "precipitation": float(p) if p is not None else None,
                    "max_wind": float(w) if w is not None else None
                })

    df = pd.DataFrame(rows)
    df = df.sort_values(by="date")
    df.to_csv(OUTPUT_FILE, index=False)
if __name__ == "__main__":
    main()
