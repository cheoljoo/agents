import os
import pandas as pd

def synthesize_recommendation(quant, fundamental, news):
    """Simple decision logic for final recommendation."""
    score = 0
    if quant == "Bullish":
        score += 1
    elif quant == "Bearish":
        score -= 1
    
    if fundamental == "Undervalued":
        score += 1
    elif fundamental == "Overvalued":
        score -= 1
    
    if news == "Positive":
        score += 1
    
    if score >= 2:
        return "Strong Buy"
    elif score == 1:
        return "Buy"
    elif score == 0:
        return "Hold"
    else:
        return "Sell"

def main():
    quant_path = "data/investment/quant_signals.csv"
    fnd_path = "data/investment/fundamental_signals.csv"
    news_path = "data/investment/news_signals.csv"
    
    if not all(os.path.exists(p) for p in [quant_path, fnd_path, news_path]):
        print("Required signals missing. Run agents 1, 2, 3 first.")
        return
    
    # 'Code' 컬럼을 문자열(str)로 읽도록 지정 (앞자리 0 유지)
    q_df = pd.read_csv(quant_path, dtype={'Code': str})
    f_df = pd.read_csv(fnd_path, dtype={'Code': str})
    n_df = pd.read_csv(news_path, dtype={'Code': str})
    
    # Merge all
    df = q_df.merge(f_df, on=['Code', 'Name']).merge(n_df, on=['Code', 'Name'])
    
    # Final Decision
    df['Recommendation'] = df.apply(lambda r: synthesize_recommendation(
        r['Quant_Signal'], r['Fundamental_Signal'], r['News_Sentiment']
    ), axis=1)
    
    # Save Report
    df.to_csv("data/investment/final_committee_report.csv", index=False)
    
    print("\n--- KOSPI Top 10 Investment Committee Final Report ---")
    # 코드 포맷팅 (6자리 유지)
    df['Code'] = df['Code'].str.zfill(6)
    print(df[['Name', 'Code', 'Recommendation']])

if __name__ == "__main__":
    main()
