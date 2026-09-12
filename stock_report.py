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
    closing prices for each ticker as a list of lists (rows = tickers),
    along with the matching trading dates for each ticker.
    """
    # Ask for extra calendar days so weekends/holidays don't leave us
    # short of `trading_days` actual trading sessions.
    history = yf.download(
        tickers,
        period=f"{trading_days + 10}d",
        progress=False,
    )["Close"]

    closes = []
    dates = []
    for ticker in tickers:
        series = history[ticker].dropna().tail(trading_days)
        closes.append(series.tolist())
        dates.append(list(series.index))

    return closes, dates


def fetch_company_names(tickers):
    """Look up the display name for each ticker (falls back to the
    ticker symbol itself if a name isn't available)."""
    names = {}
    for ticker in tickers:
        info = yf.Ticker(ticker).info
        names[ticker] = info.get("shortName", ticker)
    return names


def format_date(timestamp):
    """Format a date as 'Mon D, YYYY', e.g. 'Sep 11, 2026'."""
    return f"{timestamp.strftime('%b')} {timestamp.day}, {timestamp.strftime('%Y')}"


def plot_ticker(ticker, company_name, dates, prices):
    """Plot one ticker's closing prices, color-coded green/red for
    up/down days, and save it as a PNG in charts/."""
    up_color = "tab:green"
    down_color = "tab:red"
    first_point_color = "tab:gray"

    x = np.arange(len(prices))

    fig, ax = plt.subplots()

    # Color each line segment by whether the price rose or fell versus
    # the previous trading day.
    for i in range(1, len(prices)):
        segment_color = up_color if prices[i] >= prices[i - 1] else down_color
        ax.plot(x[i - 1 : i + 1], prices[i - 1 : i + 1], color=segment_color, linewidth=2, zorder=1)

    point_colors = [first_point_color] + [
        up_color if prices[i] >= prices[i - 1] else down_color for i in range(1, len(prices))
    ]
    ax.scatter(x, prices, color=point_colors, edgecolor="black", linewidth=0.5, zorder=2)

    ax.set_title(f"{company_name} ({ticker}) - Last {len(prices)} Trading Days")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price (USD)")
    ax.set_xticks(x)
    ax.set_xticklabels([format_date(d) for d in dates], rotation=45, ha="right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    fig.savefig(os.path.join(CHARTS_DIR, f"{ticker}.png"))
    plt.close(fig)


def main():
    closes_list, dates_list = fetch_closing_prices(TICKERS, TRADING_DAYS)
    closes = np.array(closes_list)
    company_names = fetch_company_names(TICKERS)

    print(f"Data source: {DATA_SOURCE}")
    print(f"Closing prices array shape: {closes.shape}")

    os.makedirs(CHARTS_DIR, exist_ok=True)
    for ticker, prices, dates in zip(TICKERS, closes, dates_list):
        plot_ticker(ticker, company_names[ticker], dates, prices)
        print(f"Saved chart for {ticker}")


if __name__ == "__main__":
    main()
