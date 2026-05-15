from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests
import yfinance as yf


class AlphaVantageError(RuntimeError):
    """Raised when Alpha Vantage returns an error or unexpected payload."""


class YahooFinanceError(RuntimeError):
    """Raised when Yahoo Finance returns an error or unexpected payload."""


class StooqError(RuntimeError):
    """Raised when Stooq returns an error or unexpected payload."""


class YFinanceError(RuntimeError):
    """Raised when yfinance returns an error or unexpected payload."""


@dataclass(frozen=True)
class AlphaVantageClient:
    api_key: str
    base_url: str = "https://www.alphavantage.co/query"

    def _request(self, params: dict[str, Any]) -> dict[str, Any]:
        response = requests.get(self.base_url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

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
        payload = self._request(params)

        info_message = payload.get("Information")
        if isinstance(info_message, str) and "premium endpoint" in info_message.lower():
            # Automatic fallback to free endpoint.
            daily_params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": self.api_key,
                "outputsize": outputsize,
            }
            payload = self._request(daily_params)

        if "Error Message" in payload:
            raise AlphaVantageError(payload["Error Message"])
        if "Note" in payload:
            raise AlphaVantageError(payload["Note"])
        if "Information" in payload:
            raise AlphaVantageError(payload["Information"])

        if not any("Time Series" in key for key in payload.keys()):
            available_keys = ", ".join(payload.keys()) or "<none>"
            raise AlphaVantageError(
                "Alpha Vantage response did not include time-series data. "
                f"Available keys: {available_keys}"
            )

        return payload


@dataclass(frozen=True)
class YahooFinanceClient:
    base_url: str = "https://query1.finance.yahoo.com/v8/finance/chart"

    def fetch_chart(self, symbol: str, interval: str = "1d", range_value: str = "6mo") -> dict[str, Any]:
        params = {
            "interval": interval,
            "range": range_value,
            "includePrePost": "false",
            "events": "div,splits",
        }
        response = requests.get(f"{self.base_url}/{symbol}", params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        chart = payload.get("chart", {})
        error = chart.get("error")
        if error:
            description = error.get("description", "Unknown Yahoo Finance error")
            raise YahooFinanceError(description)

        result = chart.get("result")
        if not isinstance(result, list) or not result:
            raise YahooFinanceError("Yahoo Finance response did not include chart result data.")

        return payload


@dataclass(frozen=True)
class StooqClient:
    base_url: str = "https://stooq.com/q/d/l/"

    def fetch_daily_csv(self, symbol: str) -> str:
        normalized_symbol = symbol.strip().lower()
        if "." not in normalized_symbol:
            normalized_symbol = f"{normalized_symbol}.us"

        params = {
            "s": normalized_symbol,
            "i": "d",
        }
        response = requests.get(self.base_url, params=params, timeout=30)
        response.raise_for_status()
        csv_text = response.text.strip()

        if not csv_text or csv_text.lower().startswith("no data"):
            raise StooqError(f"Stooq returned no data for symbol: {symbol}")

        return csv_text


@dataclass(frozen=True)
class YFinanceClient:
    def fetch_history(self, symbol: str, interval: str = "1d", period: str = "6mo"):
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period, interval=interval, auto_adjust=False, actions=False)

        if history is None or history.empty:
            raise YFinanceError(f"yfinance returned no data for symbol: {symbol}")

        return history
