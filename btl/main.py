"""
Main Script - Stock Return Prediction

This script loads stock data, applies the SMA Gap Momentum strategy,
generates predictions, and evaluates performance.

Usage:
    python main.py                    # Run on single stock (s1)
    python main.py --stock s5         # Run on specific stock
    python main.py --all              # Run on all 30 stocks
    python main.py --stock s1 --plot  # Run with visualization
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
from pathlib import Path

# Import strategy module
from strategies.strategy_sma_gap_momentum import predict_returns


def load_stock_data(stock_file, data_dir='sample_data'):
    """
    Load stock data from .npy file.

    Args:
        stock_file: Stock filename (e.g., 's1.npy' or 's1')
        data_dir: Directory containing stock data files

    Returns:
        Tuple of (prices, volumes, full_data_array)
    """
    # Ensure .npy extension
    if not stock_file.endswith('.npy'):
        stock_file = f"{stock_file}.npy"

    filepath = os.path.join(data_dir, stock_file)

    # Load data
    A = np.load(filepath, allow_pickle=True)

    # Extract columns
    # Column indices: [0: date, 1: open, 2: close, 3: low, 4: high, 5: nsh, 6: volume, 7: adjusted]
    P = A[:, 2]  # Close prices
    V = A[:, 6]  # Volume

    return P, V, A


def target(P, V):
    """
    Calculate actual returns (ground truth).

    Args:
        P: Price array
        V: Volume array (not used, included for signature compatibility)

    Returns:
        Array of actual returns
    """
    n, Q = len(P), [0]
    for i in range(1, n):
        Q.append(P[i] / P[i - 1] - 1)
    return Q


def evaluate(p, t, display=False):
    """
    Evaluate prediction performance.

    Args:
        p: Predicted returns array
        t: Target (actual) returns array
        display: If True, print results and show histogram

    Returns:
        Tuple of (absolute_error, relative_score)

    Evaluation Criteria:
        - absolute_error < 0.005 is good
        - relative_score > 0 indicates positive signal
    """
    p, t = p[1:], t[1:]
    n, e, f = len(t), [], []

    for i in range(1, n):
        e.append(t[i] - p[i - 1])
        f.append(t[i])

    den = np.nanquantile(np.abs(e), 0.5) + 0.5 * np.nanquantile(np.abs(e), 0.9)
    num = np.nanquantile(np.abs(f), 0.5) + 0.5 * np.nanquantile(np.abs(f), 0.9)

    if display:
        print(f"\n\tbase = {round(num, 3)}  |  abs = {round(den, 3)}  |  rel = {round(1 - den / num, 3)}\n")
        plt.figure(figsize=(10, 6))
        plt.hist(e, bins=30, edgecolor='black', alpha=0.7)
        plt.xlabel('Prediction Error')
        plt.ylabel('Frequency')
        plt.title('Distribution of Prediction Errors')
        plt.grid(True, alpha=0.3)
        plt.show()

    return den, 1 - den / num


def run_single_stock(stock_name, data_dir='sample_data', display=True):
    """
    Run prediction on a single stock.

    Args:
        stock_name: Stock identifier (e.g., 's1')
        data_dir: Directory containing stock data
        display: If True, show evaluation results

    Returns:
        Tuple of (absolute_error, relative_score)
    """
    print(f"\n{'='*60}")
    print(f"Processing Stock: {stock_name}")
    print(f"{'='*60}")

    # Load data
    P, V, A = load_stock_data(stock_name, data_dir)
    print(f"Loaded {len(P)} trading days")

    # Generate predictions
    print("Generating predictions using SMA Gap Momentum strategy...")
    predictions = predict_returns(P, V)

    # Calculate actual returns
    actual_returns = target(P, V)

    # Evaluate performance
    print("Evaluating performance...")
    abs_error, rel_score = evaluate(predictions, actual_returns, display=display)

    # Performance summary
    print(f"\nPerformance Summary:")
    print(f"  Absolute Error: {abs_error:.6f} {'✓ PASS' if abs_error < 0.005 else '✗ FAIL'} (target: < 0.005)")
    print(f"  Relative Score: {rel_score:.6f} {'✓ PASS' if rel_score > 0 else '✗ FAIL'} (target: > 0)")

    return abs_error, rel_score


def run_all_stocks(data_dir='sample_data'):
    """
    Run prediction on all 30 stocks.

    Args:
        data_dir: Directory containing stock data

    Returns:
        DataFrame with results for all stocks
    """
    results = []

    print(f"\n{'='*60}")
    print(f"Processing All 30 Stocks")
    print(f"{'='*60}\n")

    for i in range(1, 31):
        stock_name = f's{i}'
        try:
            # Run without display for batch processing
            abs_error, rel_score = run_single_stock(stock_name, data_dir, display=False)

            results.append({
                'stock': stock_name,
                'abs_error': abs_error,
                'rel_score': rel_score,
                'abs_pass': abs_error < 0.005,
                'rel_pass': rel_score > 0
            })

            # Show progress
            status = '✓' if (abs_error < 0.005 and rel_score > 0) else '✗'
            print(f"  {status} {stock_name}: abs={abs_error:.6f}, rel={rel_score:.6f}")

        except Exception as e:
            print(f"  ✗ {stock_name}: ERROR - {str(e)}")
            results.append({
                'stock': stock_name,
                'abs_error': None,
                'rel_score': None,
                'abs_pass': False,
                'rel_pass': False
            })

    # Create summary DataFrame
    df_results = pd.DataFrame(results)

    # Print summary statistics
    print(f"\n{'='*60}")
    print("SUMMARY STATISTICS")
    print(f"{'='*60}")

    valid_results = df_results.dropna()
    if len(valid_results) > 0:
        print(f"\nSuccessfully processed: {len(valid_results)}/30 stocks")
        print(f"\nAbsolute Error:")
        print(f"  Mean:   {valid_results['abs_error'].mean():.6f}")
        print(f"  Median: {valid_results['abs_error'].median():.6f}")
        print(f"  Min:    {valid_results['abs_error'].min():.6f}")
        print(f"  Max:    {valid_results['abs_error'].max():.6f}")
        print(f"  Passed: {valid_results['abs_pass'].sum()}/30 stocks")

        print(f"\nRelative Score:")
        print(f"  Mean:   {valid_results['rel_score'].mean():.6f}")
        print(f"  Median: {valid_results['rel_score'].median():.6f}")
        print(f"  Min:    {valid_results['rel_score'].min():.6f}")
        print(f"  Max:    {valid_results['rel_score'].max():.6f}")
        print(f"  Passed: {valid_results['rel_pass'].sum()}/30 stocks")

        both_pass = (valid_results['abs_pass'] & valid_results['rel_pass']).sum()
        print(f"\nOverall:")
        print(f"  Both criteria passed: {both_pass}/30 stocks ({both_pass/30*100:.1f}%)")

    return df_results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Stock Return Prediction using SMA Gap Momentum Strategy'
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
        help='Run on all 30 stocks'
    )
    parser.add_argument(
        '--data-dir',
        type=str,
        default='sample_data',
        help='Directory containing stock data files'
    )
    parser.add_argument(
        '--no-plot',
        action='store_true',
        help='Disable plotting'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output CSV file for results (only for --all mode)'
    )

    args = parser.parse_args()

    if args.all:
        # Run on all stocks
        results_df = run_all_stocks(args.data_dir)

        # Save results if output file specified
        if args.output:
            results_df.to_csv(args.output, index=False)
            print(f"\nResults saved to: {args.output}")
    else:
        # Run on single stock
        run_single_stock(args.stock, args.data_dir, display=not args.no_plot)


if __name__ == '__main__':
    main()
