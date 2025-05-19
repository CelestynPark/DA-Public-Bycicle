import pandas as pd
import os
from config.settings import SUMMARY_DIR

def summarize_csv(path: str, key: str) -> str:
    try:
        df = pd.read_csv(path)
        top = df.sort_values(df.columns[-1], ascending=False).head(5)
        summary =f"{key} 기준 상위 5개:\n"
        for _, row in top.iterrows():
            summary += ", ".join([f"{col}: {row[col]}" for col in df.columns]) + "\n"
        return summary
    except Exception:
        return f"{key} 분석 결과 불러오기 실패"
    
def load_context() -> str:
    summary_parts = []
    files = {
        "시간대별": "by_hour.csv",
        "요일별": "by_day.csv"
    }
    for key, fname in files.items():
        path = os.path.join(SUMMARY_DIR, fname)
        print(path)
        summary_parts.append(summarize_csv(path, key))
    return "\n".join(summary_parts)