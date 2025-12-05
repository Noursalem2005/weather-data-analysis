# Weather Data Analysis - Final Project Report

## Distributed Processing Course

**Location:** Cairo, Egypt
**Analysis Period:** 2000 - 2024 (25 years)

---

## 1. Executive Summary

This report presents a comprehensive analysis of 25 years of weather data from Cairo, Egypt, demonstrating distributed processing concepts through an ETL pipeline and Map-Reduce implementation. The analysis reveals a clear **warming trend of +1.36°C per decade** with 2024 being the hottest year on record at 46.4°C.

### Key Findings

| Metric | Value |
|--------|-------|
| Total Observations | 9,132 daily records |
| Hottest Year | 2024 (46.4°C) |
| Coolest Year | 2006 (40.6°C) |
| Mean Annual Max Temperature | 43.24°C |
| Temperature Trend | +1.36°C per decade |
| Anomalies Detected | 1 (2024) |

---

## 2. Project Objectives

The project focused on:

1. **Gathering raw weather data** (temperature, precipitation, wind speed)
2. **Cleaning and preparing the dataset** using ETL principles
3. **Computing statistical and analytical features** from raw values
4. **Applying Map-Reduce** to compute yearly maximum temperatures
5. **Presenting extracted features** in clear, visual forms
6. **Detecting anomalies** in weather patterns

---

## 3. Methodology

### 3.1 Data Pipeline Architecture

```
EXTRACT → TRANSFORM → LOAD → MAP-REDUCE → ANALYSIS → VISUALIZATION
```

1. **Extract**: Downloaded data from Open-Meteo Archive API
2. **Transform**: Converted JSON to structured CSV format
3. **Load**: Stored processed data for analysis
4. **Map-Reduce**: Computed yearly maximum temperatures
5. **Analysis**: Applied statistical methods for insights
6. **Visualization**: Generated 12 professional charts

### 3.2 Map-Reduce Implementation

The Map-Reduce pattern was implemented to find the **highest temperature of each year**:

- **Map Phase**: Extracted (year, temperature) pairs from each daily record
- **Shuffle Phase**: Grouped temperatures by year
- **Reduce Phase**: Computed maximum temperature for each year

---

## 4. Analysis Results

### 4.1 Comprehensive Dashboard

![Analysis Dashboard](../output/00_analysis_dashboard.png)

*Figure 1: Comprehensive analysis dashboard showing key metrics, trends, and patterns*

---

### 4.2 Yearly Temperature Trend Analysis

![Yearly Temperature Trend](../output/01_yearly_temperature_trend.png)

*Figure 2: 25-year temperature trend with linear regression and anomaly detection*

**Key Observations:**

- Clear warming trend: **+1.36°C per decade**
- Temperature range: 40.6°C to 46.4°C
- 2024 identified as an anomaly (above 1.5 standard deviations)

---

### 4.3 Decade Comparison

![Decade Comparison](../output/03_decade_comparison.png)

*Figure 3: Comparison of average maximum temperatures by decade*

**Decade Progression:**

- 2000s: Cooler baseline period
- 2010s: Significant warming
- 2020s: Continued warming trend with record temperatures

---

### 4.4 Monthly Temperature Patterns

![Monthly Temperature](../output/04_monthly_temperature.png)

*Figure 4: Monthly average temperatures showing seasonal variation*

**Monthly Extremes:**

- Hottest Month: July (37.4°C average max)
- Coldest Month: January (19.4°C average max)
- Temperature Range: 18°C between summer and winter

---

### 4.5 Annual Temperature Cycle

![Temperature Cycle](../output/05_temperature_cycle.png)

*Figure 5: Annual temperature cycle showing the transition between seasons*

---

### 4.6 Rainfall Distribution (Polar Chart)

![Rainfall Polar](../output/06_rainfall_polar.png)

*Figure 6: Monthly rainfall distribution in polar format*

**Precipitation Pattern:**

- Wettest Month: February (0.2mm/day average)
- Driest Month: July (nearly 0mm)
- Cairo exhibits typical Mediterranean/desert climate with winter rainfall

---

### 4.7 Monthly Precipitation

![Precipitation Monthly](../output/07_precipitation_monthly.png)

*Figure 7: Bar chart of monthly precipitation averages*

---

## 5. Yearly Maximum Temperatures (Map-Reduce Output)

| Year | Maximum Temperature (°C) |
|------|-------------------------|
| 2000 | 42.7 |
| 2001 | 42.0 |
| 2002 | 43.9 |
| 2003 | 42.6 |
| 2004 | 42.1 |
| 2005 | 40.8 |
| 2006 | 40.6 |
| 2007 | 42.2 |
| 2008 | 42.2 |
| 2009 | 41.0 |
| 2010 | 45.2 |
| 2011 | 41.2 |
| 2012 | 40.7 |
| 2013 | 45.1 |
| 2014 | 44.6 |
| 2015 | 45.5 |
| 2016 | 45.1 |
| 2017 | 41.4 |
| 2018 | 43.8 |
| 2019 | 44.3 |
| 2020 | 44.3 |
| 2021 | 44.4 |
| 2022 | 44.1 |
| 2023 | 44.7 |
| 2024 | **46.4** (Highest) |

---

## 6. Conclusions

### 6.1 Key Findings

1. **Warming Trend**: Clear evidence of rising temperatures with +1.36°C per decade increase
2. **Record Year**: 2024 recorded the highest temperature (46.4°C) in the 25-year dataset
3. **Seasonal Patterns**: Consistent summer heat waves with July being the hottest month
4. **Anomaly Detection**: 2024 identified as statistically anomalous (exceeds threshold)
5. **Desert Climate**: Minimal precipitation, especially during summer months

### 6.2 Distributed Processing Concepts Demonstrated

- **ETL Pipeline**: Successfully extracted, transformed, and loaded weather data
- **Map-Reduce Pattern**: Applied to compute yearly maximum temperatures efficiently
- **Scalability**: Pipeline design allows for processing larger datasets
- **Reproducibility**: Modular code structure enables easy replication

