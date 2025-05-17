import pandas as pd

def check_missing_dates(df: pd.DataFrame) -> pd.DataFrame:
    df['RENT_DT'] = pd.to_datetime(df['RENT_DT'])
    all_dates = pd.date_range(start=df['RENT_DT'].min(), end=df['RENT_DT'].max())
    existing = df["RENT_DT"].dt.date.unique()
    missing = sorted(set(all_dates.date) - set(existing))
    return pd.DataFrame({"누락일자": missing})

def check_anomalie(df: pd.DataFrame) -> pd.DataFrame:
    anomolies = df[
        (df['USE_CNT'] <= 0) | 
        (df['MOVE_METER'] <= 0) | 
        (df['MOVE_TIME'] <= 0)
    ]
    return anomolies[['RENT_DT', 'RENT_HR', 'RENT_ID', 'USE_CNT', 'MOVE_METER', 'MOVE_TIME']]

def check_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    dup = df.duplicated(subset=['RENT_DT', 'RENT_HR', 'RENT_ID', 'AGE_TYPE', 'GENDER_CD'], keep=False)
    return df[dup]

def check_missing_columns(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    result = []
    for col in cols:
        total = len(df)
        missing = df[col].isna().sum()
        rate = round((missing / total) * 100, 2)
        result.append({"컬럼": col, "결측값 수": missing, "결측률(%)": rate})
    return pd.DataFrame(result)
