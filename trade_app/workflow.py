from __future__ import annotations

from .analysis import fit_linear_trend
from .client import AlphaVantageClient, StooqClient, YahooFinanceClient, YFinanceClient
from .config import AppConfig
from .plotting import plot_series
from .timeseries import parse_intraday_points, parse_stooq_csv_points, parse_yahoo_chart_points, parse_yfinance_history_points, points_to_vectors


def load_market_points(config: AppConfig):
    if config.provider == "yfinance":
        client = YFinanceClient()
        history = client.fetch_history(
            symbol=config.symbol,
            interval=config.interval,
            period=config.yahoo_range,
        )
        return parse_yfinance_history_points(history)

    if config.provider == "stooq":
        client = StooqClient()
        csv_text = client.fetch_daily_csv(symbol=config.symbol)
        return parse_stooq_csv_points(csv_text)

    if config.provider == "alphavantage":
        client = AlphaVantageClient(api_key=config.api_key)
        payload = client.fetch_intraday(
            symbol=config.symbol,
            interval=config.interval,
            outputsize=config.outputsize,
        )
        return parse_intraday_points(payload, config.interval)

    yahoo_client = YahooFinanceClient()
    yahoo_payload = yahoo_client.fetch_chart(
        symbol=config.symbol,
        interval=config.interval,
        range_value=config.yahoo_range,
    )
    return parse_yahoo_chart_points(yahoo_payload)


def run_pipeline(config: AppConfig) -> None:
    points = load_market_points(config)
    timestamps, prices = points_to_vectors(points)
    _, trend_line = fit_linear_trend(timestamps, prices)

    print([(point.timestamp, point.price) for point in points])
    plot_series(timestamps, prices, trend_line)
