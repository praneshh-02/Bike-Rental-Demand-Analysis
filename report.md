# Bike Rental Demand Analysis for Fleet Planning

**Industry:** Mobility / Smart City  
**Dataset:** UCI Bike Sharing Dataset, hourly file (`hour.csv`, renamed `03_bike_rental.csv`)  
**Coverage:** 17,379 hourly records from 2011–2012

## 1. Objective

Study how bike rentals vary by hour, season, day type, weather, and temperature. Use the observed patterns to suggest practical fleet planning actions.

## 2. Data and method

The source file contains 17 columns. `dteday` and `hr` were combined into a pandas `DateTime`; date, month, and hour were extracted. The original file is kept unchanged and a cleaned analysis copy is saved separately.

The dataset includes `cnt` (total rentals), `season`, `weathersit`, `temp`, `hum`, and `workingday`. Official season codes are 1 Winter, 2 Spring, 3 Summer, and 4 Fall. Weather codes are grouped as clear/partly cloudy, mist/cloudy, light rain or snow, and heavy rain or snow. `workingday=0` includes weekends and holidays, so those are compared together.

All humidity readings are present, so no imputation was needed. Temperature is normalized in the source (not in Celsius); its mean is reported in normalized units. Seasonal and weather comparisons use average rentals per hourly record so groups with different row counts can be compared fairly. IQR outliers are records above Q3 + 1.5×IQR.

## 3. Key results

- **Total rentals:** 3,292,679 across 17,379 hourly records.
- **Average rentals:** 189.46 per recorded hour.
- **Humidity:** 0 missing readings.
- **Temperature (NumPy mean):** 0.4970 on the source's normalized scale.
- **Temperature/rentals correlation:** 0.405, a moderate positive association in this dataset. This does not show that temperature alone causes demand to change.
- **High-demand IQR records:** Q1 = 40, Q3 = 281, IQR = 241, upper bound = 642.5 rentals/hour; 505 records exceed the upper bound. These are high observations, not automatically data errors.

### Average rentals by season

| Season | Average rentals/hour | Total rentals | Records |
|---|---:|---:|---:|
| Winter | 111.11 | 471,348 | 4,242 |
| Spring | 208.34 | 918,589 | 4,409 |
| Summer | 236.02 | 1,061,129 | 4,496 |
| Fall | 198.87 | 841,613 | 4,232 |

Summer has the highest average and winter the lowest in this dataset.

### Average rentals by day type

| Day type | Average rentals/hour | Total rentals | Records |
|---|---:|---:|---:|
| Weekday (`workingday=1`) | 193.21 | 2,292,410 | 11,865 |
| Weekend / holiday (`workingday=0`) | 181.41 | 1,000,269 | 5,514 |

The source flag combines weekend and holiday observations; this analysis cannot separate the two.

### Average rentals by weather

| Weather group | Average rentals/hour | Total rentals | Records |
|---|---:|---:|---:|
| Clear / partly cloudy | 204.87 | 2,338,173 | 11,413 |
| Mist / cloudy | 175.17 | 795,952 | 4,544 |
| Light rain or snow | 111.58 | 158,331 | 1,419 |
| Heavy rain or snow | 74.33 | 223 | 3 |

Only three heavy-weather records occur, so that average is based on very little data and should not be treated as a precise forecast.

### Hourly demand pattern

| Hour | Average rentals | Hour | Average rentals |
|---:|---:|---:|---:|
| 00 | 53.90 | 12 | 253.32 |
| 01 | 33.38 | 13 | 253.66 |
| 02 | 22.87 | 14 | 240.95 |
| 03 | 11.73 | 15 | 251.23 |
| 04 | 6.35 | 16 | 311.98 |
| 05 | 19.89 | 17 | **461.45** |
| 06 | 76.04 | 18 | **425.51** |
| 07 | 212.06 | 19 | 311.52 |
| 08 | **359.01** | 20 | 226.03 |
| 09 | 219.31 | 21 | 172.31 |
| 10 | 173.67 | 22 | 131.34 |
| 11 | 208.14 | 23 | 87.83 |

