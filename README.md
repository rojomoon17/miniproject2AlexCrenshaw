# miniproject2AlexCrenshaw

Mini Project 2 for INF601 - Advanced Programming in Python.

Fetches the closing price of 5 stock tickers for the last 10 trading days,
stores the results in a NumPy array, and plots one color-coded chart per
ticker as a PNG.

## What it does

- Downloads the last 10 trading days of closing prices for 5 tickers
  (`ORCL`, `NVDA`, `INTC`, `MU`, `XOM`) using the [yfinance](https://pypi.org/project/yfinance/)
  API.
- Converts the results into a NumPy array (5 tickers x 10 days).
- Plots each ticker on its own chart: company name and ticker in the
  title, calendar dates on the x-axis, and the line/points/shading
  color-coded green for up days and red for down days.
- Saves each chart as a PNG in `charts/`. This folder is generated when
  the script runs and is **not** committed to the repo (see
  `.gitignore`).

**Data source:** yfinance was reachable and working, so it's used
directly; the Practice Hub `GET /api/v1/datasets/stocks` fallback
mentioned in the assignment was not needed.

## Requirements

- Python 3.11+

## Installation

```bash
git clone https://github.com/rojomoon17/miniproject2AlexCrenshaw.git
cd miniproject2AlexCrenshaw
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux
pip install -r requirements.txt
```

## Running it

```bash
python stock_report.py
```

This prints the data source and the shape of the NumPy array, then
writes one PNG per ticker to `charts/` (created automatically if it
doesn't already exist).

## Troubleshooting

If `yfinance`/`requests` fail with a `CERTIFICATE_VERIFY_FAILED` error,
it could be an antivirus doing HTTPS scanning (Avast caused this issue when I was working on the project)
with a root certificate that isn't in Python's bundled `certifi` trust
store. Add an exception for `python.exe` in your antivirus's HTTPS/SSL
scanning settings, or disable that feature, and try again.

## AI Usage

This project was built with Claude Code. Roughly how it was used:

- Data fetching, the NumPy array conversion, and the initial plotting
  code were drafted by Claude Code based on the assignment requirements,
  then run and checked before moving on.
- The chart styling (company name in the title, calendar date
  formatting, green/red color-coding, the dark gradient background, and
  the shaded/gapped area under the line) was built through an iterative
  loop: I had Claude draft something, run it, then send me
  the result; I'd point out what looked wrong or what I wanted
  changed, and it would adjust and re-run. Several attempts at the
  gap-between-line-and-shading effect were tried and rejected (a
  uniform shadow, a straight vertical offset, a shifted fill region)
  before landing on a clipped, feathered stroke that stayed visually
  even regardless of a segment's slope.
- `requirements.txt` was regenerated with `pip freeze` and this README
  was drafted by Claude Code, then reviewed and edited by me for tone.
- All commits were reviewed before pushing; every design decision
  (colors, date format, chart effects, which tickers to use) was mine -
  Claude Code implemented and iterated on them.
- I also asked Claude what stocks would be interesting to look at and used the 5 it suggested.
- The instructor provided PowerShell commands for downloading the requirements and using pip freeze to record them into the requirements.txt file. Claude suggested using UTF-8, instead of the UTF-16 format that PowerShell defaulted to, for more standardized documentation so it ran a new pip freeze using bash.
