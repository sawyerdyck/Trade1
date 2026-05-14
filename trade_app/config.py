from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AppConfig:
    symbol: str = "BTC"
    interval: str = "1min"
    api_key: str = ""
    outputsize: str = "compact"


def load_config() -> AppConfig:
    """Load runtime settings from environment variables.

    Environment variables:
    - ALPHAVANTAGE_API_KEY: required for real Alpha Vantage requests.
    - STOCK_SYMBOL: market symbol to analyze.
    - STOCK_INTERVAL: intraday interval supported by Alpha Vantage.
    - ALPHAVANTAGE_OUTPUTSIZE: compact or full.
    """

    return AppConfig(
        symbol=os.getenv("STOCK_SYMBOL", "BTC"),
        interval=os.getenv("STOCK_INTERVAL", "1min"),
        api_key=os.getenv("ALPHAVANTAGE_API_KEY", "").strip(),
        outputsize=os.getenv("ALPHAVANTAGE_OUTPUTSIZE", "compact"),
    )
