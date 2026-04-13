# KOSPI50 Data Analysis Agents

This project follows a multi-agent orchestration architecture where a central Orchestrator coordinates specialized sub-agents.

## Architecture

1.  **Orchestrator Agent (`main.py`)**
    - **Role**: Workflow Manager
    - **Task**: Orchestrates the execution sequence of sub-agents, manages status, and provides final verification feedback.
    - **Execution**: `uv run main.py`

2.  **Daily Stock Agent (`agents/daily_stock`)**
    - **Role**: Data Collector (Price & Volume)
    - **Task**: Collects daily OHLCV, 10-month MA, Market Cap, and Dividends.
    - **Data Output**: `data/daily/`

3.  **Fundamental Agent (`agents/fundamentals`)**
    - **Role**: Data Collector (Company Status)
    - **Task**: Collects fundamental metrics like PER, PBR, and Market Cap.
    - **Data Output**: `data/fundamentals/`

4.  **Validation Agent (`agents/validator`)**
    - **Role**: Quality Assurance
    - **Task**: Cross-checks data consistency between Agent 1 and Agent 2, logs issues.
    - **Report Output**: `data/validation_report.txt`

## Execution Workflow (Autonomous Mode)

Simply run the master command to trigger the entire automated pipeline:
```bash
uv run main.py
```
This single command initiates the Manager, which then calls each sub-agent and reports the final status.
