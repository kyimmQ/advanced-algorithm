# Stock Price Forecasting - CO5115 Assignment

Academic assignment for stock return prediction using technical analysis and Python. Predict next-day returns for 30 stocks using historical OHLCV data.

**Institution:** HCMUT (Ho Chi Minh University of Technology)
**Course:** CO5115 - Technical Analysis with Python
**Instructor:** vinhpham@hcmut.edu.vn

## Overview

### Problem Statement

Given historical price and volume data, forecast next-day stock returns:

```
f(P[:-(n-1)], V[:-(n-1)]) = Return[n]

Where:
- P = price data (open, close, low, high, adjusted)
- V = volume data (number of shares, volume)
- n = trading day index
- Return range: [-7%, +7%]
```

### Dataset

- **Stocks:** 30 files (s1.npy to s30.npy)
- **Timeframe:** 242 trading days (~1 year)
- **Features:** 8 columns per file

### Evaluation Criteria

- **Absolute Error:** `|predicted - actual| < 0.005`
- **Relative Performance:** `relative_score > 0`
- **Test Data:** Different time interval, same 30 stocks

## Project Structure

```
.
├── btl/                          # Assignment workspace (Bài Tập Lớn)
│   ├── strategies/               # Strategy implementations
│   ├── tests/                    # Test scripts
│   ├── notebooks/                # Jupyter notebooks
│   ├── sample_data/              # Stock datasets
│   ├── main.py                   # Main execution script
│   └── README.md                 # BTL directory guide
├── learn/                        # Course materials
│   ├── 01_*.ipynb ... 12_*.ipynb # 12 course notebooks
│   ├── video_*.ipynb             # 4 video lecture notebooks
│   ├── exercise_*.ipynb          # 3 practice exercises
│   ├── backtester_*.py           # 7 OOP backtester modules
│   ├── demo_ta_intro.py          # 103-line demo script
│   └── *.csv                     # 17 practice datasets
├── docs/                         # Documentation
│   ├── project-overview-pdr.md   # Project overview & PDR
│   ├── codebase-summary.md       # Comprehensive codebase summary
│   ├── code-standards.md         # Code standards & structure
│   ├── system-architecture.md    # System architecture
│   ├── python-scripts-guide.md   # Guide for new Python scripts
│   └── notebook-visualization-guide.md # Guide for visualization notebook
├── .claude/                      # Claude Code configuration
├── plans/                        # Development plans & reports
├── .venv/                        # Python virtual environment
├── requirements.txt              # Python packages
├── CLAUDE.md                     # Claude agent instructions
└── README.md                     # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- 2+ GB RAM
- 100 MB disk space

### Installation

1. **Clone or download the repository**

2. **Activate virtual environment**
   ```bash
   # macOS/Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project

#### 1. Main Strategy Script
Run the prediction engine from the `btl/` directory:
```bash
cd btl
python main.py --stock s1
```

#### 2. Anomaly Testing
Run the anomaly detection analysis:
```bash
python btl/tests/test_strategy_anomalies.py --stock s1
```

#### 3. Interactive Notebooks
Launch Jupyter to explore visualizations:
```bash
jupyter lab btl/notebooks/Strategy\ Analysis\ and\ Visualization.ipynb
```

## Current Status

### ✅ Completed Components

- **Modular Architecture:** Separated strategies, tests, and notebooks
- **Strategy Implementation:** SMA Gap Momentum strategy with forward-looking anomaly detection
- **Prediction Engine:** `main.py` for batch processing all 30 stocks
- **Validation Suite:** Anomaly detection tests to verify strategy reliability
- **Documentation:** Full documentation suite in `docs/`

### ⏳ In Progress

- Refinement of SMA Gap Momentum weights to meet MAE < 0.005 target
- Integration of advanced indicators (RSI, MACD) into the modular strategy
- Ensemble prediction methods

## Performance Metrics

The project is evaluated against:
- **Absolute Error (MAE):** Target < 0.005
- **Relative Score:** Target > 0

Current benchmark for `s1`:
- MAE: ~0.011
- Relative Score: ~ -0.047
- Anomaly Rate: ~46%

## Documentation

Comprehensive documentation in `docs/`:

- **Project Overview & PDR** (`docs/project-overview-pdr.md`)
- **Codebase Summary** (`docs/codebase-summary.md`)
- **Code Standards** (`docs/code-standards.md`)
- **System Architecture** (`docs/system-architecture.md`)
- **Python Scripts Guide** (`docs/python-scripts-guide.md`)
- **Visualization Guide** (`docs/notebook-visualization-guide.md`)

## License

Academic assignment for HCMUT course CO5115. For educational purposes only.

## Contact

**Instructor:** vinhpham@hcmut.edu.vn
**Submission:** Via LMS system
**Team Members:** [Fill in your team member names]

---

**Last Updated:** 2026-01-23
**Status:** Major refactor complete - Strategy refinement in progress
