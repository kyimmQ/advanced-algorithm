# System Architecture

## Overview

Stock price forecasting system for academic assignment using technical analysis and machine learning techniques to predict next-day returns for 30 stocks.

**Architecture Type:** Monolithic Jupyter Notebook with supporting modules
**Primary Language:** Python 3.x
**Deployment:** Local development environment
**Data Flow:** Batch processing (offline analysis)

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER INTERFACE LAYER                       │
│                  (Jupyter Notebook/JupyterLab)                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Matplotlib │  │    Plotly    │  │  Cufflinks   │         │
│  │   Charts     │  │  Interactive │  │  Integration │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                    APPLICATION LAYER                            │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Sample          │  │  Technical   │  │  Prediction  │      │
│  │ Assignment.ipynb│  │  Indicators  │  │  Engine      │      │
│  └─────────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                     BUSINESS LOGIC LAYER                        │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────┐ │
│  │   SMA      │  │    RSI     │  │   MACD     │  │ Bollinger│ │
│  │ Calculator │  │ Calculator │  │ Calculator │  │  Bands   │ │
│  └────────────┘  └────────────┘  └────────────┘  └──────────┘ │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │  Pattern   │  │   Signal   │  │  Feature   │               │
│  │ Detection  │  │ Generation │  │ Engineering│               │
│  └────────────┘  └────────────┘  └────────────┘               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                      DATA ACCESS LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   NumPy I/O  │  │   Pandas     │  │    Data      │         │
│  │  (.npy load) │  │  DataFrame   │  │  Validation  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────┴─────────────────────────────────────┐
│                       DATA STORAGE LAYER                        │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  File System                                           │    │
│  │  ├── btl/s1.npy ... s30.npy (30 stock files)          │    │
│  │  └── 242 days × 8 features per file                   │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Data Layer

#### Data Storage
**Location:** `btl/` directory
**Format:** NumPy binary (.npy)
**Structure:**
```
Stock Data File (s1.npy - s30.npy)
├── Shape: (242, 8)
├── Dtype: float64 (mixed with datetime for column 0)
└── Columns:
    ├── [0] date: Trading date
    ├── [1] open: Opening price
    ├── [2] close: Closing price
    ├── [3] low: Lowest price
    ├── [4] high: Highest price
    ├── [5] nsh: Number of shares
    ├── [6] volume: Trading volume
    └── [7] adjusted: Adjusted close
```

#### Data Access Pattern
```python
# Load single stock
data = np.load('btl/s{id}.npy')

# Transform to pandas
df = pd.DataFrame(data, columns=COLUMN_NAMES)

# Access via indexing
close_prices = data[:, CLOSE_COL]
```

**Characteristics:**
- Read-only access (no writes during prediction)
- Sequential access pattern (time series)
- Fixed schema (8 columns, 242 rows)
- No external data sources (static dataset)

### 2. Business Logic Layer

#### Technical Indicator Modules

**Simple Moving Average (SMA)**
```python
Input:  price_array[t-n:t]
Output: mean(price_array)
Parameters: period (20, 50, 200 days)
```

**Exponential Moving Average (EMA)**
```python
Input:  price_array[t-n:t]
Output: weighted_mean(price_array, alpha=2/(n+1))
Parameters: period (12, 26 days)
```

**Relative Strength Index (RSI)**
```python
Input:  price_array[t-n:t]
Output: 100 - (100 / (1 + RS))
        RS = avg_gain / avg_loss
Parameters: period (14 days)
```

**MACD (Moving Average Convergence Divergence)**
```python
Input:  price_array[t-n:t]
Output: {macd_line, signal_line, histogram}
        macd = EMA(12) - EMA(26)
        signal = EMA(macd, 9)
Parameters: fast=12, slow=26, signal=9
```

**Bollinger Bands**
```python
Input:  price_array[t-n:t]
Output: {upper, middle, lower}
        middle = SMA(20)
        upper = middle + 2*std
        lower = middle - 2*std
Parameters: period=20, num_std=2
```

#### Pattern Detection Modules

