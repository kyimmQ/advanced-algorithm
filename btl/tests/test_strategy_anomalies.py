"""
Test Script - Anomaly Detection Analysis

This script tests the SMA Gap Momentum strategy by analyzing anomaly patterns
and printing detailed statistics about when the strategy signals contradict
actual price movements.

Usage:
    python test_strategy_anomalies.py              # Test on s1
    python test_strategy_anomalies.py --stock s5   # Test on specific stock
    python test_strategy_anomalies.py --all        # Test all 30 stocks
"""

import numpy as np
import pandas as pd
import argparse
import os
from datetime import datetime

# Import strategy module
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from strategies.strategy_sma_gap_momentum import (
    calculate_features,
    detect_anomalies,
    get_strategy_summary
)


def load_stock_data(stock_file, data_dir='sample_data'):
    """
    Load stock data from .npy file.

    Args:
        stock_file: Stock filename (e.g., 's1.npy' or 's1')
        data_dir: Directory containing stock data files

    Returns:
        Tuple of (prices, volumes, dates, full_data_array)
    """
    if not stock_file.endswith('.npy'):
        stock_file = f"{stock_file}.npy"

    # Handle relative path from tests directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    btl_dir = os.path.dirname(script_dir)
    filepath = os.path.join(btl_dir, data_dir, stock_file)

    A = np.load(filepath, allow_pickle=True)

    # Extract columns
    dates = A[:, 0]
    P = A[:, 2]  # Close prices
    V = A[:, 6]  # Volume

    return P, V, dates, A


def print_anomaly_summary(stock_name, df, summary):
    """
    Print detailed anomaly summary for a stock.

    Args:
        stock_name: Stock identifier
        df: DataFrame with features and anomaly detection
        summary: Summary statistics dictionary
    """
    print(f"\n{'='*70}")
    print(f"ANOMALY ANALYSIS: {stock_name}")
    print(f"{'='*70}")

    # Basic statistics
    print(f"\nTotal Trading Days: {summary['total_days']}")

    # Strategy signal distribution
    print(f"\nStrategy Signal Distribution:")
    print(f"  Strong Downtrend:  {summary['strong_downtrend_days']:3d} days")
    print(f"  Signal Uptrend:    {summary['signal_uptrend_days']:3d} days (recovery)")
    print(f"  Strong Uptrend:    {summary['strong_uptrend_days']:3d} days")
    print(f"  Signal Downtrend:  {summary['signal_downtrend_days']:3d} days (weakening)")

    # Anomaly statistics
    print(f"\nAnomaly Detection Results:")
    print(f"  Strong Downtrend Anomalies (price rose):    {summary['down_anomalies']:3d}")
    print(f"  Signal Downtrend Anomalies (price rose):    {summary['signaldown_anomalies']:3d}")
    print(f"  Signal Uptrend Anomalies (price dropped):   {summary['signalup_anomalies']:3d}")
    print(f"  Strong Uptrend Anomalies (price dropped):   {summary['up_anomalies']:3d}")
    print(f"  {'─'*68}")
    print(f"  Total Anomalies: {summary['total_anomalies']:3d} ({summary['total_anomalies']/summary['total_days']*100:.1f}% of days)")

    # Calculate anomaly rates per signal type
    print(f"\nAnomaly Rate by Signal Type:")
    if summary['strong_downtrend_days'] > 0:
        rate = summary['down_anomalies'] / summary['strong_downtrend_days'] * 100
        print(f"  Strong Downtrend:  {rate:5.1f}% anomaly rate")
    if summary['signal_downtrend_days'] > 0:
        rate = summary['signaldown_anomalies'] / summary['signal_downtrend_days'] * 100
        print(f"  Signal Downtrend:  {rate:5.1f}% anomaly rate")
    if summary['signal_uptrend_days'] > 0:
        rate = summary['signalup_anomalies'] / summary['signal_uptrend_days'] * 100
        print(f"  Signal Uptrend:    {rate:5.1f}% anomaly rate")
    if summary['strong_uptrend_days'] > 0:
        rate = summary['up_anomalies'] / summary['strong_uptrend_days'] * 100
        print(f"  Strong Uptrend:    {rate:5.1f}% anomaly rate")


