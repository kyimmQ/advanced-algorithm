# Project Overview & Product Development Requirements

## Project Identity

**Name:** Stock Price Forecasting - CO5115 Assignment
**Institution:** HCMUT (Ho Chi Minh University of Technology)
**Course:** CO5115 - Technical Analysis with Python
**Instructor:** vinhpham@hcmut.edu.vn
**Type:** Academic Assignment - Stock Return Prediction
**Status:** In Progress

## Project Objective

Develop a forecasting model to predict next-day stock returns using historical OHLCV (Open, High, Low, Close, Volume) data for 30 stocks.

### Core Problem Statement

```
Given: P[: -(n-1)], V[: -(n-1)]  (historical price & volume data)
Predict: Return[n]                (next-day return)

Where:
- P = price data (open, close, low, high, adjusted)
- V = volume data (number of shares, volume)
- n = trading day index
- Return range: [-7%, +7%]
```

## Assignment Requirements

### Functional Requirements

1. **Data Processing**
   - Load and process 30 stock datasets (s1.npy to s30.npy)
   - Handle 242 trading days per stock (~1 year historical data)
   - Extract 8 features: date, open, close, low, high, nsh, volume, adjusted

2. **Technical Analysis Implementation**
   - Apply technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands, etc.)
   - Detect market patterns (anomalies, gaps, trends)
   - Generate trading signals and strategies

3. **Forecasting Model**
   - Implement prediction function in cell 14 of `Sample Assignment.ipynb`
   - Use historical price/volume to forecast next-day returns
   - Support batch prediction for 30 stocks

4. **Deliverable**
   - Customized Jupyter notebook with team member names
   - Working prediction function
   - Documentation of methodology and approach

### Non-Functional Requirements

1. **Performance Metrics**
   - Absolute error: `|predicted - actual| < 0.005`
   - Relative performance: `relative_score > 0`
   - Tested on different time interval, same 30 stocks

2. **Code Quality**
   - Clean, readable Python code
   - Proper use of numpy, pandas, matplotlib, plotly
   - Follow Jupyter notebook best practices

3. **Reproducibility**
   - Deterministic results
   - Clear methodology documentation
   - Reusable code structure

## Current Implementation Status

### Completed Components

1. **Data Loading & Exploration** (Cells 1-6)
   - Successfully loads 30 stock datasets
   - Extracts OHLCV features
   - Basic data visualization

2. **Technical Indicators** (Cells 7-10)
   - Simple Moving Average (SMA) trend detection
   - Anomaly detection using statistical thresholds
   - Gap momentum strategy implementation

3. **Visualization Dashboard** (Cells 11-13)
   - Plotly-based interactive charts
   - Multiple subplot layout
   - Price, volume, and indicator overlays

### In Progress

1. **Prediction Function** (Cell 14)
   - Currently empty, awaiting implementation
   - Core requirement for assignment completion
   - Should return predicted returns for next trading day

### Known Issues

1. **Bug in Cell 11**
   - Undefined variable reference
   - Affects visualization rendering
   - Needs debugging and fix

## Success Criteria

### Acceptance Criteria

- [ ] All 30 stocks processed successfully
- [ ] Prediction function implemented and working
- [ ] Absolute error < 0.005 on test set
- [ ] Relative performance > 0
- [ ] No runtime errors in notebook
- [ ] Team member names filled in
- [ ] Code properly documented

### Evaluation Metrics

1. **Accuracy Metrics**
   - Mean Absolute Error (MAE)
   - Mean Squared Error (MSE)
   - Directional Accuracy (up/down prediction)

2. **Performance Metrics**
   - Absolute prediction error threshold
   - Relative performance vs baseline
   - Consistency across 30 stocks

3. **Code Quality**
   - Notebook executes end-to-end without errors
   - Clear comments and explanations
   - Proper use of libraries and methods

## Timeline & Milestones

### Development Phases

1. **Phase 1: Foundation** ✅ COMPLETED
   - Data loading and exploration
   - Basic technical indicators
   - Visualization setup

2. **Phase 2: Strategy Development** ⏳ IN PROGRESS
   - Advanced technical indicators
   - Pattern recognition
   - Feature engineering

3. **Phase 3: Model Implementation** 🔜 UPCOMING
   - Prediction function development
   - Model training and validation
   - Performance optimization

4. **Phase 4: Testing & Refinement** 🔜 UPCOMING
   - Bug fixes (cell 11)
   - Performance tuning
   - Documentation completion

5. **Phase 5: Submission** 🔜 UPCOMING
   - Final testing
   - Team member names
   - Notebook cleanup and submission

### Key Dates

- **Project Start:** 2026-01-20 (initial implementation session)
- **Current Status:** Phase 2 - Strategy Development
- **Submission Deadline:** TBD (check LMS system)

## Team Composition

**Team Members:** TBD (to be filled in notebook)
**Group Size:** TBD
**Collaboration Model:** Group assignment

## Technical Constraints

### Dependencies

- Python 3.x with scientific computing stack
- 123 packages (see requirements.txt)
- Jupyter notebook environment

### Data Constraints

- Fixed dataset: 30 stocks, 242 days each
- Historical data only (no real-time feeds)
- Return range limited to [-7%, +7%]

### Computational Constraints

- Must run in standard Jupyter environment
- No external API dependencies for submission
- Reasonable execution time for grading

## Risks & Mitigation

### Technical Risks

1. **Overfitting Risk**
   - Mitigation: Cross-validation, simple models, regularization

2. **Data Quality Issues**
   - Mitigation: Anomaly detection, data validation, outlier handling

3. **Performance Degradation**
   - Mitigation: Test on separate interval, ensemble methods

### Project Risks

1. **Incomplete Prediction Function**
   - Mitigation: Prioritize core functionality, iterative development

2. **Known Bugs**
   - Mitigation: Debug cell 11, systematic testing

3. **Time Constraints**
   - Mitigation: Focus on working solution first, optimization second

## References & Resources

### Course Materials

- 48 files in `learn/` directory
- 21 Jupyter notebooks covering TA concepts
- 7 OOP backtester modules
- 17 CSV datasets for practice

### Key Learning Resources

1. **Technical Indicators:** SMA, EMA, MACD, RSI, Stochastic, Bollinger Bands
2. **Pattern Recognition:** Pivot Points, Fibonacci, Gaps, Anomalies
3. **Backtesting:** OOP framework for strategy validation
4. **Visualization:** Plotly, QuantFig for interactive charts

### External Libraries

- `yfinance`: Yahoo Finance data (for reference only)
- `cufflinks`: Plotly integration for pandas
- `numpy`, `pandas`: Data manipulation
- `matplotlib`, `plotly`: Visualization

## Deliverable Specifications

### Notebook Structure

1. **Header Section**
   - Team member names
   - Assignment metadata

2. **Data Loading**
   - Load 30 stock datasets
   - Extract features

3. **Analysis Section**
   - Technical indicators
   - Pattern detection
   - Strategy development

4. **Prediction Section**
   - Core prediction function (cell 14)
   - Model implementation
   - Result generation

5. **Visualization**
   - Interactive charts
   - Performance metrics
   - Result summary

### Submission Format

- File: `Sample Assignment.ipynb` (customized)
- Format: Jupyter notebook (.ipynb)
- Submission: Via LMS system
- Content: Code + results + team names

## Notes

- Evaluation on different time interval ensures generalization
- Focus on robust methodology over overfitting to training data
- Course materials provide comprehensive TA toolkit
- Backtester framework available for strategy validation
