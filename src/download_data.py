"""
Download Weather Data Module
============================

This module handles the collection of historical weather data from the
Open-Meteo Archive API. It demonstrates a simple ETL (Extract) process
for distributed data processing.

The script downloads daily weather metrics including:
- Maximum and minimum temperatures
- Precipitation totals
- Maximum wind speeds

Data Source: https://open-meteo.com/
Location: Cairo, Egypt (30.0444°N, 31.2357°E)
Time Range: 2000-2024

Usage:
    python download_data.py
"""

import json
from typing import Any, Dict

import requests

from config import (
    END_YEAR,
    LATITUDE,
    LOCATION_NAME,
    LONGITUDE,
    RAW_DATA_FILE,
    START_YEAR,
    TIMEZONE,
    WEATHER_METRICS,
)


def fetch_year_data(year: int) -> Dict[str, Any]:
    """
    Fetch weather data for a specific year from Open-Meteo API.

    This function makes an HTTP request to the Open-Meteo Archive API
    to retrieve daily weather observations for the specified year.

    Args:
        year: The year to fetch data for (e.g., 2023)

    Returns:
        Dictionary containing the API response with daily weather data

    Raises:
        requests.HTTPError: If the API request fails
    """
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
        "daily": ",".join(WEATHER_METRICS),
        "timezone": TIMEZONE,
    }

    print(f"  Fetching data for year {year}...")
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def download_all_data() -> None:
    """
    Download weather data for all configured years and save to JSONL file.

    This function iterates through each year in the configured range,
    fetches the data from the API, and saves each year's response as
    a separate line in a JSON Lines (.jsonl) file.

    The JSONL format is chosen because:
    - It allows streaming/appending data
    - Each line is an independent JSON object
    - It's efficient for large datasets and distributed processing
    """
    print("=" * 60)
    print(f"Weather Data Download - {LOCATION_NAME}")
    print("=" * 60)
    print(f"Location: {LATITUDE}°N, {LONGITUDE}°E")
    print(f"Period: {START_YEAR} - {END_YEAR}")
    print(f"Output: {RAW_DATA_FILE}")
    print("-" * 60)

    total_years = END_YEAR - START_YEAR + 1

    with open(RAW_DATA_FILE, "w", encoding="utf-8") as file:
        for i, year in enumerate(range(START_YEAR, END_YEAR + 1), 1):
            data = fetch_year_data(year)
            file.write(json.dumps(data) + "\n")
            print(f"  ✓ Year {year} downloaded ({i}/{total_years})")

    print("-" * 60)
    print(f"✅ Download complete! Data saved to: {RAW_DATA_FILE}")
    print("=" * 60)


def main():
    """Main entry point for the download script."""
    download_all_data()


if __name__ == "__main__":
    main()
