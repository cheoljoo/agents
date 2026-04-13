# Agent 1: Daily Stock Data Collector

This agent is responsible for gathering daily price fluctuations and key valuation metrics for KOSPI50 companies.

## Responsibilities

- Fetch KOSPI50 constituent list.
- Collect daily OHLCV (Open, High, Low, Close, Volume) data.
- Collect daily Market Cap and Dividend information.
- Calculate 10-month Moving Average for each stock.

## Data Output

Outputs daily CSV files for each KOSPI50 ticker in `data/daily/`.

## Execution

```bash
uv run agents/daily_stock/run.py
```
