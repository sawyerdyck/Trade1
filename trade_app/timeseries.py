from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from csv import DictReader
from io import StringIO
from typing import Any


@dataclass(frozen=True)
class TimeSeriesPoint:
    timestamp: datetime
    price: float


def _series_key(interval: str) -> str:
    return f"Time Series ({interval})"


def _resolve_series(payload: dict[str, Any], interval: str) -> tuple[str, dict[str, Any]]:
    preferred_key = _series_key(interval)
    preferred = payload.get(preferred_key)
    if isinstance(preferred, dict):
        return preferred_key, preferred

    candidates: list[str] = []
    for key, value in payload.items():
        if not isinstance(value, dict):
            continue
        if "Time Series" not in key:
            continue
        candidates.append(key)

    if not candidates:
        available_keys = ", ".join(payload.keys()) or "<none>"
        raise ValueError(
            f"Missing expected series key: {preferred_key}. "
            f"Available keys: {available_keys}"
        )

    fallback_key = next((key for key in candidates if interval in key), candidates[0])
    fallback_series = payload[fallback_key]
    return fallback_key, fallback_series


def _extract_open_price(values: dict[str, Any]) -> float | None:
    if "1. open" in values:
        return float(values["1. open"])

    # Handles alternative schemas such as crypto payloads with keys like
    # "1a. open (usd)".
    for key, raw_value in values.items():
        if "open" in key.lower():
            return float(raw_value)
    return None


def parse_intraday_points(payload: dict[str, Any], interval: str) -> list[TimeSeriesPoint]:
    _, series = _resolve_series(payload, interval)

    points: list[TimeSeriesPoint] = []
    for timestamp_text, values in series.items():
        if not isinstance(values, dict):
            continue
        raw_price = _extract_open_price(values)
        if raw_price is None:
            continue

        try:
            timestamp = datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Some endpoints provide date-only strings.
            timestamp = datetime.strptime(timestamp_text, "%Y-%m-%d")

        points.append(
            TimeSeriesPoint(
                timestamp=timestamp,
                price=raw_price,
            )
        )

    points.sort(key=lambda point: point.timestamp)
    return points


def parse_yahoo_chart_points(payload: dict[str, Any]) -> list[TimeSeriesPoint]:
    chart = payload.get("chart", {})
    results = chart.get("result")
    if not isinstance(results, list) or not results:
        raise ValueError("Yahoo payload did not include chart result data.")

    primary = results[0]
    timestamps = primary.get("timestamp")
    quote_entries = primary.get("indicators", {}).get("quote", [])
    if not isinstance(timestamps, list) or not quote_entries:
        raise ValueError("Yahoo payload did not include timestamp/quote data.")

    closes = quote_entries[0].get("close", [])
    points: list[TimeSeriesPoint] = []
    for ts, close in zip(timestamps, closes):
        if ts is None or close is None:
            continue
        points.append(
            TimeSeriesPoint(
                timestamp=datetime.fromtimestamp(ts, tz=timezone.utc).replace(tzinfo=None),
                price=float(close),
            )
        )

    points.sort(key=lambda point: point.timestamp)
    if not points:
        raise ValueError("Yahoo payload did not include usable price points.")
    return points


def parse_stooq_csv_points(csv_text: str) -> list[TimeSeriesPoint]:
    points: list[TimeSeriesPoint] = []
    reader = DictReader(StringIO(csv_text))
    for row in reader:
        date_text = row.get("Date")
        close_text = row.get("Close")
        if not date_text or not close_text:
            continue
        try:
            timestamp = datetime.strptime(date_text, "%Y-%m-%d")
            price = float(close_text)
        except ValueError:
            continue
        points.append(TimeSeriesPoint(timestamp=timestamp, price=price))

    points.sort(key=lambda point: point.timestamp)
    if not points:
        raise ValueError("Stooq CSV did not include usable price points.")
    return points


def parse_yfinance_history_points(history) -> list[TimeSeriesPoint]:
    points: list[TimeSeriesPoint] = []
    for timestamp, row in history.iterrows():
        close_value = row.get("Close")
        if close_value is None:
            continue
        if hasattr(timestamp, "to_pydatetime"):
            timestamp_value = timestamp.to_pydatetime()
        else:
            timestamp_value = timestamp
        if getattr(timestamp_value, "tzinfo", None) is not None:
            timestamp_value = timestamp_value.replace(tzinfo=None)
        points.append(TimeSeriesPoint(timestamp=timestamp_value, price=float(close_value)))

    points.sort(key=lambda point: point.timestamp)
    if not points:
        raise ValueError("yfinance history did not include usable price points.")
    return points


def points_to_vectors(points: list[TimeSeriesPoint]) -> tuple[list[float], list[float]]:
    timestamps = [point.timestamp.timestamp() for point in points]
    prices = [point.price for point in points]
    return timestamps, prices
