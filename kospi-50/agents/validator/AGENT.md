# Agent 3: Validation Agent

This agent ensures the data collected by Agent 1 and Agent 2 is complete and consistent.

## Responsibilities

- Verify all 50 tickers' data files exist.
- Cross-check common metrics like Market Cap and Dividends between Agent 1 and Agent 2 outputs.
- Identify missing values or unrealistic outliers.
- Log validation results to `data/validation_report.txt`.

## Execution

```bash
uv run agents/validator/run.py
```
