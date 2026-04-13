import os
import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime

def get_kospi50_tickers():
    df_krx = fdr.StockListing('KOSPI')
    tickers = df_krx.nlargest(50, 'Marcap')['Code'].tolist()
    return tickers

def main():
    os.makedirs("data/fundamentals", exist_ok=True)
    tickers = get_kospi50_tickers()
    
    # KOSPI 상위 종목의 전체 리스트와 지표를 한 번에 가져옵니다.
    df_krx = fdr.StockListing('KOSPI')
    
    print(f"Collecting KOSPI Top 50 fundamental data using FDR...")
    for ticker in tickers[:10]: # 프로토타입: 상위 10개만
        print(f"Processing fundamental for: {ticker}...")
        # 해당 종목의 한 줄 데이터를 추출
        stock_info = df_krx[df_krx['Code'] == ticker]
        
        # PER, PBR 등 필요한 컬럼만 추출하여 CSV로 저장
        # FDR StockListing 결과에는 'PBR', 'PER' 등이 포함되어 있습니다.
        stock_info.to_csv(f"data/fundamentals/{ticker}.csv")

if __name__ == "__main__":
    main()
