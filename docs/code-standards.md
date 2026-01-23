# Code Standards & Structure

## Python Coding Conventions

### General Guidelines

1. **PEP 8 Compliance**
   - Line length: 79 characters (code), 72 (docstrings/comments)
   - Indentation: 4 spaces (no tabs)
   - Blank lines: 2 between functions/classes, 1 within functions
   - Imports: Standard library → third-party → local

2. **Naming Conventions**
   - Variables/functions: `snake_case` (e.g., `stock_data`, `calculate_sma`)
   - Classes: `PascalCase` (e.g., `BacktesterSMA`, `TradingStrategy`)
   - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETURN`, `NUM_STOCKS`)
   - Private: Leading underscore (e.g., `_internal_helper`)

3. **Import Organization**
   ```python
   # Standard library
   import os
   import sys
   from datetime import datetime

   # Third-party packages
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt
   import plotly.graph_objects as go

   # Local modules
   from backtester import BacktesterBase
   ```

### Data Handling Patterns

#### Loading Stock Data

**Standard Pattern:**
```python
import numpy as np

def load_stock_data(stock_id: int) -> np.ndarray:
    """
    Load stock data from .npy file.

    Args:
        stock_id: Stock identifier (1-30)

    Returns:
        NumPy array with shape (242, 8)
        Columns: date, open, close, low, high, nsh, volume, adjusted
    """
    filepath = f'btl/s{stock_id}.npy'
    data = np.load(filepath)
    return data
```

**Column Access:**
```python
# Use constants for column indices
DATE_COL = 0
OPEN_COL = 1
CLOSE_COL = 2
LOW_COL = 3
HIGH_COL = 4
NSH_COL = 5
VOLUME_COL = 6
ADJUSTED_COL = 7

# Extract columns
dates = data[:, DATE_COL]
close_prices = data[:, CLOSE_COL]
volumes = data[:, VOLUME_COL]
```

**Best Practice - Use Pandas:**
```python
def load_stock_as_dataframe(stock_id: int) -> pd.DataFrame:
    """Load stock data as pandas DataFrame with named columns."""
    data = np.load(f'btl/s{stock_id}.npy')
    df = pd.DataFrame(data, columns=[
        'date', 'open', 'close', 'low', 'high',
        'nsh', 'volume', 'adjusted'
    ])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df
```

#### Data Validation

**Always Validate Input:**
```python
def validate_stock_data(data: np.ndarray) -> bool:
    """
    Validate stock data format and integrity.

    Args:
        data: Stock data array

    Returns:
        True if valid, raises ValueError otherwise
    """
    # Check shape
    if data.shape != (242, 8):
        raise ValueError(f"Invalid shape {data.shape}, expected (242, 8)")

    # Check for NaN values
    if np.isnan(data).any():
        raise ValueError("Data contains NaN values")

    # Check price validity
    if (data[:, CLOSE_COL] <= 0).any():
        raise ValueError("Close prices must be positive")

    return True
```

### Technical Analysis Implementation

#### Indicator Calculation Pattern

**Template for Technical Indicators:**
```python
def calculate_sma(prices: np.ndarray, period: int = 20) -> np.ndarray:
    """
    Calculate Simple Moving Average.

    Args:
        prices: Array of prices (close prices)
        period: Moving average period (default 20)

    Returns:
        SMA values (same length as input, NaN for initial period-1 values)
    """
    if len(prices) < period:
        raise ValueError(f"Insufficient data: need {period}, got {len(prices)}")

    sma = np.full_like(prices, np.nan)
    for i in range(period - 1, len(prices)):
        sma[i] = np.mean(prices[i - period + 1:i + 1])

    return sma
```

**Vectorized Implementation (Preferred):**
```python
def calculate_sma_vectorized(prices: np.ndarray, period: int = 20) -> np.ndarray:
    """Calculate SMA using pandas for efficiency."""
    series = pd.Series(prices)
    sma = series.rolling(window=period).mean().values
    return sma
```

#### Multi-Period Analysis

**Standard Multi-Period Pattern:**
```python
def calculate_multiple_sma(prices: np.ndarray,
                          periods: list[int] = [20, 50, 200]) -> dict:
    """
    Calculate SMA for multiple periods.

    Args:
        prices: Price array
        periods: List of periods to calculate

    Returns:
        Dictionary mapping period to SMA array
    """
    sma_dict = {}
    for period in periods:
        sma_dict[f'sma_{period}'] = calculate_sma_vectorized(prices, period)
    return sma_dict
