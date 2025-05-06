import pandas as pd
from utils.logger import setup_logger

logger = setup_logger(__name__)

def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("전처리 시작")

    df = df.copy()

    try:
        df['RENT_HR'] = df['RENT_HR'].astype(str).str.zfill(2)
        df['RENT_DATETIME'] = pd.to_datetime(df['RENT_DT'] + ' ' + df['RENT_HR'] + ':00:00', format='%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logger.error(f"datetime 결합 오류: {e}")
        raise

    numeric_cols = ['MOVE_METER', 'MOVE_TIME', 'USE_CNT']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    before_rows = len(df)

    df = df.dropna(subset=numeric_cols)
    df = df[(df['MOVE_METER'] > 0) & (df['MOVE_TIME'] > 0) & (df["USE_CNT"] > 0)]

    after_rows = len(df)
    logger.info(f"이상치 제거: {before_rows - after_rows}건 제거 (남은 데이터 {after_rows:,}건)")

    df['대여_요일'] = df['RENT_DATETIME'].dt.day_name()
    df['대여_시간'] = df['RENT_DATETIME'].dt.hour

    logger.info("전처리 완료 및 파생 컬럼 생성")

    return df