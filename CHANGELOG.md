# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - 2025-01-XX

### Changed

- Restructured Final Report to focus on Map-Reduce as the core project component
- Added detailed code snippets for MAP, SHUFFLE, and REDUCE phases in report
- Simplified dashboard to 5 essential panels (removed redundant heatmaps)
- Cleaned up unused visualization functions from analysis modules

### Removed

- Temperature distribution histogram (redundant with trend analysis)
- Temperature heatmap (consolidated into dashboard)
- Wind heatmap visualization
- Correlation matrix (not essential for distributed processing focus)
- Seasonal boxplot standalone visualization

## [2.0.0] - 2024-12-05

### Added

- **Centralized Configuration** (`config.py`): All paths, constants, and settings in one place
- **Main Pipeline Runner** (`main.py`): Single command to run the entire analysis pipeline
- **Enhanced Visualizations**:
  - Comprehensive analysis dashboard (`00_analysis_dashboard.png`)
  - Decade comparison bar chart
  - Temperature cycle line chart
  - Precipitation bar chart
  - Rainfall polar chart
  - Monthly temperature pattern
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
