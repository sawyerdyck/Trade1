from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class TimeSeriesPoint:
    timestamp: datetime
    price: float


def _series_key(interval: str) -> str:
    return f"Time Series ({interval})"


def parse_intraday_points(payload: dict[str, Any], interval: str) -> list[TimeSeriesPoint]:
    key = _series_key(interval)
    series = payload.get(key)
    if not isinstance(series, dict):
        raise ValueError(f"Missing expected series key: {key}")

    points: list[TimeSeriesPoint] = []
    for timestamp_text, values in series.items():
        raw_price = values.get("1. open")
        if raw_price is None:
            continue

        points.append(
            TimeSeriesPoint(
                timestamp=datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S"),
                price=float(raw_price),
            )
        )

    points.sort(key=lambda point: point.timestamp)
    return points


def points_to_vectors(points: list[TimeSeriesPoint]) -> tuple[list[float], list[float]]:
    timestamps = [point.timestamp.timestamp() for point in points]
    prices = [point.price for point in points]
    return timestamps, prices
