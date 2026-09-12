"""
Name:    Alex Crenshaw
Class:   INF601 - Advanced Programming in Python
Project: Mini Project 2 - Stock Closing Price Report

Fetches the closing price of 5 stock tickers for the last 10 trading days
using yfinance, stores the results in a NumPy array, plots one chart per
ticker, and saves each chart as a PNG in charts/.
"""

import os

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Data source used for this project. yfinance was reachable and working,
# so the Practice Hub fallback endpoint was not needed.
DATA_SOURCE = "yfinance"

TICKERS = ["ORCL", "NVDA", "INTC", "MU", "XOM"]
TRADING_DAYS = 10
CHARTS_DIR = "charts"


def fetch_closing_prices(tickers, trading_days):
    """Download recent daily data and return the last `trading_days`
    closing prices for each ticker as a list of lists (rows = tickers).
    """
    # Ask for extra calendar days so weekends/holidays don't leave us
    # short of `trading_days` actual trading sessions.
    history = yf.download(
        tickers,
        period=f"{trading_days + 10}d",
        progress=False,
    )["Close"]

    closes = []
    for ticker in tickers:
        series = history[ticker].dropna().tail(trading_days)
        closes.append(series.tolist())

    return closes


def main():
    closes_list = fetch_closing_prices(TICKERS, TRADING_DAYS)
    closes = np.array(closes_list)

    print(f"Data source: {DATA_SOURCE}")
    print(f"Closing prices array shape: {closes.shape}")
    print(closes)


if __name__ == "__main__":
    main()
