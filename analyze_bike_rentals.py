"""Hourly bike-sharing demand analysis.

Put this script beside 03_bike_rental.csv and run:
    python analyze_bike_rentals.py

Dependencies: pandas, numpy, matplotlib
"""
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "03_bike_rental.csv"
OUTPUT_DIR = BASE_DIR / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load and inspect the original file. Work on a copy so raw data is preserved.
raw = pd.read_csv(DATA_FILE)
print("Original shape:", raw.shape)
print("Original data types:\n", raw.dtypes)
print("Missing values:\n", raw.isna().sum())

df = raw.copy()
# UCI data uses dteday + hr; combine them into a real hourly timestamp.
df["DateTime"] = pd.to_datetime(df["dteday"], errors="coerce") + pd.to_timedelta(df["hr"], unit="h")
if df["DateTime"].isna().any():
    raise ValueError("Some date/time values could not be parsed. Check dteday and hr.")
df["date"] = df["DateTime"].dt.date
df["month"] = df["DateTime"].dt.month
df["hour"] = df["DateTime"].dt.hour

# Official UCI category codes: 1 winter, 2 spring, 3 summer, 4 fall.
df["season_name"] = df["season"].map({1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"})
df["weather_name"] = df["weathersit"].map({
    1: "Clear / partly cloudy", 2: "Mist / cloudy",
    3: "Light rain or snow", 4: "Heavy rain or snow"
})
# workingday=0 includes weekends and holidays; dataset does not identify them separately here.
df["day_type"] = np.where(df["workingday"].eq(1), "Weekday", "Weekend / holiday")

# Report and handle humidity missing values. Median imputation is a safe fallback;
# this supplied dataset currently has no missing humidity readings.
humidity_missing = int(df["hum"].isna().sum())
if humidity_missing:
    df["hum"] = df["hum"].fillna(df["hum"].median())

rentals = df["cnt"]
q1, q3 = rentals.quantile([0.25, 0.75])
iqr = q3 - q1
lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr
high_outliers = df.loc[rentals > upper_bound].sort_values("cnt", ascending=False)

# Required summaries (mean compares typical hourly demand; sum is total volume).
hourly = df.groupby("hour")["cnt"].agg(mean_rentals="mean", total_rentals="sum", records="count").reset_index()
seasonal = df.groupby("season_name")["cnt"].agg(mean_rentals="mean", total_rentals="sum", records="count").reset_index()
daytype = df.groupby("day_type")["cnt"].agg(mean_rentals="mean", total_rentals="sum", records="count").reset_index()
weather = df.groupby("weather_name")["cnt"].agg(mean_rentals="mean", total_rentals="sum", records="count").reset_index()
season_weather = df.groupby(["season_name", "weather_name"])["cnt"].agg(mean_rentals="mean", total_rentals="sum", records="count").reset_index()
daily = df.groupby("date", as_index=False)["cnt"].sum().rename(columns={"cnt": "total_rentals"}).sort_values("total_rentals", ascending=False)
top10 = df.nlargest(10, "cnt")[["DateTime", "cnt", "season_name", "weather_name", "temp", "hum"]]

# NumPy calculations requested by the assignment. Temperature is normalized in the source.
average_temperature_normalized = float(np.mean(df["temp"].to_numpy()))
total_rentals_numpy = int(np.sum(df["cnt"].to_numpy()))
temperature_rental_correlation = float(df["temp"].corr(df["cnt"]))

# Save a clean analysis copy and all main summary tables for review/reuse.
df.to_csv(OUTPUT_DIR / "cleaned_bike_rentals.csv", index=False)
for name, table in {
    "hourly_summary": hourly, "seasonal_comparison": seasonal,
    "weekday_weekend_comparison": daytype, "weather_comparison": weather,
    "season_weather_summary": season_weather, "daily_demand_ranking": daily,
    "top_10_hourly_records": top10,
}.items():
    table.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)
high_outliers.to_csv(OUTPUT_DIR / "high_demand_iqr_records.csv", index=False)

# Optional presentation charts. The data tables are generated even if matplotlib
# is not installed; install matplotlib to also save PNG charts.
try:
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.plot(hourly["hour"], hourly["mean_rentals"], marker="o", color="#176B87")
    plt.xticks(range(24)); plt.xlabel("Hour of day"); plt.ylabel("Average rentals per hour")
    plt.title("Average Bike Rentals by Hour"); plt.grid(alpha=.25); plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "hourly_demand.png", dpi=180); plt.close()
    plt.figure(figsize=(8, 5))
    ordered = seasonal.set_index("season_name").reindex(["Winter", "Spring", "Summer", "Fall"])
    plt.bar(ordered.index, ordered["mean_rentals"], color=["#7CB7D3", "#73B77B", "#F2A541", "#C96A57"])
    plt.xlabel("Season"); plt.ylabel("Average rentals per hour"); plt.title("Average Bike Rentals by Season")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "seasonal_demand.png", dpi=180); plt.close()
    plt.figure(figsize=(8, 5))
    plt.scatter(df["temp"], df["cnt"], alpha=.18, s=10, color="#176B87")
    plt.xlabel("Normalized temperature (source scale)"); plt.ylabel("Rentals per hour")
    plt.title(f"Temperature and Rentals (r = {temperature_rental_correlation:.3f})")
    plt.tight_layout(); plt.savefig(OUTPUT_DIR / "temperature_vs_rentals.png", dpi=180); plt.close()
except ImportError:
    print("Matplotlib is not installed; skipped optional PNG charts.")

# Print key results clearly in the terminal.
print(f"\nRecords: {len(df):,}; rental total: {rentals.sum():,}; mean per record: {rentals.mean():.2f}")
print(f"Missing humidity: {humidity_missing}; average normalized temperature (NumPy): {average_temperature_normalized:.4f}")
print(f"Rental total (NumPy): {total_rentals_numpy:,}; temperature/rentals correlation: {temperature_rental_correlation:.3f}")
print(f"IQR bounds: [{lower_bound:.1f}, {upper_bound:.1f}]; high records: {len(high_outliers)}")
print("\nTop 10 hourly records:\n", top10.to_string(index=False))
print("\nSeasonal average rentals:\n", seasonal.to_string(index=False))
print("\nHourly summary:\n", hourly.to_string(index=False))
print(f"\nSaved cleaned data, summaries, and charts in: {OUTPUT_DIR}")
