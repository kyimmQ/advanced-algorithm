"""
SMA Gap Momentum Strategy Module

This module implements the SMA Gap Momentum strategy for stock return prediction.
The strategy analyzes the gap between SMA5 and SMA20 and its rate of change to
generate trading signals and predict next-day returns.

Strategy Signals:
- Strong Downtrend: Gap widening negatively (SMA5 moving further below SMA20)
- Signal Uptrend: Gap narrowing from negative (SMA5 recovering toward SMA20)
- Strong Uptrend: Gap widening positively (SMA5 moving further above SMA20)
- Signal Downtrend: Gap narrowing from positive (SMA5 declining toward SMA20)
"""

import numpy as np
import pandas as pd


def sma(data, n):
    """
    Calculate the simple moving average for n days.

    Args:
        data: Price data array
        n: Number of days for moving average window

    Returns:
        Array of SMA values with same length as input
    """
    return pd.Series(data).rolling(window=n, min_periods=1).mean().values


def calculate_features(P, V):
    """
    Calculate technical features for strategy.

    Args:
        P: Price array (close prices)
        V: Volume array

    Returns:
        DataFrame with calculated features including SMA5, SMA20, gap, and signals
    """
    df = pd.DataFrame({
        'price': P,
        'volume': V
    })

    # Calculate SMAs
    df['SMA5'] = sma(df['price'].values, 5)
    df['SMA20'] = sma(df['price'].values, 20)

    # Calculate gap and gap change
    df['SMA_Diff'] = df['SMA5'] - df['SMA20']
    df['Diff_Change'] = df['SMA_Diff'] - df['SMA_Diff'].shift(1)

    # Calculate previous price for anomaly detection
    df['Prev_Price'] = df['price'].shift(1)

    # Define strategy signals
    df['Strategy_Signal'] = df.apply(
        lambda row: _classify_signal(row['SMA_Diff'], row['Diff_Change']),
        axis=1
    )

    return df


def _classify_signal(diff, change):
    """
    Classify market signal based on SMA gap and gap change.

    Args:
        diff: SMA5 - SMA20 (the gap)
        change: Current gap - Previous gap (rate of change)

    Returns:
        Signal name string
    """
    if pd.isna(diff) or pd.isna(change):
        return 'Unknown'

    if diff < 0:  # Negative gap (SMA5 < SMA20)
        if change < 0:
            return 'Strong Downtrend'  # Gap widening negatively
        else:
            return 'Signal Uptrend'  # Gap narrowing (recovery)
    else:  # Positive gap (SMA5 >= SMA20)
        if change > 0:
            return 'Strong Uptrend'  # Gap widening positively
        else:
            return 'Signal Downtrend'  # Gap narrowing


def detect_anomalies(df):
    """
    Detect anomalies where price action contradicts strategy signal.

    The signal on day i should predict price movement from day i to day i+1.
    So we compare signal[i-1] with actual price change from day i-1 to day i.

    Args:
        df: DataFrame with features (from calculate_features)

    Returns:
        DataFrame with added anomaly columns
    """
    # Shift signals to align: signal[i-1] should predict change from i-1 to i
    df['Prev_Signal'] = df['Strategy_Signal'].shift(1)

    # Calculate next price for forward-looking comparison
    df['Next_Price'] = df['price'].shift(-1)

    # Anomaly: Strong Downtrend signal but next day price rose
    df['Strat_Down_Anomaly'] = (
        (df['Strategy_Signal'] == 'Strong Downtrend') &
        (df['Next_Price'] > df['price'])
    )

    # Anomaly: Signal Downtrend but next day price rose
    df['Strat_SignalDown_Anomaly'] = (
        (df['Strategy_Signal'] == 'Signal Downtrend') &
        (df['Next_Price'] > df['price'])
    )

    # Anomaly: Signal Uptrend but next day price dropped
    df['Strat_SignalUp_Anomaly'] = (
        (df['Strategy_Signal'] == 'Signal Uptrend') &
        (df['Next_Price'] < df['price'])
    )

    # Anomaly: Strong Uptrend but next day price dropped
    df['Strat_Up_Anomaly'] = (
        (df['Strategy_Signal'] == 'Strong Uptrend') &
        (df['Next_Price'] < df['price'])
    )

    return df


