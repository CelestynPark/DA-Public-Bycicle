import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from multiprocessing import Pool, cpu_count

load_dotenv()
API_KEY = os.getenv("SEOUL_API_KEY2")
BASE_URL = "http://openapi.seoul.go.kr:8088"
SERVICE_NAME = "tbCycleStationInfo"
FORMAT = "json"
CHUNK_SIZE = 1000
OUTPUT_PATH = "data/processed"
RAW_JSON_DIR = "data/raw/station_json_chunks"

os.makedirs(OUTPUT_PATH, exist_ok=True)
os.makedirs(RAW_JSON_DIR, exist_ok=True)

def get_total_count():
    url = f"{BASE_URL}/{API_KEY}/{FORMAT}/{SERVICE_NAME}/1/1/"
    print(url)
    res = requests.get(url)
    return res.json()["stationInfo"]["list_total_count"]

def fetch_chunk(args):
    start, end = args
    url = f"{BASE_URL}/{API_KEY}/{FORMAT}/{SERVICE_NAME}/{start}/{end}/"
    try:
        res = requests.get(url, timeout=5)
        json_data = res.json()

        json_filename = f"chunk_{start}_{end}.json"
        json_path = os.path.join(RAW_JSON_DIR, json_filename)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        rows = json_data.get("stationInfo", {}).get("row", [])
        print(f"[OK] {start}~{end}: {len(rows)}건")
        return rows
    except Exception as e:
        print(f"[FAIL] {start}~{end}: {e}")
        return []
    
def fetch_station_loactions_parallel():
    total = int(get_total_count())
    
    print(f"총 대여소 개수: {total}")

    ranges = [(start, min(start + CHUNK_SIZE - 1, total)) for start in range(1, total + 1, CHUNK_SIZE)]

    with Pool(processes=min(len(ranges), cpu_count())) as pool:
        results = pool.map(fetch_chunk, ranges)
    
    all_rows = [row for chunk in results for row in chunk]
    df = pd.DataFrame(all_rows)
    
    df = df[["RENT_NO", "RENT_ID_NM", "STA_LAT", "STA_LONG"]]
    df.columns = ["RENT_ID", "RENT_NM", "LAT", "LONG"]
    df.to_csv(f"{OUTPUT_PATH}/station_locations.csv", index=False, encoding='utf-8')
    print(f"[저장 완료] {OUTPUT_PATH}/station_locations.csv ({len(df)}건)")


if __name__ == "__main__":
    fetch_station_loactions_parallel()