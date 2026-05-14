from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

from .model import LinearTrendModel


@dataclass(frozen=True)
class BacktestResult:
    window_size: int
    observations: int
    mae: float
    mse: float
    directional_accuracy: float


def run_walk_forward_backtest(values: list[float], window_size: int = 20) -> BacktestResult:
    if window_size < 2:
        raise ValueError("window_size must be at least 2.")
    if len(values) <= window_size:
        raise ValueError("Not enough data points for the requested backtest window.")

    absolute_errors: list[float] = []
    squared_errors: list[float] = []
    correct_directions = 0
    total_predictions = 0

    for index in range(window_size, len(values)):
        train_window = values[index - window_size : index]
        actual_value = values[index]
        previous_value = values[index - 1]

        model = LinearTrendModel().fit(train_window)
        predicted_value = model.predict_next(train_window)

        error = predicted_value - actual_value
        absolute_errors.append(abs(error))
        squared_errors.append(error * error)
        if (predicted_value - train_window[-1]) * (actual_value - previous_value) >= 0:
            correct_directions += 1
        total_predictions += 1

    return BacktestResult(
        window_size=window_size,
        observations=total_predictions,
        mae=mean(absolute_errors),
        mse=mean(squared_errors),
        directional_accuracy=correct_directions / total_predictions,
    )
