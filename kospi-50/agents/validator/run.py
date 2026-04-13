import os
import pandas as pd

def validate_data():
    daily_path = "data/daily"
    fnd_path = "data/fundamentals"
    
    if not os.path.exists(daily_path) or not os.path.exists(fnd_path):
        print("Data directories missing. Run Agent 1 and Agent 2 first.")
        return

    daily_files = set(os.listdir(daily_path))
    fnd_files = set(os.listdir(fnd_path))
    
    common_files = daily_files.intersection(fnd_files)
    print(f"Validating {len(common_files)} common stock data files...")
    
    report = []
    for file in common_files:
        df_daily = pd.read_csv(os.path.join(daily_path, file))
        df_fnd = pd.read_csv(os.path.join(fnd_path, file))
        
        # FDR 'StockListing'은 'Marcap' (시가총액) 컬럼을 사용함
        # Agent 1에서 저장한 데이터의 컬럼 확인
        if '종가' not in df_daily.columns:
            report.append(f"WARNING: Daily data for {file} missing '종가'")
            
        # Agent 2(Fundamentals)에서 시가총액(Marcap) 확인
        if 'Marcap' not in df_fnd.columns:
            report.append(f"WARNING: Fundamental data for {file} missing 'Marcap'")
        else:
            last_marcap = df_fnd['Marcap'].iloc[-1]
            if last_marcap <= 0:
                report.append(f"ISSUE: Invalid Marcap for {file}: {last_marcap}")

    with open("data/validation_report.txt", "w") as f:
        if not report:
            f.write("All validation checks passed successfully.")
        else:
            f.write("\n".join(report))
    
    print("Validation complete. Report saved to data/validation_report.txt")

if __name__ == "__main__":
    validate_data()
