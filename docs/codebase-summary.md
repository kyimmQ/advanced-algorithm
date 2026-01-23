# Codebase Summary

## Repository Structure

```
/Users/cac.lp/school/252/AA/
├── btl/                          # Assignment work (Bài Tập Lớn)
│   ├── strategies/               # Strategy implementations
│   │   ├── __init__.py
│   │   └── strategy_sma_gap_momentum.py
│   ├── tests/                    # Test scripts
│   │   ├── __init__.py
│   │   └── test_strategy_anomalies.py
│   ├── notebooks/                # Jupyter notebooks
│   │   ├── Sample Assignment.ipynb
│   │   └── Strategy Analysis and Visualization.ipynb
│   ├── sample_data/              # Stock datasets
│   │   ├── s1.npy ... s30.npy    # 30 stock files
│   │   └── Guidance.txt
│   ├── main.py                   # Main execution script
│   └── README.md                 # BTL directory guide
├── learn/                        # Course materials
│   ├── 01_*.ipynb ... 12_*.ipynb # 12 course notebooks
│   ├── video_*.ipynb             # 4 video lecture notebooks
│   ├── exercise_*.ipynb          # 3 exercise notebooks
│   ├── backtester_*.py           # 7 OOP backtester modules
│   ├── demo_ta_intro.py          # Demo script
│   └── *.csv                     # 17 practice datasets
├── docs/                         # Documentation
│   ├── project-overview-pdr.md
│   ├── codebase-summary.md       # This file
│   ├── code-standards.md
│   ├── system-architecture.md
│   ├── python-scripts-guide.md
│   └── notebook-visualization-guide.md
├── plans/                        # Development plans
│   └── reports/                  # Agent reports
│       └── script-conversion-260123-1321-notebook-to-python.md
├── .claude/                      # Claude Code configuration
│   └── workflows/                # Orchestration workflows
├── .venv/                        # Python virtual environment
├── requirements.txt              # Python packages
├── CLAUDE.md                     # Claude agent instructions
├── README.md                     # Project README
└── .gitignore                    # Git configuration
```

## Key Components

### 1. Assignment Workspace (`btl/`)

