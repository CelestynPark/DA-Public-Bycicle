import os
import requests
import time
import json
from datetime import datetime, timedelta

API_KEY = os.getenv("SEOUL_API_KEY", "6f59656f4463656c32314451414f4a")
BASE_URL = "http://openapi.seoul.go.kr:8088"
SERVICE_NAME = "tbCycleRentUseTimeInfo"
SERVICE_KEY = "cycleRentUseTimeInfo"
FORMAT = "json"
MAX_ROWS = 1000
RETRY = 3

OUTPUT_DIR = "monthly_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_date_range(start: str, end: str):
    s_date = datetime.strptime(start, "%Y%m%d")
    e_date = datetime.strptime(end, "%Y%m%d")
    return [(s_date + timedelta(days=i)).strftime("%Y%m%d") for i in range((e_date - s_date).days + 1)]

def fetch_hourly_data(date: str, hour: int):
    start_idx = 1
    results = []

    while True:
        end_idx = start_idx + MAX_ROWS - 1
        url = f"{BASE_URL}/{API_KEY}/{FORMAT}/{SERVICE_NAME}/{start_idx}/{end_idx}/{date}/{hour}"

        for attempt in range(RETRY):
            try:
                print(url)
                response = requests.get(url, timeout=5)
                data = response.json()
                rows = data.get(SERVICE_KEY, {}).get("row", [])
                if not rows:
                    return results
                results.extend(rows)
                if len(rows) < MAX_ROWS:
                    return results
                start_idx += MAX_ROWS
                break
            except Exception as e:
                print(f"[{date} {hour}시] 요청 실패 - 재시도 {attempt + 1}: {e}")
                time.sleep(1)
        else:
            print(f"[{date} {hour}시] 재시도 실패. 스킵.")
            return results
        
def save_monthly_data(year: int, month: int):
    month_str = f"{year}{month:02d}"
    dates = get_date_range(f"{month_str}01", f"{month_str}{get_last_day(year, month):02d}")
    all_data = []

    for date in dates:
        for hour in range(24):
            rows = fetch_hourly_data(date, hour)
            all_data.extend(rows)
            time.sleep(0.2)
        
    if all_data:
        output_path = os.path.join(OUTPUT_DIR, f"{month_str}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        print(f"[저장 완료] {output_path} ({len(all_data)}건)")
    else:
        print(f"[데이터 없음] {month_str}")


def get_last_day(year: int, month: int) -> int:
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = next_month - timedelta(days=1)
    return last_day.day

if __name__ == "__main__":
    for y in range(2024, 2026):
        for m in range(1, 13):
            if y == 2024 and m < 1:
                continue
            if y == 2025 and m > 4:
                continue
            save_monthly_data(y, m)