**Anomaly Detection**
```python
Method: Statistical outlier detection
Input:  price_array, threshold (e.g., 2.5 sigma)
Output: boolean_array (True = anomaly)
Algorithm:
  1. Calculate mean and std
  2. Identify points > threshold * std from mean
  3. Return anomaly flags
```

**Gap Detection**
```python
Method: Overnight gap analysis
Input:  open_prices, close_prices[-1]
Output: gap_size, gap_direction
Algorithm:
  1. gap = open[t] - close[t-1]
  2. gap_pct = gap / close[t-1]
  3. Classify: bullish (gap > 0) or bearish (gap < 0)
```

**Trend Classification**
```python
Method: SMA slope analysis
Input:  sma_array, lookback
Output: trend_label ('bullish' | 'bearish' | 'neutral')
Algorithm:
  1. Calculate slope of SMA over lookback
  2. If slope > threshold: bullish
  3. If slope < -threshold: bearish
  4. Else: neutral
```

#### Signal Generation

**Crossover Signals**
```python
Input:  indicator_fast, indicator_slow
Output: signal (-1, 0, 1)
Logic:
  - Bullish cross: fast crosses above slow → +1
  - Bearish cross: fast crosses below slow → -1
  - No cross: → 0
```

**Threshold Signals**
```python
Input:  indicator, upper_threshold, lower_threshold
Output: signal (-1, 0, 1)
Logic:
  - Overbought: indicator > upper → -1 (sell)
  - Oversold: indicator < lower → +1 (buy)
  - Neutral: else → 0 (hold)
```

### 3. Application Layer

#### Main Notebook Structure

**Sample Assignment.ipynb Architecture:**

```
┌─────────────────────────────────────┐
│       CELL BLOCK 1-2: SETUP         │
│  - Library imports                  │
│  - Global constants                 │
│  - Helper function definitions      │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    CELL BLOCK 3-4: DATA LOADING     │
│  - Load 30 stock files              │
│  - Validate data integrity          │
│  - Create data structures           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  CELL BLOCK 5-6: EXPLORATION        │
│  - Statistical summaries            │
│  - Data distribution analysis       │
│  - Initial visualizations           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│ CELL BLOCK 7-10: TECHNICAL ANALYSIS │
│  - Calculate indicators (SMA, RSI)  │
│  - Detect patterns (gaps, anomalies)│
│  - Generate trading signals         │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  CELL BLOCK 11-13: VISUALIZATION    │
│  - Plotly dashboard creation        │
│  - Multi-subplot charts             │
│  - Interactive analysis tools       │
│  - ⚠️ BUG IN CELL 11               │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   CELL BLOCK 14: PREDICTION         │
│  - Feature extraction               │
│  - Model inference                  │
│  - Return prediction                │
│  - Constraint enforcement           │
│  - ⚠️ CURRENTLY EMPTY              │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  CELL BLOCK 15+: EVALUATION         │
│  - Performance metrics              │
│  - Result visualization             │
│  - Summary statistics               │
└─────────────────────────────────────┘
```

#### Prediction Pipeline

**Core Prediction Flow:**
```
Input: Historical data (P[:-(n-1)], V[:-(n-1)])
  │
  ├─→ Feature Engineering
  │    ├─ Price features (momentum, volatility, returns)
  │    ├─ Volume features (volume ratio, trend)
  │    ├─ Technical indicators (SMA, RSI, MACD)
  │    └─ Pattern features (gaps, anomalies)
  │
  ├─→ Model Inference
  │    ├─ Weighted combination of signals
  │    ├─ Statistical forecasting (ARIMA, etc.)
  │    └─ Rule-based prediction
  │
  ├─→ Post-processing
  │    ├─ Clip to [-0.07, 0.07]
  │    └─ Smoothing/denoising
  │
  └─→ Output: Predicted return for day n
```

### 4. Presentation Layer

#### Visualization Architecture

**Matplotlib Components:**
- Static charts for analysis
- Publication-quality figures
- PDF/PNG export capability

**Plotly Components:**
- Interactive dashboards
- Zoom/pan/hover functionality
- Dynamic filtering
- Multi-panel layouts

**Cufflinks Integration:**
- Pandas DataFrame → Plotly
- One-line chart creation
- Financial chart templates (candlestick, OHLC)

#### Dashboard Layout

