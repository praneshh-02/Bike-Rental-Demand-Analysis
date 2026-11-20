# Bike Rental Demand Analysis

**Industry:** Mobility / Smart City

**Goal:** Analyze hourly bike-sharing demand by time, season, and weather to support fleet availability planning.

## Project Files

- `03_bike_rental.csv` — Hourly source data (UCI Bike Sharing Dataset, `hour.csv` renamed for this assignment).
- `analyze_bike_rentals.py` — Complete, commented analysis script.
- `report.md` — Assignment report with methods, findings, and recommendations.
- `results/` — Cleaned data and generated summary CSV files (created when the script runs).

## Run the Project

Install Python 3 and the required packages:

```bash
python -m pip install pandas numpy
```

From this folder, run:

```bash
python analyze_bike_rentals.py
```

The script writes the cleaned dataset and summary tables to `results/`.

PNG charts are optional. Install Matplotlib to generate them:

```bash
python -m pip install matplotlib
```

## Important Data Notes

- The CSV has 17,379 hourly rows.
- The source uses `dteday` and `hr` for time and `cnt` for total hourly rentals.
- Season codes: 1 Winter, 2 Spring, 3 Summer, 4 Fall.
- `temp` is normalized, not recorded directly in degrees Celsius.
- `workingday` is 1 for working days and 0 for weekends or holidays. The comparison groups weekends and holidays together.
- The supplied dataset contains no missing humidity readings, so no values are imputed.

**Dataset Source:** [UCI Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike-sharing-dataset)

**Dataset License:** CC BY 4.0.

## GitHub

Repository link: Add your GitHub repository URL here.

## SRS Reminder

The assignment reminder asks for an "SRS document" but does not specify its meaning, structure, or template. Confirm the expected SRS format with your instructor before submitting a document under that name.
