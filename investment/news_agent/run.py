import os
import pandas as pd
import FinanceDataReader as fdr

def get_news_sentiment(ticker):
    """Simulates news analysis or sentiment."""
    # Placeholder: 실제로는 뉴스 크롤링이나 LLM 연동이 들어갈 자리입니다.
    # 현재는 예시로 티커 숫자의 합을 이용해 더미 데이터를 생성합니다.
    if sum(int(d) for d in str(ticker) if d.isdigit()) % 2 == 0:
        return "Positive"
    else:
        return "Neutral"

def main():
    os.makedirs("data/investment", exist_ok=True)
    df_krx = fdr.StockListing('KOSPI')
    top10 = df_krx.nlargest(10, 'Marcap')
    
    results = []
    for _, row in top10.iterrows():
        ticker = str(row['Code']).zfill(6)
        name = row['Name']
        print(f"News sentiment analysis for {name} ({ticker})...")
        sentiment = get_news_sentiment(ticker)
        results.append({'Code': ticker, 'Name': name, 'News_Sentiment': sentiment})
    
    pd.DataFrame(results).to_csv("data/investment/news_signals.csv", index=False)

if __name__ == "__main__":
    main()