```
┌────────────────────────────────────────────────────┐
│                  STOCK DASHBOARD                   │
├────────────────────────────────────────────────────┤
│  Panel 1: Price Chart                              │
│  ├─ Candlestick plot                               │
│  ├─ SMA overlays (20, 50, 200 day)                 │
│  └─ Buy/sell signal markers                        │
├────────────────────────────────────────────────────┤
│  Panel 2: Volume Chart                             │
│  ├─ Bar chart of daily volume                      │
│  └─ Volume moving average                          │
├────────────────────────────────────────────────────┤
│  Panel 3: Technical Indicators                     │
│  ├─ RSI (0-100 scale)                              │
│  ├─ MACD (line + histogram)                        │
│  └─ Bollinger Band width                           │
├────────────────────────────────────────────────────┤
│  Panel 4: Prediction Results                       │
│  ├─ Predicted vs actual returns                    │
│  └─ Error distribution                             │
└────────────────────────────────────────────────────┘
```

## Data Flow Architecture

### End-to-End Data Pipeline

```
┌──────────┐
│ .npy     │
│ Files    │
└────┬─────┘
     │ Load (np.load)
     ↓
┌────────────┐
│ NumPy      │
│ Array      │
│ (242, 8)   │
└────┬───────┘
     │ Transform
     ↓
┌────────────┐
│ Pandas     │
│ DataFrame  │
│ (indexed)  │
└────┬───────┘
     │ Extract columns
     ↓
┌────────────────────────────────┐
│ Feature Arrays                 │
│ ├─ prices (close, open, etc.)  │
│ ├─ volumes                     │
│ └─ dates                       │
└────┬───────────────────────────┘
     │ Calculate indicators
     ↓
┌────────────────────────────────┐
│ Technical Indicator Arrays     │
│ ├─ sma_20, sma_50, sma_200     │
│ ├─ rsi_14                      │
│ ├─ macd_line, signal, hist     │
│ └─ bb_upper, bb_middle, bb_low │
└────┬───────────────────────────┘
     │ Pattern detection
     ↓
┌────────────────────────────────┐
│ Signal Arrays                  │
│ ├─ crossover_signals           │
│ ├─ threshold_signals           │
│ └─ pattern_flags               │
└────┬───────────────────────────┘
     │ Feature engineering
     ↓
┌────────────────────────────────┐
│ Feature Dictionary             │
│ ├─ 'momentum': float           │
│ ├─ 'volatility': float         │
│ ├─ 'volume_ratio': float       │
│ └─ ... (10-20 features)        │
└────┬───────────────────────────┘
     │ Prediction model
     ↓
┌────────────────────────────────┐
│ Raw Prediction (float)         │
└────┬───────────────────────────┘
     │ Post-process (clip)
     ↓
┌────────────────────────────────┐
│ Final Prediction               │
│ (constrained to [-0.07, 0.07]) │
└────┬───────────────────────────┘
     │ Aggregate (all stocks)
     ↓
┌────────────────────────────────┐
│ Results DataFrame              │
│ ├─ stock_id                    │
│ ├─ predicted_return            │
│ ├─ actual_return (if available)│
│ └─ error                       │
└────────────────────────────────┘
```

### Batch Processing Architecture

**For All 30 Stocks:**
```python
results = []

for stock_id in range(1, 31):
    # Load data
    data = load_stock_data(stock_id)

    # Extract features
    prices = data[:, CLOSE_COL]
    volumes = data[:, VOLUME_COL]

    # Predict
    predicted_return = predict_next_return(prices, volumes)

    # Store result
    results.append({
        'stock_id': stock_id,
        'prediction': predicted_return
    })

# Aggregate
results_df = pd.DataFrame(results)
```

## Module Organization

### Assignment Module (`btl/`)

```
btl/
├── Data Files (static)
│   ├── s1.npy ... s30.npy
│   └── 242 days × 8 features each
│
└── Notebook (executable)
    └── Sample Assignment.ipynb
        ├── Setup & config
        ├── Data loading
        ├── Analysis functions
        ├── Prediction logic
        └── Evaluation metrics
```

### Learning Module (`learn/`)

