from __future__ import annotations

import numpy as np


def fit_linear_trend(x_values: list[float], y_values: list[float]) -> tuple[np.ndarray, np.poly1d]:
    if len(x_values) < 2 or len(y_values) < 2:
        raise ValueError("At least two data points are required for trend fitting.")
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length.")

    coefficients = np.polyfit(x_values, y_values, 1)
    trend_line = np.poly1d(coefficients)
    return coefficients, trend_line
