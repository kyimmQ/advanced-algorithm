# Strategies package
from .strategy_sma_gap_momentum import (
    sma,
    calculate_features,
    detect_anomalies,
    predict_returns,
    get_strategy_summary
)

__all__ = [
    'sma',
    'calculate_features',
    'detect_anomalies',
    'predict_returns',
    'get_strategy_summary'
]
