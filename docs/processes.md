# Processes Required to Make the App Work

This document explains every process the app needs in order to run correctly.

## 1. Configuration Process

The app reads its runtime values from environment variables so secrets are not hard-coded.

Required:
- `ALPHAVANTAGE_API_KEY`

Optional:
- `STOCK_SYMBOL`
- `STOCK_INTERVAL`
- `ALPHAVANTAGE_OUTPUTSIZE`

Implementation:
- `trade_app/config.py`

## 2. Data Fetch Process

The app sends a request to the Alpha Vantage REST API.

Process steps:
- Build the request with symbol, interval, output size, and API key.
- Send the HTTP request.
- Check the response for HTTP errors.
- Check the payload for Alpha Vantage error messages and rate-limit notes.

Implementation:
- `trade_app/client.py`

## 3. Parsing Process

The API response is converted into typed market points.

Process steps:
- Select the series named `Time Series (<interval>)`.
- Read each timestamp entry.
- Extract the `1. open` value.
- Convert timestamps to `datetime` objects.
- Sort points in chronological order.

Implementation:
- `trade_app/timeseries.py`

## 4. Analysis Process

The app performs a basic statistical fit over the price series.

Process steps:
- Convert timestamps to Unix seconds.
- Convert prices to floats.
- Fit a first-degree polynomial using NumPy.
- Produce a trend line function.

Implementation:
- `trade_app/analysis.py`

## 5. Visualization Process

The app displays the price data and the fitted trend line.

Process steps:
- Plot the raw price points.
- Plot the trend line on the same axes.
- Label the axes and legend.
- Render the chart.

Implementation:
- `trade_app/plotting.py`

## 6. Orchestration Process

The workflow module runs the full application in the right order.

Process steps:
- Load config.
- Fetch data.
- Parse the series.
- Compute the trend.
- Print the normalized points.
- Plot the result.

Implementation:
- `trade_app/workflow.py`
- `trade_app/cli.py`

## 7. CLI Process

The command-line interface now exposes three user-facing workflows:

- `run` fetches data and renders the trend plot.
- `predict` fetches data, fits the forecast model, and prints future estimates.
- `backtest` fetches data and measures model quality over rolling windows.

Implementation:
- `trade_app/cli.py`

## 8. Predictive Model Process

The model module fits a simple linear trend across the recent prices and projects the next value.

Implementation:
- `trade_app/model.py`

## 9. Backtesting Process

The backtesting module walks forward through the series, repeatedly trains on a fixed-size window, and scores each prediction.

Implementation:
- `trade_app/backtesting.py`

## 10. Entry Process

The legacy top-level script remains as a thin launcher.

Implementation:
- `alphaVantageAPI.py`

## 11. Dependencies

Install these Python packages before running the app:
- `requests`
- `numpy`
- `matplotlib`

## 12. Failure Handling

The app should stop with a readable error if:
- the API key is missing,
- Alpha Vantage returns an error payload,
- Alpha Vantage rate limits are hit,
- the expected time-series key is missing,
- fewer than two data points are returned.

These safeguards are implemented across the client, parser, and analysis modules.
