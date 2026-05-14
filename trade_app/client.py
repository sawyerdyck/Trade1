from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


class AlphaVantageError(RuntimeError):
    """Raised when Alpha Vantage returns an error or unexpected payload."""


@dataclass(frozen=True)
class AlphaVantageClient:
    api_key: str
    base_url: str = "https://www.alphavantage.co/query"

    def fetch_intraday(self, symbol: str, interval: str, outputsize: str = "compact") -> dict[str, Any]:
        if not self.api_key:
            raise AlphaVantageError("ALPHAVANTAGE_API_KEY is not set.")

        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": self.api_key,
            "outputsize": outputsize,
        }
        response = requests.get(self.base_url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        if "Error Message" in payload:
            raise AlphaVantageError(payload["Error Message"])
        if "Note" in payload:
            raise AlphaVantageError(payload["Note"])

        return payload
