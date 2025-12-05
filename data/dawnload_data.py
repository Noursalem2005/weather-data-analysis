import requests
import json

LAT = 30.0444
LON = 31.2357
TIMEZONE = "Africa/Cairo"

def fetch_year(year: int) -> dict:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max"
        ]),
        "timezone": TIMEZONE
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

def main():
    output_file = "weather_raw.jsonl"  
    start_year = 2000
    end_year = 2024

    with open(output_file, "w", encoding="utf-8") as f:
        for year in range(start_year, end_year + 1):
            data = fetch_year(year)
            f.write(json.dumps(data) + "\n")
            
            
    print(f"Data downloaded and saved to {output_file}")

if __name__ == "__main__":
    main()