```

### Strategy Implementation

#### Signal Generation Pattern

**Buy/Sell Signal Template:**
```python
def generate_signals(data: pd.DataFrame,
                    indicator: np.ndarray,
                    threshold: float) -> pd.Series:
    """
    Generate trading signals based on indicator.

    Args:
        data: Stock data DataFrame
        indicator: Calculated indicator values
        threshold: Signal threshold

    Returns:
        Series with values: 1 (buy), -1 (sell), 0 (hold)
    """
    signals = pd.Series(0, index=data.index)

    # Buy signal
    signals[indicator > threshold] = 1

    # Sell signal
    signals[indicator < -threshold] = -1

    return signals
```

#### Crossover Strategy Pattern

**SMA Crossover Example:**
```python
def sma_crossover_signals(prices: np.ndarray,
                         short_period: int = 20,
                         long_period: int = 50) -> np.ndarray:
    """
    Generate signals from SMA crossover.

    Args:
        prices: Price array
        short_period: Short-term SMA period
        long_period: Long-term SMA period

    Returns:
        Signal array: 1 (bullish cross), -1 (bearish cross), 0 (no cross)
    """
    sma_short = calculate_sma_vectorized(prices, short_period)
    sma_long = calculate_sma_vectorized(prices, long_period)

    # Calculate crossover
    signals = np.zeros_like(prices)

    for i in range(1, len(prices)):
        # Bullish crossover: short crosses above long
        if sma_short[i-1] <= sma_long[i-1] and sma_short[i] > sma_long[i]:
            signals[i] = 1
        # Bearish crossover: short crosses below long
        elif sma_short[i-1] >= sma_long[i-1] and sma_short[i] < sma_long[i]:
            signals[i] = -1

    return signals
```

### Prediction Function Pattern

#### Core Prediction Structure

**Template for Cell 14:**
```python
def predict_next_return(prices: np.ndarray,
                       volumes: np.ndarray,
                       lookback: int = 20) -> float:
    """
    Predict next-day return using historical price and volume.

    Args:
        prices: Historical price array P[:-(n-1)]
        volumes: Historical volume array V[:-(n-1)]
        lookback: Number of historical days to use

    Returns:
        Predicted return for next day, constrained to [-0.07, 0.07]
    """
    # Feature engineering
    features = extract_features(prices, volumes, lookback)

    # Model prediction
    raw_prediction = model_predict(features)

    # Constrain to [-7%, +7%]
    predicted_return = np.clip(raw_prediction, -0.07, 0.07)

    return predicted_return


def extract_features(prices: np.ndarray,
                    volumes: np.ndarray,
                    lookback: int) -> dict:
    """Extract technical features for prediction."""
    features = {}

    # Price features
    features['momentum'] = (prices[-1] - prices[-lookback]) / prices[-lookback]
    features['volatility'] = np.std(prices[-lookback:])
    features['sma_ratio'] = prices[-1] / np.mean(prices[-lookback:])

    # Volume features
    features['volume_ratio'] = volumes[-1] / np.mean(volumes[-lookback:])
    features['volume_trend'] = np.polyfit(range(lookback), volumes[-lookback:], 1)[0]

    # Technical indicators
    features['rsi'] = calculate_rsi(prices)[-1]
    features['macd'] = calculate_macd(prices)[-1]

    return features
```

### Error Handling

#### Defensive Programming

**Always Handle Edge Cases:**
```python
def safe_divide(numerator: float, denominator: float,
                default: float = 0.0) -> float:
    """Safely divide with default for zero denominator."""
    return numerator / denominator if denominator != 0 else default


def safe_log_return(price_current: float, price_previous: float) -> float:
    """Calculate log return with safety checks."""
    if price_previous <= 0 or price_current <= 0:
        return 0.0
    return np.log(price_current / price_previous)
```

**Try-Except for Data Loading:**
```python
def load_all_stocks(num_stocks: int = 30) -> dict:
    """Load all stock data with error handling."""
    stock_data = {}

    for i in range(1, num_stocks + 1):
        try:
            data = load_stock_data(i)
            validate_stock_data(data)
            stock_data[f's{i}'] = data
        except FileNotFoundError:
            print(f"Warning: Stock s{i} not found")
        except ValueError as e:
            print(f"Warning: Stock s{i} validation failed: {e}")

    return stock_data
