# Project: Stock Prediction CO5115

## Overview
This project focuses on stock price prediction using historical price and volume data. The implementation is based on the `Sample Assignment.ipynb` template.

## Data
- **Location:** `btl/sample_data/`
- **Format:** `.npy` files containing daily stock data.
- **Columns:** `['date', 'opn', 'cls', 'low', 'high', 'nsh', 'vol', 'adj']`

## Key Implementations
- **SMA Function:** A custom `sma(data, n)` function using `pandas` rolling mean with `min_periods=1` to handle initial data points.
- **Interactive Visualization:** Powered by `plotly`, featuring:
    - Close Price vs. 5-day and 20-day SMAs.
    - **Trend Cloud:** Fills the area between SMAs (Green for Up Trend, Red for Down Trend).
    - **Volume Subplot:** Synced bar chart for trading volume.
    - **Anomaly Detection:** Visual markers for price movements that contradict the SMA trend rules.
- **SMA Gap Momentum Strategy:** 
    - **Strong Downtrend:** SMA5 < SMA20 and gap widening.
    - **Signal Uptrend:** SMA5 < SMA20 but gap narrowing (Recovery signal).
    - **Anomalies:** Identified when price action contradicts these momentum signals.

## Environment & Conventions
- **Python:** Use the provided `.venv` virtual environment.
- **Library Requirements:** `numpy`, `pandas`, `matplotlib`, `plotly`.
- **Date Parsing:** Dates in `YYYYMMDD` format are parsed into datetime objects for better visualization.

## Folders to Ignore
- `learn/`: Contains course materials and reference data.
