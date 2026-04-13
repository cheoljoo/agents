import os
import FinanceDataReader as fdr
import pandas as pd
from datetime import datetime, timedelta

def get_quant_signal(ticker):
    """Simple technical analysis for a ticker."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=100)).strftime("%Y-%m-%d")
    
    df = fdr.DataReader(ticker, start_date, end_date)
    # 데이터가 부족한 경우 (신규 상장 등)
    if len(df) < 60: 
        return "Not Enough Data"
    
    # Simple logic: Moving Average Crossover (20d vs 60d)
    ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
    ma60 = df['Close'].rolling(window=60).mean().iloc[-1]
    last_close = df['Close'].iloc[-1]
    
    if ma20 > ma60 and last_close > ma20:
        return "Bullish"
    elif ma20 < ma60 or last_close < ma20:
        return "Bearish"
    else:
        return "Neutral"

def main():
    os.makedirs("data/investment", exist_ok=True)
    df_krx = fdr.StockListing('KOSPI')
    top10 = df_krx.nlargest(10, 'Marcap')
    
    results = []
    for _, row in top10.iterrows():
        ticker, name = row['Code'], row['Name']
        # ticker를 6자리 문자열로 고정
        ticker = str(ticker).zfill(6)
        print(f"Quant analyzing {name} ({ticker})...")
        signal = get_quant_signal(ticker)
        results.append({'Code': ticker, 'Name': name, 'Quant_Signal': signal})
    
    pd.DataFrame(results).to_csv("data/investment/quant_signals.csv", index=False)

if __name__ == "__main__":
    main()
