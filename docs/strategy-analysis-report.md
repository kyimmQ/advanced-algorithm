# Stock Prediction Strategy Analysis Report

**Date:** 2026-01-23
**Project:** CO5115 Stock Price Forecasting
**Comparison:** SMA Gap Momentum vs. Multi-Factor Technical Ensemble (MFTE)

## 1. Strategy Overview

### 1.1 SMA Gap Momentum (Baseline)
- **Logic:** Analyzes the relationship between the 5-day and 20-day Simple Moving Averages (SMA).
- **Signal Classification:**
    - **Strong Downtrend:** SMA5 < SMA20 and gap is widening.
    - **Signal Uptrend:** SMA5 < SMA20 and gap is narrowing (potential recovery).
    - **Strong Uptrend:** SMA5 > SMA20 and gap is widening.
    - **Signal Downtrend:** SMA5 > SMA20 and gap is narrowing (potential drop).
- **Prediction:** Generates a forecast based on the weighted gap strength and momentum.

### 1.2 Multi-Factor Technical Ensemble (MFTE)
- **Logic:** Combines three distinct technical analysis approaches to provide a balanced forecast.
- **Components:**
    - **Trend (MACD):** Uses EMA(12) and EMA(26) crossover logic to identify mid-term direction.
    - **Mean Reversion (RSI):** Identifies overbought (>70) or oversold (<30) conditions.
    - **Volatility (Bollinger Bands):** Measures price distance from the 20-day mean in standard deviation units.
- **Ensemble Logic:** Weighted sum of normalized signals (Trend: 40%, Reversion: 40%, Momentum: 20%).

---

## 2. Performance Comparison

The strategies were evaluated on 30 stocks (`s1` to `s30`) using two primary metrics:
1. **Absolute Error (MAE):** Target < 0.005
2. **Relative Score (rel):** Target > 0 (measures improvement over naive forecast)

### 2.1 Summary Statistics

| Metric | SMA Gap Momentum | MFTE (Ensemble) | Improvement |
| :--- | :--- | :--- | :--- |
| **Rel Score (Mean)** | -0.0413 | **-0.0126** | +0.0287 |
| **Rel Score (Max)** | 0.0922 | 0.0690 | - |
| **Rel Passed (Score > 0)** | 5 / 30 | **8 / 30** | **+60%** |
| **Abs Error (Mean)** | 0.0189 | **0.0185** | +0.0004 |
| **Both Criteria Passed** | 0 / 30 | 0 / 30 | - |

### 2.2 Key Findings
- **Predictive Power:** The MFTE strategy successfully achieved a positive relative score (`rel > 0`) for **8 stocks**, compared to only 5 for the SMA strategy.
- **Robustness:** The Ensemble method shows a much higher mean relative score (-0.0126 vs -0.0413), indicating it is closer to outperforming the naive baseline across the entire dataset.
- **Stability:** The Absolute Error is slightly lower in the Ensemble strategy, suggesting better consistency.

---

## 3. Top Performing Stocks (MFTE)

The following stocks showed positive signals (`rel > 0`) with the Ensemble strategy:

| Stock | Abs Error | Rel Score | Status |
| :--- | :--- | :--- | :--- |
| **s28** | 0.0126 | **0.0690** | ✓ Rel Pass |
| **s10** | 0.0194 | **0.0648** | ✓ Rel Pass |
| **s23** | 0.0170 | **0.0558** | ✓ Rel Pass |
| **s18** | 0.0175 | **0.0201** | ✓ Rel Pass |
| **s29** | 0.0223 | **0.0169** | ✓ Rel Pass |
| **s26** | 0.0245 | **0.0133** | ✓ Rel Pass |
| **s25** | 0.0123 | **0.0023** | ✓ Rel Pass |
| **s3** | 0.0217 | **0.0019** | ✓ Rel Pass |

---

## 4. Implementation Details

### 4.1 Files
- **SMA Strategy:** `btl/strategies/strategy_sma_gap_momentum.py`
- **Ensemble Strategy:** `btl/strategies/strategy_ensemble_v1.py`
- **Execution Script:** `btl/main.py` (use `--strategy ensemble` flag)
- **Analysis Notebooks:**
    - `btl/notebooks/Strategy Analysis and Visualization.ipynb` (SMA)
    - `btl/notebooks/Ensemble Strategy Analysis.ipynb` (MFTE)

### 4.2 How to Reproduce
To run the full benchmark again and generate CSV results:
```bash
# SMA Strategy
python main.py --all --strategy sma --output sma_results.csv

# Ensemble Strategy
python main.py --all --strategy ensemble --output ensemble_results.csv
```

---

## 5. Next Steps
1. **Hyperparameter Tuning:** Use optimization to find best weights for Trend vs. Reversion.
2. **Indicator Expansion:** Add ATR for volatility scaling and Stochastic Oscillator for reversal confirmation.
3. **Data Quality:** Investigate stocks with high error (e.g., s22) to understand failure modes.