```

## Jupyter Notebook Organization

### Cell Structure

**Standard Notebook Layout:**

1. **Setup Cells (1-2)**
   ```python
   # Cell 1: Imports
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt
   import plotly.graph_objects as go

   # Cell 2: Configuration
   NUM_STOCKS = 30
   NUM_DAYS = 242
   MAX_RETURN = 0.07
   MIN_RETURN = -0.07
   ```

2. **Data Loading Cells (3-4)**
   ```python
   # Cell 3: Load single stock (example)
   sample_stock = load_stock_data(1)

   # Cell 4: Load all stocks
   all_stocks = load_all_stocks()
   ```

3. **Analysis Cells (5-13)**
   - One cell per major analysis step
   - Clear markdown headers
   - Inline visualizations

4. **Prediction Cell (14)**
   - Core prediction function
   - Batch processing for all stocks
   - Result compilation

5. **Evaluation Cells (15+)**
   - Performance metrics
   - Result visualization
   - Summary statistics

### Markdown Documentation

**Cell Headers:**
```markdown
# Section: Data Loading

## Purpose
Load and validate stock data for 30 stocks.

## Inputs
- Stock data files: s1.npy to s30.npy

## Outputs
- `all_stocks`: Dictionary of stock data
- Shape: 30 stocks × (242, 8)
```

**Inline Comments:**
```python
# Calculate 20-day SMA for trend identification
sma_20 = calculate_sma_vectorized(close_prices, period=20)

# Identify bullish trend: price > SMA
bullish_signals = close_prices > sma_20
```

### Output Management

**Suppress Unnecessary Output:**
```python
# Use semicolon to suppress output
fig = plt.figure();

# Or assign to variable
_ = data.head()
```

**Display Key Results:**
```python
# Show important metrics
print(f"Mean Absolute Error: {mae:.4f}")
print(f"Directional Accuracy: {accuracy:.2%}")

# Display dataframes
display(results_df.head(10))
```

## Testing & Validation

### Unit Testing Pattern

**Test Functions (for modules):**
```python
import unittest

class TestTechnicalIndicators(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.prices = np.array([100, 102, 101, 103, 105, 104, 106])

    def test_sma_calculation(self):
        """Test SMA calculation accuracy."""
        sma = calculate_sma(self.prices, period=3)
        expected = np.array([np.nan, np.nan, 101, 102, 103, 104, 105])
        np.testing.assert_array_almost_equal(sma, expected)

    def test_sma_edge_cases(self):
        """Test SMA with edge cases."""
        # Insufficient data
        with self.assertRaises(ValueError):
            calculate_sma(self.prices[:2], period=3)
```

### Validation in Notebooks

**Inline Validation:**
```python
# Validate data shape
assert all_stocks['s1'].shape == (242, 8), "Invalid data shape"

# Validate return range
predicted_returns = predict_all_stocks(all_stocks)
assert np.all(predicted_returns >= -0.07), "Returns below minimum"
assert np.all(predicted_returns <= 0.07), "Returns above maximum"

print("✓ All validations passed")
```

### Performance Validation

**Metrics Calculation:**
```python
def evaluate_predictions(y_true: np.ndarray,
                        y_pred: np.ndarray) -> dict:
    """
    Calculate evaluation metrics.

    Args:
        y_true: Actual returns
        y_pred: Predicted returns

    Returns:
        Dictionary of metrics
    """
    metrics = {}

    # Absolute error
    metrics['mae'] = np.mean(np.abs(y_true - y_pred))
    metrics['rmse'] = np.sqrt(np.mean((y_true - y_pred) ** 2))

    # Directional accuracy
    direction_correct = np.sign(y_true) == np.sign(y_pred)
    metrics['direction_accuracy'] = np.mean(direction_correct)

    # Assignment criteria
    metrics['abs_error_pass'] = metrics['mae'] < 0.005

    return metrics
```

## Visualization Standards

### Matplotlib Conventions

**Standard Plot Setup:**
```python
import matplotlib.pyplot as plt

def plot_stock_price(dates, prices, title="Stock Price"):
    """Standard stock price plot."""
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(dates, prices, linewidth=2, color='#2E86AB')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig, ax
```

### Plotly Conventions

**Interactive Chart Pattern:**
```python
import plotly.graph_objects as go

def create_candlestick_chart(df: pd.DataFrame, title: str = "Stock Chart"):
    """Create interactive candlestick chart."""
    fig = go.Figure(data=[
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='OHLC'
        )
    ])

    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_white',
        height=600
    )

    return fig
```

**Multi-Subplot Dashboard:**
```python
from plotly.subplots import make_subplots

