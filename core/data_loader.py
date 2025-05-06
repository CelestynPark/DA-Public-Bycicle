import os
import json
import pandas as pd
from typing import List
from config.settings import DATA_RAW_DIR
from utils.logger import setup_logger

logger = setup_logger(__name__)

def load_all_json_files() -> pd.DataFrame:
    json_file: list[str] = [
        f for f in os.listdir(DATA_RAW_DIR)
        if f.endswith(".json") and f[:6].isdigit
    ]

    if not json_file:
        logger.error("JSON 파일이 존재하지 않습니다.")
        raise FileNotFoundError("data/raw 경로에 분석 대상 JSON 파일이 없습니다.")
    
    all_data = []
    for file in sorted(json_file):
        file_path = os.path.join(DATA_RAW_DIR, file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
                df = pd.DataFrame(raw)
                df["source_file"] = file
                all_data.append(df)
            logger.info(f"파일 로드 성공: {file}")
        except Exception as e:
            logger.warning(f"파일 로드 실패: {file} | 에러: {e}")
    
    combined_df = pd.concat(all_data, ignore_index=True)
    logger.info(f"총 {len(combined_df):,}개의 데이터 로드 완료 (파일 수: {len(json_file)})")
    return combined_df