def print_sample_anomalies(stock_name, df, dates, max_samples=5):
    """
    Print sample anomalies with detailed information.

    Args:
        stock_name: Stock identifier
        df: DataFrame with features and anomaly detection
        dates: Date array
        max_samples: Maximum number of samples to print per anomaly type
    """
    print(f"\n{'─'*70}")
    print(f"SAMPLE ANOMALIES (First {max_samples} per type)")
    print(f"{'─'*70}")
    print(f"Note: Signal on day i predicts price change from day i to day i+1")
    print(f"{'─'*70}")

    # Add dates to dataframe for display
    df['date'] = pd.to_datetime(dates.astype(int).astype(str), format='%Y%m%d', errors='coerce')

    anomaly_types = [
        ('Strat_Down_Anomaly', 'Strong Downtrend Anomaly (Next Day Price Rose)'),
        ('Strat_SignalDown_Anomaly', 'Signal Downtrend Anomaly (Next Day Price Rose)'),
        ('Strat_SignalUp_Anomaly', 'Signal Uptrend Anomaly (Next Day Price Dropped)'),
        ('Strat_Up_Anomaly', 'Strong Uptrend Anomaly (Next Day Price Dropped)')
    ]

    for anomaly_col, anomaly_name in anomaly_types:
        anomalies = df[df[anomaly_col]].head(max_samples)

        if len(anomalies) > 0:
            print(f"\n{anomaly_name}:")
            print(f"{'Date':<12} {'Signal':<20} {'Price':<10} {'Next Price':<12} {'Change':<10} {'Gap':<8}")
            print(f"{'-'*70}")

            for idx, row in anomalies.iterrows():
                date_str = row['date'].strftime('%Y-%m-%d') if pd.notna(row['date']) else 'N/A'
                # Show change from current day to next day
                price_change = ((row['Next_Price'] - row['price']) / row['price'] * 100) if pd.notna(row['Next_Price']) and row['price'] != 0 else 0
                signal = row['Strategy_Signal'][:18]  # Truncate long signal names

                print(f"{date_str:<12} {signal:<20} {row['price']:8.2f}  {row['Next_Price']:8.2f}     {price_change:6.2f}%  {row['SMA_Diff']:7.3f}")
        else:
            print(f"\n{anomaly_name}: None found")


def analyze_single_stock(stock_name, data_dir='sample_data', verbose=True):
    """
    Analyze anomalies for a single stock.

    Args:
        stock_name: Stock identifier (e.g., 's1')
        data_dir: Directory containing stock data
        verbose: If True, print detailed output

    Returns:
        Summary dictionary
    """
    # Load data
    P, V, dates, A = load_stock_data(stock_name, data_dir)

    # Calculate features
    df = calculate_features(P, V)

    # Detect anomalies
    df = detect_anomalies(df)

    # Get summary statistics
    summary = get_strategy_summary(df)
    summary['stock'] = stock_name

    if verbose:
        # Print summary
        print_anomaly_summary(stock_name, df, summary)

        # Print sample anomalies
        print_sample_anomalies(stock_name, df, dates, max_samples=5)

    return summary


def analyze_all_stocks(data_dir='sample_data'):
    """
    Analyze anomalies for all 30 stocks.

    Args:
        data_dir: Directory containing stock data

    Returns:
        DataFrame with summary for all stocks
    """
    results = []

    print(f"\n{'='*70}")
    print("ANALYZING ALL 30 STOCKS")
    print(f"{'='*70}\n")

    for i in range(1, 31):
        stock_name = f's{i}'
        try:
            # Analyze without verbose output for batch processing
            summary = analyze_single_stock(stock_name, data_dir, verbose=False)
            results.append(summary)

            # Show progress
            total_anom = summary['total_anomalies']
            anom_pct = total_anom / summary['total_days'] * 100
            print(f"  ✓ {stock_name}: {total_anom:3d} anomalies ({anom_pct:5.1f}%)")

        except Exception as e:
            print(f"  ✗ {stock_name}: ERROR - {str(e)}")

    # Create summary DataFrame
    df_results = pd.DataFrame(results)

    # Print aggregate statistics
    print(f"\n{'='*70}")
    print("AGGREGATE STATISTICS (30 Stocks)")
    print(f"{'='*70}")

    if len(df_results) > 0:
        print(f"\nAnomaly Counts (Average per stock):")
        print(f"  Strong Downtrend Anomalies: {df_results['down_anomalies'].mean():5.1f}")
        print(f"  Signal Downtrend Anomalies: {df_results['signaldown_anomalies'].mean():5.1f}")
        print(f"  Signal Uptrend Anomalies:   {df_results['signalup_anomalies'].mean():5.1f}")
        print(f"  Strong Uptrend Anomalies:   {df_results['up_anomalies'].mean():5.1f}")
        print(f"  Total Anomalies:            {df_results['total_anomalies'].mean():5.1f}")

        print(f"\nAnomaly Percentage (Average):")
        df_results['anomaly_pct'] = df_results['total_anomalies'] / df_results['total_days'] * 100
        print(f"  Mean:   {df_results['anomaly_pct'].mean():5.1f}%")
        print(f"  Median: {df_results['anomaly_pct'].median():5.1f}%")
        print(f"  Min:    {df_results['anomaly_pct'].min():5.1f}%")
        print(f"  Max:    {df_results['anomaly_pct'].max():5.1f}%")

    return df_results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Test SMA Gap Momentum Strategy - Anomaly Detection Analysis'
    )
    parser.add_argument(
        '--stock',
        type=str,
        default='s1',
        help='Stock name (e.g., s1, s2, ..., s30)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Analyze all 30 stocks'
    )
    parser.add_argument(
        '--data-dir',
        type=str,
        default='sample_data',
        help='Directory containing stock data files'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output CSV file for results (only for --all mode)'
    )

    args = parser.parse_args()

    if args.all:
        # Analyze all stocks
        results_df = analyze_all_stocks(args.data_dir)

        # Save results if output file specified
        if args.output:
            results_df.to_csv(args.output, index=False)
            print(f"\nResults saved to: {args.output}")
    else:
        # Analyze single stock
        analyze_single_stock(args.stock, args.data_dir, verbose=True)


if __name__ == '__main__':
    main()
