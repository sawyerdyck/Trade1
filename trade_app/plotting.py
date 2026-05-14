from __future__ import annotations

import matplotlib.pyplot as plt


def plot_series(timestamps: list[float], prices: list[float], trend_line) -> None:
    plt.plot(timestamps, prices, marker="o", linestyle="-", color="b", label="Data Points")
    plt.plot(timestamps, trend_line(timestamps), color="r", label="Trend Line")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.show()
