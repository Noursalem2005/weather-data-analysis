# Weather Data Analysis – Distributed Processing

A Python-based weather data analysis project that demonstrates data pipeline processing (download → transform → analyze) using map-reduce concepts and statistical analysis.

## Project Overview

This project analyzes historical weather data from Cairo (2000–2024) to:
- Download raw weather data from the Open-Meteo API
- Transform raw JSON into structured CSV datasets
- Apply map-reduce aggregation to compute yearly statistics
- Generate analysis reports with visualizations (trends, anomalies, monthly patterns)

## Folder Structure

```
weather-data-analysis/
├── src/                          # Python scripts
│   ├── download_weather.py       # Download raw weather data
│   ├── build_daily_dataset.py    # Transform JSON → daily CSV
│   ├── map_reduce_max_temp.py    # Aggregate to yearly max temps
│   ├── analyze_and_plot.py       # Yearly statistics & plots
│   ├── monthly_analysis.py       # Monthly patterns & visualizations
│   └── trend_and_anomalies.py    # Trend analysis & anomaly detection
├── data/                         # Input/intermediate data
│   ├── weather_raw.jsonl         # Raw API responses
│   ├── daily_weather.csv         # Processed daily data
│   └── yearly_max_temp.csv       # Aggregated yearly data
├── outputs/                      # Generated visualizations
│   ├── yearly_max_temp.png
│   ├── monthly_temperature.png
│   ├── monthly_rainfall.png
│   ├── monthly_wind.png
│   ├── rainfall_polar_plot.png
│   ├── wind_heatmap.png
│   └── yearly_max_temp_trend_anomalies.png
└── README.md
```

## Installation

### Requirements
- Python 3.8+
- pandas, matplotlib, numpy, requests

### Setup

```bash
pip install pandas matplotlib numpy requests
```

## Usage

Run scripts in order to build the complete data pipeline:

```bash
# 1. Download raw weather data (2000–2024)
python src/download_weather.py

# 2. Build daily dataset from raw JSON
python src/build_daily_dataset.py

# 3. Compute yearly max temperatures (map-reduce)
python src/map_reduce_max_temp.py

# 4. Analyze yearly trends and anomalies
python src/analyze_and_plot.py
python src/trend_and_anomalies.py

# 5. Generate monthly analysis & visualizations
python src/monthly_analysis.py
```

## Key Features

- **Data Pipeline:** Download → Transform → Aggregate → Analyze
- **Map-Reduce Pattern:** Demonstrates distributed processing concepts
- **Statistical Analysis:** Trend detection, anomaly identification, monthly patterns
- **Visualizations:** Line plots, bar charts, polar plots, heatmaps
- **Clean Code:** Organized structure with minimal comments for clarity

## Data Source

Weather data retrieved from [Open-Meteo Historical API](https://open-meteo.com/)
- Location: Cairo, Egypt (30.0444°N, 31.2357°E)
- Time Range: 2000–2024
- Metrics: Max/min temperature, precipitation, wind speed

## Output

The project generates:
- CSV files with processed data in `data/`
- PNG visualizations in `outputs/`

### Example Outputs

- **Yearly analysis:** Temperature trends over 24 years with anomaly detection
- **Monthly analysis:** Average patterns by month including rainfall and wind speed
- **Visualizations:** Polar plots for rainfall distribution, heatmaps for wind speed trends

## Authors

- Team members (Group project - System Analysis & Design)

## License

MIT

---

**Note:** This project is part of a System Analysis & Design assignment demonstrating data processing pipelines and statistical analysis techniques.
