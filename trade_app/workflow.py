from __future__ import annotations

from .analysis import fit_linear_trend
from .client import AlphaVantageClient
from .config import AppConfig
from .plotting import plot_series
from .timeseries import parse_intraday_points, points_to_vectors


def load_market_points(config: AppConfig):
    client = AlphaVantageClient(api_key=config.api_key)
    payload = client.fetch_intraday(
        symbol=config.symbol,
        interval=config.interval,
        outputsize=config.outputsize,
    )
    return parse_intraday_points(payload, config.interval)


def run_pipeline(config: AppConfig) -> None:
    points = load_market_points(config)
    timestamps, prices = points_to_vectors(points)
    _, trend_line = fit_linear_trend(timestamps, prices)

    print([(point.timestamp, point.price) for point in points])
    plot_series(timestamps, prices, trend_line)
