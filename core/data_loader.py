import os
import pandas as pd
from config.settings import DATA_RAW_DIR
from utils.logger import setup_logger

logger = setup_logger(__name__)
def load_monthly_data(filename: str) -> pd.DataFrame:
    path = os.path.join(DATA_RAW_DIR, filename)
    try:
        df = pd.read_csv(path, encoding="utf-8")
        df['source-file'] = filename
        logger.info(f"{filename} 로드 완료. 행 수: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"{filename}  로드 실패: {e}")
        return pd.DataFrame()
    
def load_all_data() -> pd.DataFrame:
    logger.info("모든 월별 데이터 로딩 시작")
    dfs = []

    for file in os.listdir(DATA_RAW_DIR):
        if file.endswith(".csv"):
            df = load_monthly_data(file)
            if not df.empty:
                dfs.append(df)
    
    if not dfs:
        logger.error("유효한 CSV 파일이 존재하지 않습니다.")
        raise ValueError("로딩할 데이터가 없습니다.")

    combined = pd.concat(dfs, ignore_index=True)
    logger.info(f"전체 데이터 병합 완료. 총 행 수: {len(combined)}")
    return combined