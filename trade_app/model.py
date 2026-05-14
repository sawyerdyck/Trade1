from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class LinearTrendModel:
    """Simple one-dimensional linear trend forecaster."""

    coefficients: np.ndarray | None = None
    intercept: float | None = None

    def fit(self, values: list[float]) -> "LinearTrendModel":
        if len(values) < 2:
            raise ValueError("At least two values are required to fit the model.")

        x_values = np.arange(len(values), dtype=float)
        slope, intercept = np.polyfit(x_values, np.asarray(values, dtype=float), 1)
        self.coefficients = np.asarray([slope], dtype=float)
        self.intercept = float(intercept)
        return self

    def predict_next(self, values: list[float]) -> float:
        if self.coefficients is None or self.intercept is None:
            raise ValueError("Model must be fit before prediction.")
        next_index = float(len(values))
        slope = float(self.coefficients[0])
        return slope * next_index + self.intercept

    def predict_many(self, values: list[float], steps: int = 1) -> list[float]:
        if steps < 1:
            raise ValueError("steps must be at least 1.")
        predictions: list[float] = []
        current_values = list(values)
        for _ in range(steps):
            next_prediction = self.predict_next(current_values)
            predictions.append(next_prediction)
            current_values.append(next_prediction)
        return predictions
