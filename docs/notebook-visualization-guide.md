# Strategy Analysis and Visualization Notebook

## Overview

This notebook provides comprehensive analysis and visualization of the SMA Gap Momentum strategy. It imports the modular Python scripts and adds rich interactive visualizations.

## Features

### 1. **Price Analysis with SMA Trend Cloud**
- Interactive Plotly visualization
- SMA5 and SMA20 overlays
- Green/red trend cloud showing uptrend/downtrend zones
- Volume chart below

### 2. **SMA Gap Momentum Signals**
- Color-coded gap bars showing signal strength
- 4 signal types: Strong Uptrend, Signal Uptrend, Strong Downtrend, Signal Downtrend
- Price and SMA lines for context

### 3. **Anomaly Detection Visualization**
- Markers showing where strategy signals failed
- Black X marks: Expected up but price dropped
- Purple circles: Expected down but price rose
- Gap momentum chart for context

### 4. **Prediction Performance**
- Predicted vs Actual returns comparison (line chart)
- Scatter plot showing prediction accuracy
- Perfect prediction line (y=x) for reference
- Prediction error histogram

### 5. **Directional Accuracy Analysis**
- Confusion matrix for up/down predictions
- Directional accuracy percentage
- Breakdown of correct/incorrect predictions

### 6. **Comprehensive Summary**
- Data statistics
- Strategy performance metrics
- Prediction evaluation results
- Recommendations for improvement

## How to Use

### Quick Start

```bash
# 1. Navigate to btl directory
cd /Users/cac.lp/school/252/AA/btl

# 2. Launch Jupyter Lab
jupyter lab
# OR
jupyter notebook

# 3. Open "Strategy Analysis and Visualization.ipynb"

# 4. Run all cells (Cell → Run All)
```

### Customize Analysis

To analyze different stocks, modify cell 2:

```python
# Configuration
STOCK_NAME = 's5'  # Change this to s1, s2, ..., s30
DATA_DIR = 'sample_data'
```

Then run all cells again.

## Notebook Structure

| Section | Description |
|---------|-------------|
| 1. Configuration | Set stock name and data directory |
| 2. Load Data | Load .npy file and extract prices/volumes |
| 3. Calculate Features | Generate SMA5, SMA20, gap, signals |
| 4. Detect Anomalies | Find signal failures |
| 5-7. Visualizations | Interactive Plotly charts |
| 8. Generate Predictions | Run prediction algorithm |
| 9. Calculate Actual Returns | Compute ground truth |
| 10. Evaluate Performance | Calculate metrics |
| 11-12. Prediction Viz | Compare predicted vs actual |
| 13. Directional Accuracy | Up/down prediction analysis |
| 14. Final Summary | Complete performance report |

## Visualization Examples

### Chart 1: Price with SMA Trend Cloud
Shows price movement with colored zones:
- Green zone = SMA5 above SMA20 (uptrend)
- Red zone = SMA5 below SMA20 (downtrend)

### Chart 2: Gap Momentum Signals
Color-coded bars showing signal strength:
- Dark green = Strong Uptrend
- Green = Signal Uptrend (recovery)
- Orange = Signal Downtrend (weakening)
- Red = Strong Downtrend

### Chart 3: Anomaly Markers
Visual representation of signal failures:
- Helps identify when strategy is unreliable
- Shows concentration of anomalies over time

### Chart 4: Predicted vs Actual
Line comparison showing:
- How well predictions track actual returns
- Visual assessment of prediction lag
- Magnitude of prediction errors

### Chart 5: Scatter Plot
Shows correlation between predicted and actual:
- Points on diagonal = perfect predictions
- Distance from diagonal = prediction error
- Helps identify systematic bias

## Output Metrics

The notebook calculates and displays:

**Strategy Metrics:**
- Total anomalies and percentage
- Anomaly rate by signal type
- Signal distribution

**Prediction Metrics:**
- Absolute Error (target: < 0.005)
- Relative Score (target: > 0)
- Directional Accuracy (%)
- Mean/Median/Min/Max predictions

**Statistical Analysis:**
- Prediction error histogram
- Confusion matrix
- Performance summary with recommendations

## Tips

1. **Interactive Charts**: All Plotly charts are interactive
   - Hover to see values
   - Zoom by dragging
   - Pan by dragging
   - Double-click to reset

2. **Quick Stock Comparison**:
   - Change STOCK_NAME in cell 2
   - Run all cells (Cell → Run All)
   - Compare results

3. **Export Results**:
   - Save charts: Click camera icon on Plotly chart
   - Export data: Add cells to save DataFrames to CSV

4. **Batch Analysis**:
   - For all 30 stocks, use `main.py --all` instead
   - This notebook is best for single-stock deep analysis

## Requirements

All dependencies are in the virtual environment:
- numpy
- pandas
- matplotlib
- plotly
- strategy_sma_gap_momentum module

## Troubleshooting

**Module not found error:**
```bash
# Make sure you're in the btl directory
cd /Users/cac.lp/school/252/AA/btl

# Verify strategy module exists
ls strategy_sma_gap_momentum.py
```

**Data file not found:**
```bash
# Check data directory
ls sample_data/s1.npy

# Update DATA_DIR in cell 2 if needed
```

**Charts not displaying:**
- Ensure Jupyter extensions are enabled
- Try: `jupyter labextension list`
- Restart Jupyter kernel

## Example Output

Running on stock s1 shows:
- 242 trading days analyzed
- 113 anomalies (46.7% of days)
- Absolute error: 0.011635 (above target)
- Relative score: -0.047226 (below target)
- Directional accuracy: ~50%

High anomaly rates indicate strategy needs refinement.

## Next Steps

After running the notebook:
1. Review anomaly patterns in visualizations
2. Check directional accuracy
3. Read recommendations in final summary
4. Consider adding more technical indicators
5. Experiment with different prediction weights

## Related Files

- `strategy_sma_gap_momentum.py` - Strategy implementation
- `main.py` - Batch processing script
- `test_strategy_anomalies.py` - Anomaly testing script
- `README_SCRIPTS.md` - Scripts documentation
