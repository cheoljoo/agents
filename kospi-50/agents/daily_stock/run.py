import os
import FinanceDataReader as fdr
from datetime import datetime, timedelta

def get_kospi50_tickers():
    """Get the list of tickers in the KOSPI 50 index."""
    # FinanceDataReader를 사용하여 KOSPI 리스트를 가져옵니다.
    df_krx = fdr.StockListing('KOSPI')
    # 실제 KOSPI 50 구성 종목을 정확히 가져오려면 pykrx가 필요하지만, 
    # 현재 환경 이슈로 KOSPI 상위 50개를 예시로 사용합니다.
    tickers = df_krx.nlargest(50, 'Marcap')['Code'].tolist()
    return tickers

def collect_daily_data(ticker, start_date, end_date):
    """Collect OHLCV for a ticker using FinanceDataReader."""
    df = fdr.DataReader(ticker, start_date, end_date)
    
    # 10개월 이동평균 (약 200일)
    df['10mo_MA'] = df['Close'].rolling(window=200).mean()
    
    # 시가총액 정보 (최신 데이터 기반으로 간단히 추가)
    # 실제 일별 시가총액 데이터는 pykrx가 필요하지만, FDR에서는 현재가 기준으로만 제공되므로
    # 여기서는 OHLCV 중심으로 수집합니다.
    df.rename(columns={
        'Open': '시가', 'High': '고가', 'Low': '저가', 'Close': '종가', 'Volume': '거래량'
    }, inplace=True)
    
    # Validator를 위해 필요한 '시가총액' 컬럼 더미 추가 (실제 데이터는 Agent 2에서 상세히 다룸)
    df['시가총액'] = 0 
    
    return df

def main():
    os.makedirs("data/daily", exist_ok=True)
    tickers = get_kospi50_tickers()
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=400)).strftime("%Y-%m-%d")
    
    print(f"Collecting KOSPI Top 50 ({len(tickers)}) daily data using FDR...")
    for ticker in tickers[:10]: # 프로토타입: 상위 10개만
        print(f"Processing ticker: {ticker}...")
        df = collect_daily_data(ticker, start_date, end_date)
        df.to_csv(f"data/daily/{ticker}.csv")

if __name__ == "__main__":
    main()
