import os
import FinanceDataReader as fdr
import pandas as pd

def get_fundamental_signal(ticker, df_krx):
    """Simple valuation analysis for a ticker."""
    ticker_str = str(ticker).zfill(6)
    stock_rows = df_krx[df_krx['Code'] == ticker_str]
    if stock_rows.empty:
        return "Data Missing"
    
    stock = stock_rows.iloc[0]
    # PER, PBR 등이 수치인지 확인 후 처리 (결측치 처리)
    try:
        per = float(stock.get('PER', 0))
        pbr = float(stock.get('PBR', 0))
    except (ValueError, TypeError):
        return "Invalid Data"
    
    # KOSPI 상위 종목의 경우 더 유연한 기준 적용
    if 0 < per < 15 and 0 < pbr < 1.2:
        return "Undervalued"
    elif per > 30 or pbr > 4:
        return "Overvalued"
    else:
        return "Fairly Valued"

def main():
    os.makedirs("data/investment", exist_ok=True)
    df_krx = fdr.StockListing('KOSPI')
    top10 = df_krx.nlargest(10, 'Marcap')
    
    results = []
    for _, row in top10.iterrows():
        ticker, name = row['Code'], row['Name']
        ticker_str = str(ticker).zfill(6)
        print(f"Fundamental analysis for {name} ({ticker_str})...")
        signal = get_fundamental_signal(ticker_str, df_krx)
        results.append({'Code': ticker_str, 'Name': name, 'Fundamental_Signal': signal})
    
    pd.DataFrame(results).to_csv("data/investment/fundamental_signals.csv", index=False)

if __name__ == "__main__":
    main()