def create_dashboard(df: pd.DataFrame):
    """Create multi-panel dashboard."""
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Price', 'Volume', 'Indicators'),
        row_heights=[0.5, 0.25, 0.25],
        shared_xaxes=True
    )

    # Price panel
    fig.add_trace(
        go.Scatter(x=df.index, y=df['close'], name='Close'),
        row=1, col=1
    )

    # Volume panel
    fig.add_trace(
        go.Bar(x=df.index, y=df['volume'], name='Volume'),
        row=2, col=1
    )

    # Indicators panel
    fig.add_trace(
        go.Scatter(x=df.index, y=df['sma_20'], name='SMA-20'),
        row=3, col=1
    )

    fig.update_layout(height=900, showlegend=True)
    return fig
```

## Performance Optimization

### NumPy Best Practices

**Vectorization Over Loops:**
```python
# Bad: Loop-based
returns = []
for i in range(1, len(prices)):
    returns.append((prices[i] - prices[i-1]) / prices[i-1])

# Good: Vectorized
returns = (prices[1:] - prices[:-1]) / prices[:-1]
```

**Preallocate Arrays:**
```python
# Bad: Append in loop
results = []
for i in range(1000):
    results.append(calculate(i))

# Good: Preallocate
results = np.empty(1000)
for i in range(1000):
    results[i] = calculate(i)
```

### Pandas Optimization

**Use Built-in Methods:**
```python
# Calculate returns
df['return'] = df['close'].pct_change()

# Rolling operations
df['sma_20'] = df['close'].rolling(window=20).mean()
df['volatility'] = df['return'].rolling(window=20).std()
```

## Constants & Configuration

**Define Constants at Top:**
```python
# Data constants
NUM_STOCKS = 30
NUM_TRADING_DAYS = 242
NUM_FEATURES = 8

# Column indices
COL_DATE = 0
COL_OPEN = 1
COL_CLOSE = 2
COL_LOW = 3
COL_HIGH = 4
COL_NSH = 5
COL_VOLUME = 6
COL_ADJUSTED = 7

# Prediction constraints
MAX_RETURN = 0.07
MIN_RETURN = -0.07

# Technical analysis parameters
SMA_SHORT_PERIOD = 20
SMA_LONG_PERIOD = 50
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
```

## Documentation Standards

### Docstring Format

**Use NumPy Style:**
```python
def calculate_technical_indicators(data: pd.DataFrame,
                                   indicators: list[str]) -> pd.DataFrame:
    """
    Calculate multiple technical indicators.

    Parameters
    ----------
    data : pd.DataFrame
        Stock data with OHLCV columns
    indicators : list of str
        List of indicators to calculate: ['sma', 'ema', 'rsi', 'macd']

    Returns
    -------
    pd.DataFrame
        Input data with additional indicator columns

    Raises
    ------
    ValueError
        If unknown indicator requested

    Examples
    --------
    >>> df = load_stock_as_dataframe(1)
    >>> df_with_indicators = calculate_technical_indicators(df, ['sma', 'rsi'])
    >>> print(df_with_indicators.columns)
    Index(['open', 'close', 'low', 'high', 'volume', 'sma_20', 'rsi_14'], dtype='object')
    """
    pass
```

### Code Comments

**Comment Why, Not What:**
```python
# Good: Explains reasoning
# Use log returns for better statistical properties
log_returns = np.log(prices[1:] / prices[:-1])

# Bad: States the obvious
# Calculate log of price ratio
log_returns = np.log(prices[1:] / prices[:-1])
```

## Version Control

### Commit Messages

**Format:**
```
<type>: <short summary>

<detailed description>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code restructuring
- `test`: Test addition/modification
- `perf`: Performance improvement

**Example:**
```
feat: Implement prediction function in cell 14

Add core forecasting logic using SMA crossover and RSI indicators.
Includes feature extraction, model prediction, and return clipping.

Closes #1
```

## Code Quality Checklist

Before submitting/committing:

- [ ] All cells execute without errors
- [ ] No undefined variables
- [ ] Proper error handling
- [ ] Input validation included
- [ ] Docstrings for all functions
- [ ] Clear variable names
- [ ] Constants defined at top
- [ ] No magic numbers in code
- [ ] Efficient algorithms (vectorized)
- [ ] Results validated
- [ ] Team member names filled in
- [ ] Outputs are meaningful
- [ ] Visualizations have titles/labels
- [ ] Code follows PEP 8
- [ ] No unused imports
