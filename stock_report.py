"""
Name:    Alex Crenshaw
Class:   INF601 - Advanced Programming in Python
Project: Mini Project 2 - Stock Closing Price Report

Fetches the closing price of 5 stock tickers for the last 10 trading days
using yfinance, stores the results in a NumPy array, plots one chart per
ticker, and saves each chart as a PNG in charts/.
"""
# Claude decided to use triple-quoted string literals instead of comments for the header
# after learning why I've decided to keep this format
# doing this for the first statement in a module, class, function, or method makes it the object's docstring
# docstrings can be retrieved later at runtime while comments can't so it's good for documentation
# I think it should count for the assignment's requirements

import os

import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Polygon
from matplotlib.ticker import StrMethodFormatter

CHART_DPI = 150

# Dark grey (top) fading to black (bottom), used as the chart background.
BACKGROUND_CMAP = LinearSegmentedColormap.from_list("bg_gradient", ["#262626", "#000000"])

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
    """Plot one ticker's closing prices on a dark grey-to-black gradient
    background, with the line, points, and area shading color-coded
    green/red for up/down days, and save it as a PNG in charts/."""
    up_color = "tab:green"
    down_color = "tab:red"
    text_color = "whitesmoke"

    x = np.arange(len(prices))

    fig, ax = plt.subplots()
    fig.patch.set_facecolor("black")

    # Lock the view limits before drawing so the gradient background and
    # the shaded areas line up with what's actually visible.
    price_range = max(prices) - min(prices)
    padding = price_range * 0.15 if price_range else max(prices) * 0.05
    y_bottom, y_top = min(prices) - padding, max(prices) + padding
    x_left, x_right = -0.5, len(prices) - 0.5
    ax.set_xlim(x_left, x_right)
    ax.set_ylim(y_bottom, y_top)
    ax.autoscale(False)

    # Dark grey-to-black gradient background.
    gradient = np.linspace(0, 1, 256).reshape(-1, 1)
    ax.imshow(
        gradient,
        extent=[x_left, x_right, y_bottom, y_top],
        aspect="auto",
        cmap=BACKGROUND_CMAP,
        origin="upper",
        zorder=0,
    )

    # One color per segment, based on whether the price rose or fell
    # versus the previous trading day.
    segment_colors = [up_color if prices[i] >= prices[i - 1] else down_color for i in range(1, len(prices))]

    # Shade the area under each segment, flush against the line itself,
    # then paint a background-colored stroke along that same path before
    # drawing the real line on top. A stroke's width in matplotlib is
    # always measured perpendicular to its path, so this "erases" a band
    # of constant on-screen width around the line regardless of slope -
    # unlike shifting the fill's geometry, which visibly thins out on
    # steep segments.
    LINE_WIDTH = 2
    GAP_WIDTH = 3
    # Layered, increasingly narrow/opaque strokes fade from transparent
    # at the outer edge to solid near the line, instead of one stroke
    # with a single hard edge where it meets the colored fill.
    FEATHER_LAYERS = [(1.0, 0.2), (0.7, 0.35), (0.45, 0.6), (0.2, 1.0)]
    for i, segment_color in enumerate(segment_colors, start=1):
        xi, yi = x[i - 1 : i + 1], prices[i - 1 : i + 1]
        ax.fill_between(xi, yi, y_bottom, color=segment_color, alpha=0.25, zorder=1)

        # The spacer stroke below is centered on the line, so half its
        # width would otherwise bleed above the line into the plain
        # background. Clip it to the filled region (the same shape as
        # the fill_between above) so it only erases inside the shading.
        clip_region = Polygon(
            [(xi[0], yi[0]), (xi[1], yi[1]), (xi[1], y_bottom), (xi[0], y_bottom)],
            transform=ax.transData,
        )
        for width_frac, alpha in FEATHER_LAYERS:
            (spacer,) = ax.plot(
                xi,
                yi,
                color="black",
                alpha=alpha,
                linewidth=LINE_WIDTH + 2 * GAP_WIDTH * width_frac,
                solid_capstyle="round",
                zorder=1.5,
            )
            spacer.set_clip_path(clip_region)

        ax.plot(xi, yi, color=segment_color, linewidth=LINE_WIDTH, solid_capstyle="round", zorder=2)

    # Color each point to match the segment leaving it, so every point
    # reads as part of an up or down move. The last point has no segment
    # leaving it, so it's colored like the segment arriving at it instead.
    point_colors = segment_colors + [segment_colors[-1]]
    ax.scatter(x, prices, color=point_colors, zorder=3)

    ax.set_title(f"{company_name} ({ticker}) - Last {len(prices)} Trading Days", color=text_color)
    ax.set_xlabel("Date", color=text_color)
    ax.set_ylabel("Closing Price (USD)", color=text_color)
    ax.set_xticks(x)
    ax.set_xticklabels([format_date(d) for d in dates], rotation=45, ha="right")
    ax.yaxis.set_major_formatter(StrMethodFormatter("${x:,.2f}"))
    ax.tick_params(colors=text_color)
    for spine in ax.spines.values():
        spine.set_color(text_color)
    ax.grid(axis="y", color=text_color, alpha=0.2)
    fig.tight_layout()

    fig.savefig(os.path.join(CHARTS_DIR, f"{ticker}.png"), dpi=CHART_DPI, facecolor=fig.get_facecolor())
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