#### Organized Structure
The btl directory is now organized into:
- **strategies/** - Strategy module implementations
- **tests/** - Testing scripts
- **notebooks/** - Jupyter notebooks
- **sample_data/** - Stock data files

#### Strategy Module (`btl/strategies/`)
**strategy_sma_gap_momentum.py** (264 lines)
- SMA Gap Momentum prediction strategy
- Functions: `sma()`, `calculate_features()`, `detect_anomalies()`, `predict_returns()`
- Implements gap-based return prediction with volume/volatility adjustments

#### Test Scripts (`btl/tests/`)
**test_strategy_anomalies.py** (275 lines)
- Anomaly detection analysis
- Detailed statistics and sample printing
- CLI support: `--stock`, `--all`, `--output`

#### Notebooks (`btl/notebooks/`)
**Strategy Analysis and Visualization.ipynb**
- 14 comprehensive sections
- 6 interactive Plotly visualizations
- Performance analysis and directional accuracy

**Sample Assignment.ipynb**
- Original assignment notebook
- SMA gap momentum implementation

#### Main Script (`btl/main.py`)
**main.py** (264 lines)
- Data loading and prediction execution
- Performance evaluation
- CLI support: `--stock`, `--all`, `--no-plot`, `--output`

#### Stock Data Files
**Format:** NumPy binary (.npy)
- **Count:** 30 files (s1.npy to s30.npy)
- **Dimensions:** 242 rows × 8 columns per file
- **Timeframe:** ~1 year of trading days
- **Columns:**
  1. `date`: Trading date
  2. `open`: Opening price
  3. `close`: Closing price
  4. `low`: Lowest price
  5. `high`: Highest price
  6. `nsh`: Number of shares
  7. `volume`: Trading volume
  8. `adjusted`: Adjusted closing price

#### Assignment Instructions
**File:** `Guidance.txt`
- Problem definition: Forecast Return[n] from P[:-(n-1)], V[:-(n-1)]
- Evaluation: Different time interval, same 30 stocks
- Submission: Customized notebook via LMS

### 2. Learning Materials (`learn/`)

#### Course Notebooks (21 total)

**Sequential Course (12 notebooks):**
1. `01_*.ipynb`: Introduction to Technical Analysis
2. `02_*.ipynb`: Simple Moving Average (SMA)
3. `03_*.ipynb`: Exponential Moving Average (EMA)
4. `04_*.ipynb`: Moving Average Convergence Divergence (MACD)
5. `05_*.ipynb`: Relative Strength Index (RSI)
6. `06_*.ipynb`: Stochastic Oscillator
7. `07_*.ipynb`: Bollinger Bands
8. `08_*.ipynb`: Pivot Points
9. `09_*.ipynb`: Fibonacci Retracements
10. `10_*.ipynb`: Advanced Patterns
11. `11_*.ipynb`: Strategy Combination
12. `12_*.ipynb`: Backtesting Framework

**Video Lectures (4 notebooks):**
- `video_lecture_01.ipynb` to `video_lecture_04.ipynb`
- Companion materials for course videos

**Exercises (3 notebooks):**
- `exercise_01.ipynb`, `exercise_02.ipynb`, `exercise_03.ipynb`
- Practice problems with solutions

#### Backtester Modules (7 files)

**OOP Framework for Strategy Testing:**
1. `backtester_base.py`: Base backtester class
2. `backtester_sma.py`: SMA strategy implementation
3. `backtester_ema.py`: EMA strategy implementation
4. `backtester_macd.py`: MACD strategy implementation
5. `backtester_rsi.py`: RSI strategy implementation
6. `backtester_bollinger.py`: Bollinger Bands strategy
7. `backtester_combined.py`: Multi-indicator strategies

**Features:**
- Object-oriented design
- Modular strategy components
- Performance metrics calculation
- Visualization support

#### Demo Script
**File:** `demo_ta_intro.py`
- **Lines:** 103
- **Purpose:** Interactive TA demo with live data
- **Key Features:**
  - `yfinance` integration for data fetching
  - `Plotly` + `QuantFig` for visualization
  - Real-time indicator calculation
  - Interactive candlestick charts

#### Practice Datasets (17 CSV files)
- Historical stock data for exercises
- Various timeframes and stocks
- Used in course notebooks and exercises

### 3. Configuration & Dependencies

#### Python Environment
**File:** `requirements.txt` (123 packages)

**Core Scientific Stack:**
- `numpy==1.26.4`: Numerical computation
- `pandas==2.3.3`: Data manipulation
- `matplotlib==3.10.8`: Static plotting
- `plotly==5.24.1`: Interactive visualization

**Financial Libraries:**
- `yfinance==1.0`: Yahoo Finance data fetching
- `cufflinks==0.17.3`: Plotly-pandas integration

**Jupyter Ecosystem:**
- `jupyter==1.1.1`: Notebook server
- `jupyterlab==4.5.2`: Modern IDE interface
- `ipykernel==6.29.5`: IPython kernel
- `ipywidgets==8.1.8`: Interactive widgets

**Database:**
- `peewee==3.19.0`: ORM for data persistence

**Other Notable:**
- `beautifulsoup4==4.14.3`: Web scraping
- `requests==2.32.5`: HTTP library
- `PyYAML==6.0.3`: Configuration parsing

#### Virtual Environment
- Location: `.venv/`
- Python version: 3.x (compatible with requirements)
- Isolated dependency management

### 4. Development Infrastructure

#### Claude Code Configuration (`.claude/`)
- Workflow definitions for orchestration
- Agent instructions and protocols
- Hook scripts for automation
- Skills and subagent configurations

#### Documentation (`docs/`)
- Project overview and PDR
- Codebase summary (this file)
- Code standards and conventions
- System architecture documentation

#### Planning & Reports (`plans/`)
- Development plans
- Scout reports from codebase analysis
- Agent execution reports
- Decision logs

## Current Implementation

### Completed Features

1. **Data Pipeline**
   - NumPy-based data loading for 30 stocks
   - Feature extraction from OHLCV columns
   - Data validation and shape verification

2. **Technical Indicators**
   - Simple Moving Average (SMA) trends
   - Multiple period support (e.g., 20-day, 50-day)
   - Trend classification (bullish/bearish)

3. **Pattern Detection**
   - Statistical anomaly detection
   - Threshold-based outlier identification
   - Gap momentum strategy
   - Price gap analysis

4. **Visualization System**
   - Plotly-based interactive charts
   - Multi-subplot dashboard layout
   - Price, volume, and indicator overlays
   - Candlestick chart support
   - Dynamic filtering and zooming

5. **Strategy Framework**
   - Gap momentum buy/sell signals
   - SMA crossover logic (foundation)
   - Strategy parameter configuration

### In Progress

1. **Core Prediction Function** (Cell 14)
   - **Status:** Empty implementation
   - **Required:** Main forecasting logic
   - **Input:** Historical P[:-(n-1)], V[:-(n-1)]
   - **Output:** Predicted Return[n] for next day
   - **Constraints:** [-7%, +7%] return range

2. **Advanced Indicators**
   - EMA, MACD, RSI implementation
   - Bollinger Bands integration
   - Multi-indicator fusion

3. **Feature Engineering**
   - Lag features creation
   - Technical indicator features
   - Volume-based signals
   - Price momentum metrics

### Known Issues

#### Bug in Cell 11 (Visualization)
- **Type:** Undefined variable reference
- **Impact:** Breaks notebook execution flow
- **Severity:** Medium (blocks visualization)
- **Status:** Identified, awaiting fix
- **Location:** Dashboard rendering cell

#### Empty Prediction Function (Cell 14)
- **Type:** Missing implementation
- **Impact:** Assignment incomplete
- **Severity:** Critical (core requirement)
- **Status:** Awaiting implementation
- **Priority:** Highest

## Data Specifications

### Stock Dataset Format

**File Structure:**
- Extension: `.npy` (NumPy binary format)
- Encoding: NumPy default (platform-dependent endianness)
- Compression: None

**Data Schema:**
```python
shape: (242, 8)
dtype: [
    ('date', 'datetime64[D]'),
    ('open', 'float64'),
    ('close', 'float64'),
    ('low', 'float64'),
    ('high', 'float64'),
    ('nsh', 'int64'),          # Number of shares
    ('volume', 'float64'),
    ('adjusted', 'float64')     # Adjusted close
]
```

**Data Characteristics:**
- Trading days: 242 (~1 year, accounting for weekends/holidays)
- Price range: Varies by stock
- Return range: [-7%, +7%] (constrained)
- Missing values: Unknown (requires validation)

### Loading Pattern

```python
import numpy as np

# Load single stock
data = np.load('btl/s1.npy')

# Access columns
dates = data[:, 0]
open_prices = data[:, 1]
close_prices = data[:, 2]
# ... etc
```

## Technical Stack

### Core Technologies

1. **Programming Language:** Python 3.x
2. **Computation:** NumPy, Pandas
3. **Visualization:** Matplotlib, Plotly, Cufflinks
4. **Development:** Jupyter Notebook/Lab
5. **Data Source:** Provided .npy files (+ yfinance for reference)
6. **Version Control:** Git

### Development Tools

1. **AI Assistants:**
   - Claude Code (orchestration, planning)
   - Gemini (specialized tasks)

2. **Environment:**
   - Virtual environment (`.venv/`)
   - Jupyter kernel for notebook execution
   - Interactive widget support

3. **Libraries:**
   - Scientific: numpy, pandas, scipy
   - Visualization: matplotlib, plotly, seaborn
   - Financial: yfinance, cufflinks
   - ML (potential): scikit-learn, statsmodels

## Code Organization

### Notebook Structure (`Sample Assignment.ipynb`)

**Section 1: Setup & Data Loading (Cells 1-3)**
- Import libraries
- Load 30 stock datasets
- Define helper functions

**Section 2: Exploratory Analysis (Cells 4-6)**
- Data shape verification
- Basic statistics
- Feature distribution

**Section 3: Technical Analysis (Cells 7-10)**
- SMA calculation and trends
- Anomaly detection logic
- Gap momentum strategy
- Signal generation

**Section 4: Visualization (Cells 11-13)**
- Dashboard setup (BUG in cell 11)
- Multi-subplot charts
- Interactive Plotly figures

**Section 5: Prediction (Cell 14+)**
- **Cell 14:** Main prediction function (EMPTY)
- Evaluation metrics
- Result compilation

### Course Material Organization

**Progressive Learning Path:**
1. Basics: Introduction, SMA, EMA
2. Oscillators: MACD, RSI, Stochastic
3. Bands: Bollinger Bands
4. Levels: Pivot Points, Fibonacci
5. Integration: Multi-indicator strategies
6. Validation: Backtesting framework

**Modular Backtester:**
- Base class with common functionality
- Strategy-specific subclasses
- Pluggable indicator modules
- Reusable performance metrics

## Metrics & Performance

### Target Metrics (from assignment)

1. **Absolute Error:** `|predicted - actual| < 0.005`
2. **Relative Performance:** `relative_score > 0`
3. **Evaluation:** Different time interval, same 30 stocks

### Additional Metrics (recommended)

1. **Accuracy Metrics:**
   - Mean Absolute Error (MAE)
   - Root Mean Squared Error (RMSE)
   - Mean Absolute Percentage Error (MAPE)

2. **Directional Metrics:**
   - Directional accuracy (up/down correct)
   - Confusion matrix for trend prediction
   - Precision/recall for buy/sell signals

3. **Financial Metrics:**
   - Sharpe ratio (if trading strategy)
   - Maximum drawdown
   - Win rate

## Dependencies Map

### Core Dependencies
```
numpy (1.26.4)
  └── pandas (2.3.3)
        └── matplotlib (3.10.8)
              └── plotly (5.24.1)
                    └── cufflinks (0.17.3)
```

### Jupyter Stack
```
jupyter (1.1.1)
  ├── jupyterlab (4.5.2)
  ├── notebook (7.5.2)
  ├── ipykernel (6.29.5)
  │     └── ipython (8.38.0)
  └── ipywidgets (8.1.8)
```

### Financial Stack
```
yfinance (1.0)
  └── requests (2.32.5)
        └── urllib3 (2.6.3)
```

## File Size & Complexity

### Assignment Files (`btl/`)
- `Sample Assignment.ipynb`: ~50-100 KB (estimated, with outputs)
- Stock data files (30 × .npy): ~10-50 KB each
- Total: ~1-2 MB

### Course Materials (`learn/`)
- 21 notebooks: ~5-10 MB total (with outputs)
- 7 Python modules: ~50-100 KB total
- 17 CSV datasets: ~5-20 MB total
- Total: ~15-30 MB

### Environment
- `.venv/`: 100-500 MB (full Python packages)
- Node modules (if any): N/A

## Version Control Status

### Git Repository
- **Branch:** main
- **Recent commits:**
  - `7b2d807`: Add gemini support
  - `8bde29a`: initial commit

### Tracked Changes
- Modified: `btl/Sample Assignment.ipynb`
- Untracked: `.claude/`, `CLAUDE.md`

### Ignored Files (`.gitignore`)
- `.venv/` (virtual environment)
- `.DS_Store` (macOS metadata)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)

## Next Steps

### Immediate Priorities

1. **Fix Cell 11 Bug**
   - Debug undefined variable
   - Restore visualization functionality
   - Test dashboard rendering

2. **Implement Prediction Function (Cell 14)**
   - Design forecasting approach
   - Implement model/algorithm
   - Validate outputs against constraints

3. **Feature Engineering**
   - Create technical indicator features
   - Generate lag features
   - Engineer volume-based signals

### Medium-Term Goals

1. Model validation and testing
2. Performance optimization
3. Documentation completion
4. Team member names addition
5. Final submission preparation

### Long-Term Enhancements

1. Advanced indicator integration
2. Ensemble prediction methods
3. Cross-validation framework
4. Automated hyperparameter tuning

## Notes

- Codebase well-structured with clear separation (assignment vs learning)
- Rich course materials provide comprehensive TA foundation
- Main blocker: Empty prediction function (cell 14)
- Minor blocker: Cell 11 visualization bug
- Strong foundation in data loading and basic indicators
- Ready for core prediction logic implementation
