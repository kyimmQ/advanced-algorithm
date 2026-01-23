# BTL Directory - Stock Prediction Project

Organized codebase for CO5115 Stock Price Forecasting Assignment.

## Directory Structure

```
btl/
├── strategies/              # Strategy implementations
│   ├── __init__.py
│   └── strategy_sma_gap_momentum.py
├── tests/                   # Test scripts
│   ├── __init__.py
│   └── test_strategy_anomalies.py
├── notebooks/               # Jupyter notebooks
│   ├── Sample Assignment.ipynb
│   └── Strategy Analysis and Visualization.ipynb
├── sample_data/            # Stock data files
│   ├── s1.npy ... s30.npy (30 stocks)
│   └── Guidance.txt
├── main.py                 # Main execution script
└── README.md              # This file
```

## Quick Start

### 1. Run Main Script (from btl directory)

```bash
cd /Users/cac.lp/school/252/AA/btl
source ../.venv/bin/activate  # OR use: ../.venv/bin/python main.py

# Single stock
python main.py --stock s1

# All stocks
python main.py --all --output results.csv
```

### 2. Run Anomaly Tests (from anywhere)

```bash
# From btl directory
python tests/test_strategy_anomalies.py --stock s1

# From tests directory
cd tests
python test_strategy_anomalies.py --stock s1

# All stocks
python test_strategy_anomalies.py --all --output anomalies.csv
```

### 3. Run Notebooks

```bash
# From btl directory
jupyter lab

# Or from notebooks directory
cd notebooks
jupyter lab
```

Then open:

- `Strategy Analysis and Visualization.ipynb` - Interactive analysis
- `Sample Assignment.ipynb` - Original assignment

## File Descriptions

### Strategies (`strategies/`)

**strategy_sma_gap_momentum.py** (264 lines)

- Core strategy implementation
- Functions:
  - `sma()` - Simple Moving Average
  - `calculate_features()` - Technical indicators
  - `detect_anomalies()` - Signal failure detection
  - `predict_returns()` - Next-day return prediction
  - `get_strategy_summary()` - Statistics

### Tests (`tests/`)

**test_strategy_anomalies.py** (275 lines)

- Anomaly detection testing
- Detailed statistics and reports
- Sample anomaly printing
- Batch analysis support
- CLI: `--stock`, `--all`, `--output`

### Notebooks (`notebooks/`)

**Strategy Analysis and Visualization.ipynb**

- 14 comprehensive sections
- 6 interactive Plotly visualizations
- Performance analysis
- Directional accuracy
- Runs from notebooks directory

**Sample Assignment.ipynb**

- Original assignment notebook
- SMA gap momentum cells
- Visualization examples

### Main Script (`main.py`)

**main.py** (264 lines)

- Data loading
- Prediction execution
- Performance evaluation
- Batch processing
- CLI: `--stock`, `--all`, `--no-plot`, `--output`

## Usage Examples

### From BTL Directory

```bash
# Main predictions
python main.py --stock s5
python main.py --all --output results.csv

# Tests (relative path)
python tests/test_strategy_anomalies.py --stock s1

# Notebooks
jupyter lab notebooks/
```

### From Tests Directory

```bash
cd tests

# Run tests
python test_strategy_anomalies.py --stock s1
python test_strategy_anomalies.py --all
```

### From Notebooks Directory

```bash
cd notebooks

# Launch Jupyter
jupyter lab

# Open notebooks and run cells
# Imports are configured to work from notebooks/
```

## Import Structure

### From main.py (in btl/)

```python
from strategies.strategy_sma_gap_momentum import predict_returns
```

### From tests (in tests/)

```python
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from strategies.strategy_sma_gap_momentum import (
    calculate_features,
    detect_anomalies,
    get_strategy_summary
)
```

### From notebooks (in notebooks/)

```python
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath('')), '..'))
from strategies import (
    calculate_features,
    detect_anomalies,
    predict_returns,
    get_strategy_summary
)
```

## Data Files

**sample_data/** contains:

- 30 stock files: `s1.npy` to `s30.npy`
- Each file: 242 days × 8 columns
- Columns: [date, open, close, low, high, nsh, volume, adjusted]
- Format: NumPy binary arrays

## Running Tests

All scripts handle paths automatically:

```bash
# Works from btl/
python tests/test_strategy_anomalies.py --stock s1

# Also works from tests/
cd tests
python test_strategy_anomalies.py --stock s1

# Data paths are resolved relative to script location
```

## Performance Metrics

**Current Results (Stock s1):**

- Absolute Error: 0.011635 (target: < 0.005) ✗
- Relative Score: -0.047226 (target: > 0) ✗
- Anomaly Rate: 46.7% (113/242 days)

**Strategy needs tuning to meet targets.**

## Troubleshooting

### Import Errors

```bash
# Ensure you're using the virtual environment
source ../.venv/bin/activate  # from btl/
source ../../.venv/bin/activate  # from tests/

# Verify Python can find modules
python -c "from strategies import predict_returns"
```

### Path Issues

```bash
# Always activate from project root
cd /Users/cac.lp/school/252/AA
source .venv/bin/activate

# Then navigate to working directory
cd btl
python main.py --stock s1
```

### Jupyter Kernel

```bash
# Make sure to use the project's venv kernel
# In Jupyter: Kernel → Change Kernel → Python 3 (.venv)
```

## Documentation

See `/docs` directory for:

- `python-scripts-guide.md` - Detailed script usage
- `notebook-visualization-guide.md` - Notebook guide
- `code-standards.md` - Coding standards
- `system-architecture.md` - Architecture overview

## Next Steps

1. **Improve Strategy**: Add more technical indicators
2. **Tune Parameters**: Adjust prediction weights
3. **Validate Performance**: Test on all 30 stocks
4. **Reduce Anomalies**: Refine signal classification
5. **Meet Targets**: Absolute error < 0.005, Relative score > 0

## Related Files

**In `/docs`:**

- python-scripts-guide.md
- notebook-visualization-guide.md

**In `/plans/reports`:**

- script-conversion-260123-1321-notebook-to-python.md

---

**Last Updated:** 2026-01-23
**Status:** Organized and tested ✓
