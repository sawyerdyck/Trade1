# Trade Analysis App

This project fetches intraday price data from Alpha Vantage, converts it into a time series, fits a simple linear trend, and plots the result.

## What Changed

The original single-file script has been split into focused submodules under `trade_app/` so each part of the workflow is isolated and easier to maintain.

## Project Flow

1. Load runtime settings from environment variables.
2. Request intraday data from Alpha Vantage.
3. Parse the API response into timestamped price points.
4. Convert the points into numeric vectors.
5. Fit a linear trend line.
6. Plot the raw series and trend line.

## Setup

Install the dependencies used by the app:

```bash
pip install requests numpy matplotlib
```

Set the required Alpha Vantage key before running:

```powershell
$env:ALPHAVANTAGE_API_KEY="your_api_key"
```

Optional environment variables:

- `STOCK_SYMBOL` defaults to `BTC`
- `STOCK_INTERVAL` defaults to `1min`
- `ALPHAVANTAGE_OUTPUTSIZE` defaults to `compact`

## Run

```bash
python alphaVantageAPI.py
python -m trade_app
```

## CLI Commands

The launcher now supports subcommands:

```bash
python alphaVantageAPI.py run
python alphaVantageAPI.py predict --steps 3
python alphaVantageAPI.py backtest --window-size 20
```

## Prediction Layer

`trade_app/model.py` provides a simple linear trend forecaster for short-horizon predictions.

## Backtesting Layer

`trade_app/backtesting.py` performs a walk-forward test over the historical series and reports:

- mean absolute error
- mean squared error
- directional accuracy

## Module Map

- `trade_app/config.py` loads configuration.
- `trade_app/client.py` handles Alpha Vantage requests and errors.
- `trade_app/timeseries.py` parses and sorts the returned data.
- `trade_app/analysis.py` calculates the trend line.
- `trade_app/plotting.py` renders the chart.
- `trade_app/workflow.py` orchestrates the full pipeline.
- `trade_app/cli.py` exposes the command-line entry point.
- `trade_app/model.py` contains the predictive model.
- `trade_app/backtesting.py` evaluates the model over historical windows.

## Notes

- The app uses the open, intraday price field from Alpha Vantage.
- If Alpha Vantage rate limits are hit, the client raises a clear error message.
- The pipeline currently produces a simple linear trend; it is a foundation for future predictive models.
- The repository now ignores the local virtual environment folders and caches through `.gitignore`.
