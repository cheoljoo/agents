# Agent 2: Fundamental Data Collector

This agent is responsible for gathering corporate status and fundamental metrics for KOSPI50 companies.

## Responsibilities

- Fetch KOSPI50 constituent list.
- Collect daily PER, PBR, Dividend Yield, and Market Cap.
- (Optional) Fetch Cash Flow from financial reports.

## Data Output

Outputs daily CSV files for each KOSPI50 ticker in `data/fundamentals/`.

## Execution

```bash
uv run agents/fundamentals/run.py
```
