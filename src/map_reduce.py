import json
from typing import List, Tuple, Dict

RAW_FILE = "./data/weather_raw.jsonl"
OUTPUT_FILE = "yearly_max_temp.csv"

def mapper(line: str) -> List[Tuple[str, float]]:
    """Map step: return list of (year, temperature) for a JSONL line."""
    line = line.strip()
    if not line:
        return []

    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return []

    daily = data.get("daily", {})
    dates = daily.get("time", [])
    temps = daily.get("temperature_2m_max", [])

    results: List[Tuple[str, float]] = []
    for date_str, temp in zip(dates, temps):
        if temp is None:
            continue
        # "2000-01-01" -> "2000"
        year = date_str.split("-")[0]
        try:
            temp_val = float(temp)
        except (TypeError, ValueError):
            continue
        results.append((year, temp_val))

    return results

def shuffle_and_group(mapped_values: List[Tuple[str, float]]) -> Dict[str, List[float]]:
    """Group mapped (year, temp) tuples by year."""
    grouped: Dict[str, List[float]] = {}
    for year, temp in mapped_values:
        if year not in grouped:
            grouped[year] = []
        grouped[year].append(temp)
    return grouped

def reducer(year: str, temps: List[float]) -> Tuple[str, float]:
    """Reduce step: return (year, max_temp)."""
    if not temps:
        return year, float("nan")
    return year, max(temps)


def main():
    all_mapped: List[Tuple[str, float]] = []
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        for line in f:
            mapped = mapper(line)
            all_mapped.extend(mapped)

    # 2) Shuffle and Group by year
    grouped = shuffle_and_group(all_mapped)

    # 3) Reduce to get max temperature per year
    results: List[Tuple[str, float]] = []
    for year, temps in grouped.items():
        year_result = reducer(year, temps)
        results.append(year_result)
        
    # 4) Sort results by year
    results.sort(key=lambda x: x[0])
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("year,max_temperature\n")
        for year, max_temp in results:
            out.write(f"{year},{max_temp}\n")
            
if __name__ == "__main__":
    main()