```
learn/
├── Course Notebooks (reference)
│   ├── Sequential lessons (01-12)
│   ├── Video lectures (4 notebooks)
│   └── Exercises (3 notebooks)
│
├── Backtester Framework (OOP)
│   ├── backtester_base.py (abstract base)
│   ├── backtester_sma.py (strategy impl)
│   ├── backtester_ema.py
│   ├── backtester_macd.py
│   ├── backtester_rsi.py
│   ├── backtester_bollinger.py
│   └── backtester_combined.py (ensemble)
│
├── Demo Scripts
│   └── demo_ta_intro.py (103-line interactive demo)
│
└── Practice Data
    └── 17 CSV files (various stocks/timeframes)
```

### Integration Points

**Cross-module Usage:**
1. Assignment notebook imports concepts from course materials
2. Backtester modules provide validation framework
3. Demo script illustrates library usage patterns
4. Practice data enables strategy testing

**No Direct Dependencies:**
- Assignment is self-contained (can run independently)
- Learning materials are reference only
- Backtester is optional validation tool

## Technology Stack

### Core Technologies

```
┌─────────────────────────────────────────────┐
│              PYTHON 3.x RUNTIME             │
├─────────────────────────────────────────────┤
│  Computation         Visualization          │
│  ├─ numpy            ├─ matplotlib          │
│  ├─ pandas           ├─ plotly              │
│  └─ scipy (optional) └─ cufflinks           │
├─────────────────────────────────────────────┤
│  Notebook Environment                       │
│  ├─ jupyter                                 │
│  ├─ jupyterlab                              │
│  ├─ ipykernel                               │
│  └─ ipywidgets                              │
├─────────────────────────────────────────────┤
│  Financial (reference)                      │
│  └─ yfinance                                │
├─────────────────────────────────────────────┤
│  Database (optional)                        │
│  └─ peewee                                  │
└─────────────────────────────────────────────┘
```

### Dependency Graph

```
Jupyter Notebook
    ├─→ IPython Kernel
    │    └─→ Python 3.x
    │
    ├─→ NumPy (data arrays)
    │    └─→ Pandas (DataFrames)
    │         └─→ Matplotlib (plotting)
    │              └─→ Plotly (interactive)
    │                   └─→ Cufflinks (pandas integration)
    │
    └─→ yfinance (external data - optional)
         └─→ requests (HTTP)
```

## Execution Environment

### Development Environment

**Local Setup:**
- OS: macOS/Linux/Windows
- Python: 3.8+
- Virtual environment: `.venv/`
- IDE: JupyterLab or Jupyter Notebook
- Browser: Chrome/Firefox/Safari (for notebook UI)

**Resource Requirements:**
- RAM: 2+ GB (for data processing)
- Storage: 100 MB (data + notebooks)
- CPU: Modern multi-core (for faster computation)

### Runtime Configuration

**Python Environment:**
```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter lab
# or
jupyter notebook
```

**Jupyter Configuration:**
- Kernel: Python 3 (ipykernel)
- Max output: Default (adjustable for large dataframes)
- Autosave: Enabled (periodic checkpoints)

## Performance Characteristics

### Computational Complexity

**Data Loading:** O(n) where n = 30 stocks
- Load time: ~100-500ms total

**Indicator Calculation:** O(n*m) where n = stocks, m = days
- SMA: O(m) per stock
- RSI: O(m) per stock
- MACD: O(m) per stock
- Total: O(30 * 242) ≈ 7260 operations

**Prediction:** O(n) where n = 30 stocks
- Per-stock prediction: ~1-10ms
- Total: ~30-300ms

**Visualization:** O(n*m) for rendering
- Dashboard creation: ~500ms-2s

### Memory Footprint

**Data Storage:**
- Single stock: (242 × 8) × 8 bytes = ~15 KB
- All stocks: 30 × 15 KB ≈ 450 KB
- With indicators: ~2-5 MB total

**Notebook Memory:**
- Base kernel: ~100-200 MB
- With data loaded: ~200-400 MB
- Peak (with visualizations): ~500 MB - 1 GB

### Scalability Considerations

**Current Scale:**
- 30 stocks (small dataset)
- 242 days (~1 year)
- 8 features per day
- Single-threaded processing

