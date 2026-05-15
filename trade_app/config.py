from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    symbol: str = "AAPL"
    interval: str = "1d"
    provider: str = "yfinance"
    yahoo_range: str = "6mo"
    api_key: str = ""
    outputsize: str = "compact"


def load_config() -> AppConfig:
    """Load runtime settings from environment variables.

    Environment variables:
    - STOCK_SYMBOL: market symbol to analyze.
    - STOCK_INTERVAL: chart interval supported by the selected provider.
    - STOCK_PROVIDER: data source. Defaults to yfinance.
    - YAHOO_RANGE: range for Yahoo chart API (e.g. 1mo, 3mo, 6mo, 1y).
    - ALPHAVANTAGE_API_KEY: only needed when STOCK_PROVIDER=alphavantage.
    - ALPHAVANTAGE_OUTPUTSIZE: compact or full.
    """

    return AppConfig(
        symbol=os.getenv("STOCK_SYMBOL", "AAPL"),
        interval=os.getenv("STOCK_INTERVAL", "1d"),
        provider=os.getenv("STOCK_PROVIDER", "yfinance").strip().lower(),
        yahoo_range=os.getenv("YAHOO_RANGE", "6mo").strip(),
        api_key=os.getenv("ALPHAVANTAGE_API_KEY", "").strip(),
        outputsize=os.getenv("ALPHAVANTAGE_OUTPUTSIZE", "compact"),
    )
