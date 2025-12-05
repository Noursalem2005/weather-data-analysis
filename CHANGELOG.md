# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2024-12-05

### Added

- **Centralized Configuration** (`config.py`): All paths, constants, and settings in one place
- **Main Pipeline Runner** (`main.py`): Single command to run the entire analysis pipeline
- **Enhanced Visualizations**:
  - Comprehensive analysis dashboard (`00_analysis_dashboard.png`)
  - Temperature distribution with histogram and box plot
  - Decade comparison bar chart
  - Temperature cycle line chart
  - Precipitation bar chart
  - Temperature climate heatmap
  - Seasonal comparison box plots
  - Correlation matrix heatmap
- **Improved Documentation**:
  - Comprehensive README with badges and diagrams
  - Final project report with all visualizations
  - Proper docstrings in all modules

### Changed

- Restructured all scripts with proper documentation and type hints
- Standardized file naming convention (removed typos)
- All outputs now save to `output/` directory with numbered prefixes
- Improved Map-Reduce implementation with clear phase separation
- Enhanced statistical analysis with more metrics

### Removed

- Old duplicate files with naming issues (`dawnload_data.py`, `monthly_analysiss.py`)
- Redundant code and comments

## [1.0.0] - 2024-11-XX

### Added

- Initial project structure
- Basic data download from Open-Meteo API
- Simple Map-Reduce for yearly max temperature
- Basic monthly and yearly analysis
- Initial visualizations
