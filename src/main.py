"""
Weather Data Analysis - Main Pipeline Runner
=============================================

This is the main entry point for the complete weather data analysis
pipeline. It orchestrates all processing stages in the correct order.

Pipeline Stages:
    1. Download: Fetch raw weather data from Open-Meteo API
    2. Transform: Build structured daily dataset from raw JSON
    3. Aggregate: Apply Map-Reduce to compute yearly statistics
    4. Analyze: Generate yearly and monthly analysis with visualizations
    5. Dashboard: Create comprehensive summary visualization

Usage:
    python main.py              # Run complete pipeline
    python main.py --skip-download  # Skip download (use existing data)

Note: Requires internet connection for data download stage.
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import DATA_DIR, OUTPUT_DIR, RAW_DATA_FILE


def print_header():
    """Print the pipeline header."""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🌤️  WEATHER DATA ANALYSIS PIPELINE".center(68) + "║")
    print("║" + "  Distributed Processing Project".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")


def run_stage(stage_name: str, module_name: str):
    """
    Run a pipeline stage with timing and status reporting.

    Args:
        stage_name: Human-readable stage name
        module_name: Python module to import and run
    """
    print(f"\n{'─' * 70}")
    print(f"📌 STAGE: {stage_name}")
    print(f"{'─' * 70}\n")

    start_time = time.time()

    try:
        # Dynamic import and run
        module = __import__(module_name)
        module.main()

        elapsed = time.time() - start_time
        print(f"\n⏱️  Stage completed in {elapsed:.2f} seconds")
        return True

    except Exception as e:
        print(f"\n❌ Error in {stage_name}: {e}")
        return False


def main():
    """Run the complete analysis pipeline."""
    print_header()

    # Parse command line arguments
    skip_download = "--skip-download" in sys.argv

    if skip_download:
        print("ℹ️  Skipping download stage (using existing data)\n")

    # Check if data exists when skipping download
    if skip_download and not RAW_DATA_FILE.exists():
        print(f"❌ Error: Raw data file not found: {RAW_DATA_FILE}")
        print("   Please run without --skip-download to fetch data first.")
        return 1

    # Define pipeline stages
    stages = []

    if not skip_download:
        stages.append(("1. Data Download", "download_data"))

    stages.extend(
        [
            ("2. Build Daily Dataset", "build_dataset"),
            ("3. Map-Reduce Analysis", "map_reduce_analysis"),
            ("4. Yearly Analysis", "yearly_analysis"),
            ("5. Monthly Analysis", "monthly_analysis"),
            ("6. Create Dashboard", "create_dashboard"),
        ]
    )

    # Run all stages
    total_start = time.time()
    successful = 0
    failed = 0

    for stage_name, module_name in stages:
        if run_stage(stage_name, module_name):
            successful += 1
        else:
            failed += 1

    # Print summary
    total_elapsed = time.time() - total_start

    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + "  PIPELINE COMPLETE".center(68) + "║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  ✅ Successful stages: {successful:<43}║")
    if failed > 0:
        print(f"║  ❌ Failed stages: {failed:<47}║")
    print(f"║  ⏱️  Total time: {total_elapsed:.2f} seconds{' ' * 36}║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  📁 Data directory: {str(DATA_DIR)[:45]:<46}║")
    print(f"║  📁 Output directory: {str(OUTPUT_DIR)[:43]:<44}║")
    print("╚" + "═" * 68 + "╝")
    print("\n")

    if failed > 0:
        print("⚠️  Some stages failed. Check the output above for details.\n")
        return 1

    print("🎉 All visualizations have been generated in the output folder!\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