The strongest average is at 5 PM; 6 PM and 8 AM are also prominent. The very low early-morning averages identify a useful window for repositioning and maintenance, subject to operational needs.

### Ten highest-demand hourly records

| Date and hour | Rentals | Season | Weather |
|---|---:|---|---|
| 2012-09-12 18:00 | 977 | Summer | Clear / partly cloudy |
| 2012-09-20 17:00 | 976 | Summer | Clear / partly cloudy |
| 2012-09-11 17:00 | 970 | Summer | Clear / partly cloudy |
| 2012-09-10 18:00 | 968 | Summer | Clear / partly cloudy |
| 2012-09-25 17:00 | 967 | Fall | Clear / partly cloudy |
| 2012-10-24 17:00 | 963 | Fall | Clear / partly cloudy |
| 2012-03-23 17:00 | 957 | Spring | Mist / cloudy |
| 2012-09-26 17:00 | 953 | Fall | Clear / partly cloudy |
| 2012-10-10 17:00 | 948 | Fall | Clear / partly cloudy |
| 2012-10-16 17:00 | 943 | Fall | Clear / partly cloudy |

### Season and weather summary

Average rentals per hour by group:

| Season | Clear / partly cloudy | Mist / cloudy | Light rain or snow | Heavy rain or snow |
|---|---:|---:|---:|---:|
| Winter | 122.06 | 103.07 | 58.65 | 74.33* |
| Spring | 232.41 | 181.26 | 115.18 | — |
| Summer | 244.49 | 224.85 | 171.96 | — |
| Fall | 209.46 | 201.48 | 116.45 | — |

`*` Only three heavy-weather rows, all in the winter group. Dashes mean no records for that combination.

### Highest-demand days

| Date | Total rentals |
|---|---:|
| 2012-09-15 | 8,714 |
| 2012-09-29 | 8,555 |
| 2012-09-22 | 8,395 |
| 2012-03-23 | 8,362 |
| 2012-05-19 | 8,294 |

## 4. Operational recommendations

1. **Stage additional bikes before the evening commute.** Average demand peaks at 5–6 PM (461 and 426 rentals/hour). Rebalance stations before this period and monitor stockouts at high-demand locations.
2. **Protect the morning peak.** Demand is also high around 8 AM (359 rentals/hour). Complete overnight charging/checks and position bikes before the morning rush.
3. **Use seasonal capacity planning.** Summer averages 236 rentals/hour versus 111 in winter. Maintain a larger active fleet and more frequent rebalancing in warmer months; schedule deeper maintenance during lower-demand winter periods while keeping adequate service coverage.
4. **Adjust dispatch using weather forecasts.** Average demand is lower in rain/snow categories than clear weather. Use weather forecasts to reduce discretionary redistribution on low-demand days, but keep minimum availability and safety/service standards.
5. **Treat peaks as planning signals and validate locally.** The IQR rule flags 505 high-demand hours, many plausibly reflecting commute or seasonal peaks. Use station-level live data and repeat observations before permanently changing fleet size; the heavy-weather group has only three records.

## 5. Files and reproducibility

Run `python analyze_bike_rentals.py` from this folder. The script creates `results/cleaned_bike_rentals.csv` and CSV summaries for hourly, seasonal, weekday/weekend-holiday, weather, season-weather, daily ranking, top ten, and high-IQR records. It also creates PNG charts when Matplotlib is installed.

**Source:** [UCI Machine Learning Repository — Bike Sharing Dataset](https://archive.ics.uci.edu/dataset/275/bike-sharing-dataset), hourly Capital Bikeshare records for 2011–2012, CC BY 4.0.

**Submission note:** The assignment reminder mentions an SRS but provides no required definition or template. Confirm the expected SRS format with the instructor before preparing that separate deliverable.