def predict_returns(P, V):
    """
    Predict next-day returns using SMA Gap Momentum strategy.

    This function implements the core prediction logic based on:
    - SMA gap momentum (trend strength)
    - Gap change rate (trend acceleration)
    - Volume patterns (confirmation)

    Args:
        P: Historical price array (close prices)
        V: Historical volume array

    Returns:
        Array of predicted returns for next day (same length as input)
        Returns are constrained to [-0.07, 0.07] range
    """
    def truncate(u):
        """Constrain return to valid market range [-7%, +7%]"""
        return np.clip(u, -0.07, 0.07)

    n = len(P)
    Q = [0]  # First day has no prediction

    # Calculate features for all historical data
    df = calculate_features(P, V)

    # For each day starting from day 1, predict next-day return
    for i in range(1, n):
        # Extract recent features
        sma_diff = df.loc[i, 'SMA_Diff']
        diff_change = df.loc[i, 'Diff_Change']
        signal = df.loc[i, 'Strategy_Signal']

        # Calculate momentum (5-day price change rate)
        if i >= 5:
            momentum = (P[i] - P[i-5]) / P[i-5]
        else:
            momentum = 0

        # Calculate volatility (5-day standard deviation)
        if i >= 5:
            volatility = np.std(P[max(0, i-5):i+1])
        else:
            volatility = 0

        # Calculate volume ratio (current volume vs 5-day average)
        if i >= 5:
            avg_volume = np.mean(V[max(0, i-5):i+1])
            volume_ratio = V[i] / avg_volume if avg_volume > 0 else 1.0
        else:
            volume_ratio = 1.0

        # Prediction logic based on signal and features
        if pd.isna(sma_diff) or pd.isna(diff_change):
            prediction = 0
        else:
            # Base prediction on gap momentum
            gap_strength = sma_diff / P[i] if P[i] > 0 else 0
            gap_acceleration = diff_change / P[i] if P[i] > 0 else 0

            # Combine signals with different weights
            if signal == 'Strong Uptrend':
                prediction = 0.6 * gap_strength + 0.3 * gap_acceleration + 0.1 * momentum
            elif signal == 'Signal Uptrend':
                prediction = 0.4 * gap_strength + 0.4 * gap_acceleration + 0.2 * momentum
            elif signal == 'Signal Downtrend':
                prediction = 0.4 * gap_strength + 0.4 * gap_acceleration - 0.2 * abs(momentum)
            elif signal == 'Strong Downtrend':
                prediction = 0.6 * gap_strength + 0.3 * gap_acceleration - 0.1 * abs(momentum)
            else:
                prediction = 0.5 * momentum

            # Adjust for volume confirmation
            if volume_ratio > 1.5:  # High volume confirms trend
                prediction *= 1.2
            elif volume_ratio < 0.7:  # Low volume weakens signal
                prediction *= 0.8

            # Adjust for volatility (higher volatility = more uncertainty)
            if volatility > 0:
                volatility_factor = min(1.0, 0.05 / volatility) if volatility > 0.05 else 1.0
                prediction *= volatility_factor

        # Constrain to valid range
        Q.append(truncate(prediction))

    return Q


def get_strategy_summary(df):
    """
    Generate summary statistics for the strategy.

    Args:
        df: DataFrame with anomaly detection results

    Returns:
        Dictionary with summary statistics
    """
    summary = {
        'total_days': len(df),
        'strong_downtrend_days': (df['Strategy_Signal'] == 'Strong Downtrend').sum(),
        'signal_uptrend_days': (df['Strategy_Signal'] == 'Signal Uptrend').sum(),
        'strong_uptrend_days': (df['Strategy_Signal'] == 'Strong Uptrend').sum(),
        'signal_downtrend_days': (df['Strategy_Signal'] == 'Signal Downtrend').sum(),
        'down_anomalies': df['Strat_Down_Anomaly'].sum(),
        'signaldown_anomalies': df['Strat_SignalDown_Anomaly'].sum(),
        'signalup_anomalies': df['Strat_SignalUp_Anomaly'].sum(),
        'up_anomalies': df['Strat_Up_Anomaly'].sum(),
    }

    summary['total_anomalies'] = (
        summary['down_anomalies'] +
        summary['signaldown_anomalies'] +
        summary['signalup_anomalies'] +
        summary['up_anomalies']
    )

    return summary
