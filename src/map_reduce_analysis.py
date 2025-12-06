"""
Map-Reduce Implementation for Yearly Maximum Temperature
=========================================================

This module demonstrates the Map-Reduce paradigm applied to weather
data processing. It computes the maximum temperature for each year
using the classic Map-Reduce pattern.

Map-Reduce Pattern:
    1. MAP: Extract (year, temperature) pairs from each record
    2. SHUFFLE: Group temperatures by year
    3. REDUCE: Compute maximum temperature for each year

This pattern is foundational in distributed processing systems like
Hadoop and Spark, allowing parallel processing of large datasets.

Input: weather_raw.jsonl
Output: yearly_max_temp.csv

Usage:
    python map_reduce.py
"""

import json
from typing import Dict, List, Tuple

from config import RAW_DATA_FILE, YEARLY_MAX_TEMP_FILE

# =============================================================================
# MAP PHASE
# =============================================================================


def mapper(line: str) -> List[Tuple[str, float]]:
    """
    Map function: Extract (year, temperature) pairs from a JSONL line.

    This function implements the MAP phase of the Map-Reduce paradigm.
    It takes a raw JSON line containing a year's worth of data and
    emits (key, value) pairs where:
        - key: year (string)
        - value: maximum temperature for that day (float)

    Args:
        line: A single JSONL line containing daily weather data

    Returns:
        List of (year, temperature) tuples

    Example:
        >>> mapper('{"daily": {"time": ["2020-01-01"], "temperature_2m_max": [25.5]}}')
        [("2020", 25.5)]
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
    temperatures = daily.get("temperature_2m_max", [])

    key_value_pairs: List[Tuple[str, float]] = []

    for date_str, temp in zip(dates, temperatures):
        if temp is None:
            continue

        # Extract year from date string "YYYY-MM-DD"
        year = date_str.split("-")[0]

        try:
            temp_value = float(temp)
        except (TypeError, ValueError):
            continue

        key_value_pairs.append((year, temp_value))

    return key_value_pairs


# =============================================================================
# SHUFFLE PHASE
# =============================================================================


def shuffle_and_group(mapped_pairs: List[Tuple[str, float]]) -> Dict[str, List[float]]:
    """
    Shuffle and group: Organize mapped pairs by key (year).

    This function implements the SHUFFLE phase of Map-Reduce.
    It groups all values (temperatures) by their keys (years),
    preparing the data for the reduce phase.

    In a distributed system, this phase would involve:
    - Partitioning data across nodes
    - Sorting by key
    - Transferring data between nodes (shuffle)

    Args:
        mapped_pairs: List of (year, temperature) tuples from map phase

    Returns:
        Dictionary mapping each year to a list of temperatures

    Example:
        >>> shuffle_and_group([("2020", 25.5), ("2020", 30.0), ("2021", 28.0)])
        {"2020": [25.5, 30.0], "2021": [28.0]}
    """
    grouped: Dict[str, List[float]] = {}

    for year, temperature in mapped_pairs:
        if year not in grouped:
            grouped[year] = []
        grouped[year].append(temperature)

    return grouped


# =============================================================================
# REDUCE PHASE
# =============================================================================


def reducer(year: str, temperatures: List[float]) -> Tuple[str, float]:
    """
    Reduce function: Compute the maximum temperature for a year.

    This function implements the REDUCE phase of Map-Reduce.
    It takes all temperatures for a given year and computes
    the maximum value.

    Args:
        year: The year (key)
        temperatures: List of all temperatures for that year (values)

    Returns:
        Tuple of (year, maximum_temperature)

    Example:
        >>> reducer("2020", [25.5, 30.0, 28.0, 35.2])
        ("2020", 35.2)
    """
    if not temperatures:
        return year, float("nan")

    return year, max(temperatures)


# =============================================================================
# MAP-REDUCE ORCHESTRATION
# =============================================================================


def run_map_reduce() -> List[Tuple[str, float]]:
    """
    Execute the complete Map-Reduce pipeline.

    This function orchestrates the three phases:
    1. MAP: Process each line and emit (year, temp) pairs
    2. SHUFFLE: Group temperatures by year
    3. REDUCE: Compute max temperature per year

    Returns:
        Sorted list of (year, max_temperature) tuples
    """
    print("=" * 60)
    print("Map-Reduce: Yearly Maximum Temperature Computation")
    print("=" * 60)
    print(f"Input: {RAW_DATA_FILE}")
    print(f"Output: {YEARLY_MAX_TEMP_FILE}")
    print("-" * 60)

    # Phase 1: MAP
    print("\n[Phase 1/3] MAP - Extracting (year, temperature) pairs...")
    all_mapped: List[Tuple[str, float]] = []
    line_count = 0

    with open(RAW_DATA_FILE, "r", encoding="utf-8") as file:
        for line in file:
            mapped = mapper(line)
            all_mapped.extend(mapped)
            line_count += 1

    print(f"  ✓ Processed {line_count} input lines")
    print(f"  ✓ Generated {len(all_mapped):,} (key, value) pairs")

    # Phase 2: SHUFFLE
    print("\n[Phase 2/3] SHUFFLE - Grouping by year...")
    grouped = shuffle_and_group(all_mapped)
    print(f"  ✓ Grouped data into {len(grouped)} years")

    # Phase 3: REDUCE
    print("\n[Phase 3/3] REDUCE - Computing maximum per year...")
    results: List[Tuple[str, float]] = []

    for year, temperatures in grouped.items():
        result = reducer(year, temperatures)
        results.append(result)

    # Sort by year
    results.sort(key=lambda x: x[0])
    print(f"  ✓ Computed {len(results)} yearly maximum temperatures")

    return results


def save_results(results: List[Tuple[str, float]]) -> None:
    """
    Save Map-Reduce results to CSV file.

    Args:
        results: List of (year, max_temperature) tuples
    """
    with open(YEARLY_MAX_TEMP_FILE, "w", encoding="utf-8") as file:
        file.write("year,max_temperature\n")
        for year, max_temp in results:
            file.write(f"{year},{max_temp:.1f}\n")

    print(f"\n  ✓ Results saved to: {YEARLY_MAX_TEMP_FILE}")


def print_results_summary(results: List[Tuple[str, float]]) -> None:
    """
    Print a summary of the Map-Reduce results.

    Args:
        results: List of (year, max_temperature) tuples
    """
    print("-" * 60)
    print("Results Summary:")
    print("-" * 60)
    print(f"{'Year':<10} {'Max Temperature (°C)':<20}")
    print("-" * 30)

    for year, max_temp in results:
        print(f"{year:<10} {max_temp:.1f}°C")

    # Find overall hottest year
    hottest_year, hottest_temp = max(results, key=lambda x: x[1])
    coolest_year, coolest_temp = min(results, key=lambda x: x[1])

    print("-" * 60)
    print(f"🔥 Hottest Year: {hottest_year} ({hottest_temp:.1f}°C)")
    print(f"❄️  Coolest Year: {coolest_year} ({coolest_temp:.1f}°C)")
    print("=" * 60)


def main():
    """Main entry point for Map-Reduce processing."""
    results = run_map_reduce()
    save_results(results)
    print_results_summary(results)
    print("✅ Map-Reduce processing complete!")


if __name__ == "__main__":
    main()
