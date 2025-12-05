"""
Build Daily Dataset Module
==========================

This module transforms raw JSON Lines weather data into a structured
CSV format suitable for analysis. It demonstrates the Transform step
of an ETL pipeline.

The transformation includes:
- Parsing nested JSON structures
- Extracting temporal features (year, month)
- Handling missing values
- Sorting by date

Input: weather_raw.jsonl (raw API responses)
Output: daily_weather.csv (structured daily observations)

Usage:
    python build_daily_dataset.py
"""

import json
from typing import Any, Dict, List, Optional

import pandas as pd

from config import DAILY_DATA_FILE, RAW_DATA_FILE


def parse_jsonl_line(line: str) -> List[Dict[str, Any]]:
    """
    Parse a single JSONL line and extract daily weather records.

    Each line in the JSONL file contains a full year of daily data.
    This function extracts individual daily records from the nested
    JSON structure.

    Args:
        line: A single line from the JSONL file (JSON string)

    Returns:
        List of dictionaries, each representing one day's weather data
    """
    line = line.strip()
    if not line:
        return []

    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return []

    daily = data.get("daily", {})
    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    precipitations = daily.get("precipitation_sum", [])
    max_winds = daily.get("windspeed_10m_max", [])

    records = []
    for date, tmax, tmin, precip, wind in zip(
        dates, max_temps, min_temps, precipitations, max_winds
    ):
        # Extract year and month from date string (YYYY-MM-DD)
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])

        records.append(
            {
                "date": date,
                "year": year,
                "month": month,
                "max_temp": safe_float(tmax),
                "min_temp": safe_float(tmin),
                "precipitation": safe_float(precip),
                "max_wind": safe_float(wind),
            }
        )

    return records


def safe_float(value: Any) -> Optional[float]:
    """
    Safely convert a value to float, returning None for invalid values.

    Args:
        value: Any value to convert

    Returns:
        Float value or None if conversion fails
    """
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_dataset() -> pd.DataFrame:
    """
    Build a complete daily weather dataset from raw JSONL data.

    This function reads the raw JSONL file, parses each line to extract
    daily records, and combines them into a single pandas DataFrame.

    Returns:
        DataFrame with columns: date, year, month, max_temp, min_temp,
        precipitation, max_wind
    """
    print("=" * 60)
    print("Building Daily Weather Dataset")
    print("=" * 60)
    print(f"Input: {RAW_DATA_FILE}")
    print(f"Output: {DAILY_DATA_FILE}")
    print("-" * 60)

    all_records = []
    line_count = 0

    with open(RAW_DATA_FILE, "r", encoding="utf-8") as file:
        for line in file:
            records = parse_jsonl_line(line)
            all_records.extend(records)
            line_count += 1

    print(f"  Processed {line_count} year(s) of data")
    print(f"  Total daily records: {len(all_records)}")

    # Create DataFrame and sort by date
    df = pd.DataFrame(all_records)
    df = df.sort_values(by="date").reset_index(drop=True)

    return df


def save_dataset(df: pd.DataFrame) -> None:
    """
    Save the dataset to CSV file.

    Args:
        df: DataFrame to save
    """
    df.to_csv(DAILY_DATA_FILE, index=False)
    print(f"  ✓ Dataset saved to: {DAILY_DATA_FILE}")


def print_dataset_summary(df: pd.DataFrame) -> None:
    """
    Print a summary of the dataset for verification.

    Args:
        df: DataFrame to summarize
    """
    print("-" * 60)
    print("Dataset Summary:")
    print(f"  Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"  Years covered: {df['year'].min()} - {df['year'].max()}")
    print(f"  Total observations: {len(df):,}")
    print(f"  Missing values:")
    for col in ["max_temp", "min_temp", "precipitation", "max_wind"]:
        missing = df[col].isna().sum()
        print(f"    - {col}: {missing} ({missing/len(df)*100:.2f}%)")
    print("=" * 60)


def main():
    """Main entry point for dataset building."""
    df = build_dataset()
    save_dataset(df)
    print_dataset_summary(df)
    print("✅ Dataset building complete!")


if __name__ == "__main__":
    main()
