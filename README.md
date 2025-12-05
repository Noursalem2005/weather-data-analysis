# 🌤️ Weather Data Analysis - Distributed Processing Project

> A comprehensive weather data analysis pipeline demonstrating distributed processing concepts including ETL pipelines, Map-Reduce patterns, and statistical analysis.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-success.svg)]()

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Pipeline Architecture](#-pipeline-architecture)
- [Analysis Outputs](#-analysis-outputs)
- [Data Source](#-data-source)
- [Authors](#-authors)

---

## 🎯 Project Overview

This project analyzes **25 years of historical weather data** (2000-2024) from Cairo, Egypt to demonstrate key concepts in distributed data processing:

### Objectives

1. **Data Collection**: Gather raw weather data from Open-Meteo API
2. **Data Cleaning**: Transform and prepare the dataset
3. **Feature Extraction**: Compute statistical and analytical features
4. **Map-Reduce Processing**: Apply distributed processing patterns
5. **Visualization**: Present insights in clear, interpretable forms
6. **Anomaly Detection**: Identify unusual weather patterns

### Key Metrics Analyzed

| Metric | Description | Unit |
|--------|-------------|------|
| Temperature (Max) | Daily maximum temperature | °C |
| Temperature (Min) | Daily minimum temperature | °C |
| Precipitation | Daily rainfall/precipitation | mm |
| Wind Speed | Maximum daily wind speed | km/h |

---

## ✨ Features

### 🔄 ETL Pipeline

- **Extract**: Download weather data from Open-Meteo Archive API
- **Transform**: Convert raw JSON to structured CSV format
- **Load**: Store processed data for analysis

### 🗺️ Map-Reduce Implementation

- Demonstrates the Map-Reduce paradigm for computing yearly maximum temperatures
- **Map Phase**: Extract (year, temperature) key-value pairs
- **Shuffle Phase**: Group data by year
- **Reduce Phase**: Compute maximum for each year

### 📊 Statistical Analysis

- Trend analysis using linear regression
- Anomaly detection using standard deviation thresholds
- Seasonal pattern analysis
- Correlation analysis between weather variables

### 📈 Visualizations (12+ Charts)

- Yearly temperature trends with anomaly markers
- Temperature distribution histograms and box plots
- Monthly pattern analysis
- Seasonal comparisons
- Climate heatmaps (temperature and wind)
- Correlation matrices
- Polar rainfall charts
- Comprehensive analysis dashboard

---

## 📁 Project Structure

```
weather-data-analysis/
├── 📂 src/                          # Source code
│   ├── config.py                    # Configuration and constants
│   ├── main.py                      # Main pipeline runner
│   ├── download_data.py             # Data collection (Extract)
│   ├── build_dataset.py             # Data transformation (Transform)
│   ├── map_reduce_analysis.py       # Map-Reduce implementation
│   ├── yearly_analysis.py           # Yearly statistics & visualizations
│   ├── monthly_analysis.py          # Monthly patterns & visualizations
│   └── create_dashboard.py          # Comprehensive dashboard
│
├── 📂 data/                         # Data files
│   ├── weather_raw.jsonl            # Raw API responses (JSONL format)
│   ├── daily_weather.csv            # Processed daily observations
│   └── yearly_max_temp.csv          # Aggregated yearly data
│
├── 📂 output/                       # Generated visualizations
│   ├── 00_analysis_dashboard.png    # Complete analysis dashboard
│   ├── 01_yearly_temperature_trend.png
│   ├── 02_temperature_distribution.png
│   ├── 03_decade_comparison.png
│   ├── 04_monthly_temperature.png
│   ├── 05_temperature_cycle.png
│   ├── 06_rainfall_polar.png
│   ├── 07_precipitation_monthly.png
│   ├── 08_wind_heatmap.png
│   ├── 09_temperature_heatmap.png
│   ├── 10_seasonal_comparison.png
│   └── 11_correlation_matrix.png
│
├── 📂 docs/                         # Documentation
│   └── FINAL_REPORT.md              # Final project report
│
├── README.md                        # This file
├── CHANGELOG.md                     # Version history
└── .gitignore                       # Git ignore rules
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/weather-data-analysis.git
   cd weather-data-analysis
   ```

2. **Install dependencies**

   ```bash
   pip install pandas numpy matplotlib seaborn requests
   ```

3. **Verify installation**

   ```bash
   python --version  # Should be 3.8+
   ```

---

## 💻 Usage

### Run Complete Pipeline

Execute the entire analysis pipeline with a single command:

```bash
cd src
python main.py
```

This will:

1. Download weather data (if not cached)
2. Build the daily dataset
3. Run Map-Reduce analysis
4. Generate yearly analysis
5. Generate monthly analysis
6. Create the summary dashboard

### Skip Data Download

If you already have the data, skip the download step:

```bash
python main.py --skip-download
```

### Run Individual Scripts

You can also run each stage separately:

```bash
# Step 1: Download raw data
python download_data.py

# Step 2: Build daily dataset
python build_dataset.py

# Step 3: Map-Reduce aggregation
python map_reduce_analysis.py

# Step 4: Yearly analysis
python yearly_analysis.py

# Step 5: Monthly analysis
python monthly_analysis.py

# Step 6: Create dashboard
python create_dashboard.py
```

---

## 🔧 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATA PROCESSING PIPELINE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   EXTRACT    │───▶│  TRANSFORM   │───▶│    LOAD      │               │
│  │              │    │              │    │              │               │
│  │ Open-Meteo   │    │ JSON → CSV   │    │ daily_       │               │
│  │ API          │    │ Parse &      │    │ weather.csv  │               │
│  │              │    │ Clean        │    │              │               │
│  └──────────────┘    └──────────────┘    └──────────────┘               │
│         │                                        │                       │
│         │            ┌───────────────────────────┘                       │
│         │            │                                                   │
│         ▼            ▼                                                   │
│  ┌───────────────────────────────────────────────────────────┐          │
│  │                     MAP-REDUCE                             │          │
│  ├───────────────────────────────────────────────────────────┤          │
│  │  ┌─────────┐    ┌─────────────┐    ┌─────────────┐        │          │
│  │  │   MAP   │───▶│   SHUFFLE   │───▶│   REDUCE    │        │          │
│  │  │         │    │             │    │             │        │          │
│  │  │(year,   │    │ Group by    │    │ max(temps)  │        │          │
│  │  │ temp)   │    │ year        │    │ per year    │        │          │
│  │  └─────────┘    └─────────────┘    └─────────────┘        │          │
│  └───────────────────────────────────────────────────────────┘          │
│                              │                                           │
│                              ▼                                           │
│  ┌───────────────────────────────────────────────────────────┐          │
│  │                      ANALYSIS                              │          │
│  ├───────────────────────────────────────────────────────────┤          │
│  │  • Statistical Summary    • Trend Detection               │          │
│  │  • Anomaly Detection      • Seasonal Patterns             │          │
│  │  • Correlation Analysis   • Visualizations                │          │
│  └───────────────────────────────────────────────────────────┘          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Analysis Outputs

### Dashboard Overview

The main dashboard (`00_analysis_dashboard.png`) provides a complete overview:

- Yearly temperature trends with anomaly detection
- Key statistics summary
- Monthly temperature patterns
- Seasonal comparisons
- Climate heatmaps

### Individual Visualizations

| # | Visualization | Description |
|---|---------------|-------------|
| 01 | Yearly Temperature Trend | 25-year temperature trend with regression line and anomalies |
| 02 | Temperature Distribution | Histogram with KDE and box plot |
| 03 | Decade Comparison | Bar chart comparing average temperatures by decade |
| 04 | Monthly Temperature | Side-by-side comparison of max/min temperatures |
| 05 | Temperature Cycle | Line chart showing annual temperature cycle |
| 06 | Rainfall Polar | Polar/radar chart of monthly rainfall distribution |
| 07 | Precipitation Monthly | Bar chart of monthly precipitation averages |
| 08 | Wind Heatmap | Year × Month heatmap of wind speeds |
| 09 | Temperature Heatmap | Year × Month heatmap of temperatures |
| 10 | Seasonal Comparison | Box plots comparing seasons |
| 11 | Correlation Matrix | Correlation between weather variables |

---

## 🌐 Data Source

**Open-Meteo Historical Weather API**

- URL: <https://open-meteo.com/>
- Location: Cairo, Egypt (30.0444°N, 31.2357°E)
- Time Range: January 1, 2000 – December 31, 2024
- Resolution: Daily observations
- Variables: Temperature (max/min), Precipitation, Wind Speed

---

## 👥 Authors

**Distributed Processing Course Project**

- Team Members: [Add team member names]
- Course: Distributed Processing
- Institution: [Add institution name]
- Date: 2024

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ for Distributed Processing Course**

</div>
