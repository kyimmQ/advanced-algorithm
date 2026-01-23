# Python Scripts - SMA Gap Momentum Strategy

This directory contains modular Python scripts for stock return prediction using the SMA Gap Momentum strategy.

## Files

### 1. `strategy_sma_gap_momentum.py`
Strategy module implementing the SMA Gap Momentum prediction algorithm.

**Key Functions:**
- `sma(data, n)` - Calculate Simple Moving Average
- `calculate_features(P, V)` - Calculate technical features (SMA5, SMA20, gap, signals)
- `detect_anomalies(df)` - Detect anomalies where price contradicts signals
- `predict_returns(P, V)` - Core prediction function (returns array of predicted returns)
- `get_strategy_summary(df)` - Generate summary statistics

**Strategy Logic:**
- Analyzes gap between SMA5 and SMA20
- Classifies signals: Strong Uptrend, Signal Uptrend, Strong Downtrend, Signal Downtrend
- Predicts returns based on gap momentum, volume patterns, and volatility

### 2. `main.py`
Main script for running predictions and evaluating performance.

**Usage:**
```bash
# Activate virtual environment first
source ../.venv/bin/activate

# Run on single stock (default: s1)
python main.py

# Run on specific stock
python main.py --stock s5

# Run on specific stock without plotting
python main.py --stock s1 --no-plot

# Run on all 30 stocks
python main.py --all

# Run on all stocks and save results to CSV
python main.py --all --output results.csv
```

**Performance Metrics:**
- Absolute Error: Target < 0.005
- Relative Score: Target > 0

### 3. `test_strategy_anomalies.py`
Test script for analyzing anomaly patterns in the strategy.

**Usage:**
```bash
# Activate virtual environment first
source ../.venv/bin/activate

# Analyze anomalies for single stock (default: s1)
python test_strategy_anomalies.py

# Analyze specific stock
python test_strategy_anomalies.py --stock s10

# Analyze all 30 stocks
python test_strategy_anomalies.py --all

# Analyze all stocks and save results to CSV
python test_strategy_anomalies.py --all --output anomalies.csv
```

**Output:**
- Strategy signal distribution
- Anomaly counts and rates
- Sample anomalies with dates and price changes
- Aggregate statistics for all stocks

## Quick Start

```bash
# 1. Navigate to btl directory
cd btl

# 2. Activate virtual environment
source ../.venv/bin/activate

# 3. Run prediction on single stock
python main.py --stock s1

# 4. Analyze anomalies
python test_strategy_anomalies.py --stock s1

# 5. Run batch processing on all stocks
python main.py --all --output results.csv
python test_strategy_anomalies.py --all --output anomalies.csv
```

## Strategy Overview

### SMA Gap Momentum Strategy

The strategy analyzes the relationship between two simple moving averages:
- **SMA5**: 5-day simple moving average (short-term trend)
- **SMA20**: 20-day simple moving average (long-term trend)

**Key Metrics:**
1. **Gap**: `SMA5 - SMA20` (measures trend strength)
2. **Gap Change**: Current gap - Previous gap (measures trend acceleration)

**Signal Classification:**

| Signal | Gap | Gap Change | Interpretation |
|--------|-----|------------|----------------|
| Strong Uptrend | Positive | Increasing | Bullish momentum strengthening |
| Signal Uptrend | Negative | Increasing | Recovery from downtrend |
| Strong Downtrend | Negative | Decreasing | Bearish momentum strengthening |
| Signal Downtrend | Positive | Decreasing | Weakening from uptrend |

**Anomalies:**
- Situations where price action contradicts strategy signal
- Example: Strong Downtrend signal but price increased
- Used to assess strategy reliability

## Example Output

### Main Script (`main.py`)
```
============================================================
Processing Stock: s1
============================================================
Loaded 242 trading days
Generating predictions using SMA Gap Momentum strategy...
Evaluating performance...

Performance Summary:
  Absolute Error: 0.011635 ✗ FAIL (target: < 0.005)
  Relative Score: -0.047226 ✗ FAIL (target: > 0)
```

### Anomaly Test (`test_strategy_anomalies.py`)
```
======================================================================
ANOMALY ANALYSIS: s1
======================================================================

Total Trading Days: 242

Strategy Signal Distribution:
  Strong Downtrend:   73 days
  Signal Uptrend:     61 days (recovery)
  Strong Uptrend:     54 days
  Signal Downtrend:   53 days (weakening)

Anomaly Detection Results:
  Strong Downtrend Anomalies (price rose):     21
  Signal Downtrend Anomalies (price rose):     16
  Signal Uptrend Anomalies (price dropped):    24
  Strong Uptrend Anomalies (price dropped):    23
  ────────────────────────────────────────────────────────────
  Total Anomalies:  84 (34.7% of days)
```

## Data Requirements

- Stock data files: `sample_data/s1.npy` to `sample_data/s30.npy`
- Format: NumPy binary arrays (242 days × 8 columns)
- Columns: [date, open, close, low, high, nsh, volume, adjusted]

## Dependencies

All required packages are in the virtual environment (`.venv/`):
- numpy
- pandas
- matplotlib

## Notes

- All scripts use the virtual environment's Python interpreter
- Predictions are constrained to [-7%, +7%] range per assignment requirements
- The strategy uses multiple features: gap momentum, volume ratios, volatility
- Anomaly detection helps identify strategy weaknesses

## Troubleshooting

**Import errors:**
```bash
# Make sure virtual environment is activated
source ../.venv/bin/activate
```

**File not found:**
```bash
# Make sure you're in the btl directory
cd /Users/cac.lp/school/252/AA/btl
```

**Data directory issues:**
```bash
# Specify custom data directory
python main.py --data-dir path/to/data
```
