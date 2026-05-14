from __future__ import annotations

import argparse

from .backtesting import run_walk_forward_backtest
from .config import load_config
from .model import LinearTrendModel
from .timeseries import points_to_vectors
from .workflow import load_market_points, run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trade analysis command line interface")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("run", help="Fetch data, fit a trend, and plot it")

    predict_parser = subparsers.add_parser("predict", help="Predict future prices from recent data")
    predict_parser.add_argument("--steps", type=int, default=1, help="Number of steps ahead to forecast")

    backtest_parser = subparsers.add_parser("backtest", help="Run a walk-forward backtest")
    backtest_parser.add_argument("--window-size", type=int, default=20, help="Training window size")

    parser.set_defaults(command="run")
    return parser


def _handle_predict(steps: int) -> None:
    config = load_config()
    points = load_market_points(config)
    _, prices = points_to_vectors(points)
    model = LinearTrendModel().fit(prices)
    predictions = model.predict_many(prices, steps=steps)
    print({"symbol": config.symbol, "steps": steps, "predictions": predictions})


def _handle_backtest(window_size: int) -> None:
    config = load_config()
    points = load_market_points(config)
    _, prices = points_to_vectors(points)
    result = run_walk_forward_backtest(prices, window_size=window_size)
    print(result)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "predict":
        _handle_predict(args.steps)
        return
    if args.command == "backtest":
        _handle_backtest(args.window_size)
        return

    config = load_config()
    run_pipeline(config)


if __name__ == "__main__":
    main()
