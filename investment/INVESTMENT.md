# KOSPI Top 10 Investment Committee

This multi-agent committee analyzes the top 10 KOSPI stocks from technical, fundamental, and qualitative perspectives to make investment recommendations.

## Committee Participants

1. **Agent 1: The Quant (`quant_agent`)**
   - **Role**: Technical Analyst
   - **Task**: Analyzes price trends, RSI, Moving Average crossovers, and Volume.
   - **Output**: Bullish/Bearish technical signal.

2. **Agent 2: The Fundamentalist (`fundamental_agent`)**
   - **Role**: Value Analyst
   - **Task**: Analyzes PER, PBR, and Market Cap relative to history or industry.
   - **Output**: Undervalued/Overvalued fundamental signal.

3. **Agent 3: The News Analyst (`news_agent`)**
   - **Role**: Qualitative Analyst
   - **Task**: Fetches recent headlines and sentiment (simulated/placeholder).
   - **Output**: Positive/Negative sentiment signal.

4. **Agent 4: The Manager (`manager_agent`)**
   - **Role**: Committee Chair / Orchestrator
   - **Task**: Synthesizes inputs from Agents 1, 2, and 3 to produce a final "Buy/Hold/Sell" recommendation.
   - **Output**: Final investment report for each stock.

## Automated Execution

```bash
uv run investment/main.py
```