**Potential Optimizations:**
- Parallel processing (multiprocessing)
- Vectorized operations (NumPy/Pandas)
- Caching computed indicators
- Lazy evaluation for visualizations

## Security & Data Privacy

### Data Handling

**No External Transmission:**
- All data processed locally
- No network calls during prediction
- Results stay in notebook environment

**Read-only Data:**
- Original .npy files never modified
- Transformations in memory only
- No data persistence (unless explicitly saved)

### Code Safety

**Validated Inputs:**
- Data shape validation
- Range checking (return constraints)
- Error handling for file I/O

**No Credentials Required:**
- No API keys needed for assignment
- yfinance used only for reference (optional)

## Monitoring & Debugging

### Built-in Diagnostics

**Data Validation:**
```python
assert data.shape == (242, 8), "Invalid shape"
assert not np.isnan(data).any(), "Contains NaN"
```

**Performance Tracking:**
```python
import time
start = time.time()
# ... computation ...
elapsed = time.time() - start
print(f"Execution time: {elapsed:.2f}s")
```

**Error Handling:**
```python
try:
    data = load_stock_data(stock_id)
except FileNotFoundError:
    print(f"Stock {stock_id} not found")
except Exception as e:
    print(f"Error loading stock: {e}")
```

### Debugging Tools

**Jupyter Debugging:**
- `%debug` magic for post-mortem debugging
- `%%time` for cell execution timing
- `%pdb` for automatic debugger on exception

**Logging:**
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Processing stock s1")
```

## Deployment Architecture

### Local Deployment (Current)

```
Developer Machine
├── Python Virtual Environment (.venv/)
├── Jupyter Server (localhost:8888)
├── Stock Data Files (btl/*.npy)
└── Notebook (Sample Assignment.ipynb)
     └── Browser Interface
```

### Submission Architecture

```
Assignment Submission
├── Sample Assignment.ipynb (main file)
│    ├── All cells executed
│    ├── Outputs visible
│    └── Team member names filled
└── (Optional: PDF export for reference)
```

**Submission Format:**
- File: `.ipynb` (Jupyter notebook format)
- Delivery: LMS upload
- Validation: Instructor runs notebook with different test data

### Evaluation Architecture

```
Evaluation Environment
├── Grading Script
│    ├── Loads test dataset (different time interval)
│    ├── Executes cell 14 (prediction function)
│    └── Calculates performance metrics
│
├── Test Data (30 stocks, different period)
│    └── Same format: (N, 8) arrays
│
└── Metrics Calculation
     ├── Absolute error: |pred - actual|
     ├── Threshold check: error < 0.005
     └── Relative performance: score > 0
```

## Known Issues & Limitations

### Current Issues

1. **Cell 11 Bug**
   - Type: Undefined variable
   - Impact: Visualization breaks
   - Workaround: Skip cell or fix variable reference

2. **Empty Prediction Function (Cell 14)**
   - Type: Missing implementation
   - Impact: Cannot generate predictions
   - Status: Critical - requires implementation

### Architectural Limitations

1. **Static Dataset**
   - No real-time data updates
   - Fixed historical period
   - Cannot adapt to market changes

2. **Single-Threaded Processing**
   - Sequential stock processing
   - No parallel computation
   - Underutilized on multi-core systems

3. **Memory-Bound**
   - All data loaded in memory
   - Large visualizations consume RAM
   - No streaming or out-of-core processing

4. **No Model Persistence**
   - No trained model saving
   - Must recompute each session
   - No incremental learning

## Future Enhancements

### Short-term Improvements

1. Implement prediction function (cell 14)
2. Fix cell 11 visualization bug
3. Add cross-validation framework
4. Implement ensemble methods

### Long-term Architectural Changes

1. **Modular Architecture**
   - Separate modules for indicators, strategies, prediction
   - Reusable components
   - Unit test coverage

2. **Pipeline Architecture**
   - sklearn-style transformers
   - Composable feature engineering
   - Model stacking/ensembling

3. **Streaming Architecture**
   - Real-time data ingestion
   - Incremental model updates
   - Online learning capabilities

4. **Distributed Processing**
   - Parallel stock processing
   - GPU acceleration for ML models
   - Cloud deployment option
