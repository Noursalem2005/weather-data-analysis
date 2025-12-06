"""
Configuration module for Weather Data Analysis Project.

This module contains all shared constants and paths used across the project.
Centralizing configuration makes the project easier to maintain and modify.
"""

from pathlib import Path

# =============================================================================
# PROJECT PATHS
# =============================================================================

# Base directory (project root)
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# DATA FILES
# =============================================================================

# Input files
RAW_DATA_FILE = DATA_DIR / "weather_raw.jsonl"
DAILY_DATA_FILE = DATA_DIR / "daily_weather.csv"
YEARLY_MAX_TEMP_FILE = DATA_DIR / "yearly_max_temp.csv"

# =============================================================================
# LOCATION SETTINGS (Cairo, Egypt)
# =============================================================================

LATITUDE = 30.0444
LONGITUDE = 31.2357
TIMEZONE = "Africa/Cairo"
LOCATION_NAME = "Cairo, Egypt"

# =============================================================================
# DATA COLLECTION SETTINGS
# =============================================================================

START_YEAR = 2000
END_YEAR = 2024

# Weather metrics to collect from API
WEATHER_METRICS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "windspeed_10m_max",
]

# =============================================================================
# VISUALIZATION SETTINGS
# =============================================================================

# Figure sizes
FIGURE_SIZE_STANDARD = (12, 6)
FIGURE_SIZE_WIDE = (14, 6)
FIGURE_SIZE_SQUARE = (10, 10)
FIGURE_SIZE_HEATMAP = (14, 8)

# DPI for saved figures
FIGURE_DPI = 300

# Color palettes
COLOR_PRIMARY = "#1f77b4"
COLOR_SECONDARY = "#ff7f0e"
COLOR_ACCENT = "#d62728"
COLOR_SUCCESS = "#2ca02c"

# Month names mapping
MONTH_NAMES = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

MONTH_FULL_NAMES = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

# Season definitions (for Northern Hemisphere)
SEASONS = {
    "Winter": [12, 1, 2],
    "Spring": [3, 4, 5],
    "Summer": [6, 7, 8],
    "Autumn": [9, 10, 11],
}

# =============================================================================
# ANALYSIS SETTINGS
# =============================================================================

# Anomaly detection threshold (standard deviations)
ANOMALY_THRESHOLD_STD = 1.5
