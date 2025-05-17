import pandas as pd
from utils.logger import setup_logger
import os
from config.settings import (
    DATA_PROCESSED_DIR, STATION_CSV_FILENAME
)

logger = setup_logger(__name__)

def analyze_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby('대여_시간')['USE_CNT']
        .sum()
        .reset_index(name='대여건수')
        .sort_values('대여_시간')
    )

def analyze_by_day(df: pd.DataFrame) -> pd.DataFrame:
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    result = (
        df.groupby('대여_요일')['USE_CNT']
        .sum()
        .reset_index(name='대여건수')
    )
    result['대여_요일'] = pd.Categorical(result['대여_요일'], categories=weekday_order, ordered=True)
    return result.sort_values('대여_요일')

def analyze_age_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    df['AGE_TYPE'] = df['AGE_TYPE'].fillna('기타')
    pivot = pd.pivot_table(
        df,
        index='AGE_TYPE',
        columns='대여_시간',
        values='USE_CNT',
        aggfunc='sum',
        fill_value=0
    )
    pivot = pivot.sort_index()
    return pivot

def analyze_top_station_by_distance(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    df_grouped = (
        df.groupby(['RENT_ID', 'RENT_NM'])[['MOVE_METER', 'USE_CNT']]
        .sum()
        .reset_index()
    )

    df_grouped['평균이동거리'] = df_grouped['MOVE_METER'] / df_grouped['USE_CNT']
    df_sorted = df_grouped.sort_values('평균이동거리', ascending=False).head(top_n)
    return df_sorted[['RENT_ID', 'RENT_NM', '평균이동거리']]

def analyze_gender_age_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    df["GENDER_CD"] = df['GENDER_CD'].replace('', '기타')
    df['AGE_TYPE'] = df['AGE_TYPE'].fillna("기타")

    pivot = pd.pivot_table(
        df,
        index='GENDER_CD',
        columns='AGE_TYPE',
        values='USE_CNT',
        aggfunc='sum',
        fill_value=0
    )
    return pivot

def analyze_daily_energy_and_carbon(df:pd.DataFrame) -> pd.DataFrame:
    df['RENT_DT'] = pd.to_datetime(df['RENT_DT'])
    df['EXER_AMT'] = pd.to_datetime(df['EXER_AMT'], errors='coerce')
    df['CARBON_AMT'] = pd.to_numeric(df['CARBON_AMT'], errors='coerce')

    result = (
        df.groupby('RENT_DT')[['EXER_AMT', 'CARBON_AMT']]
        .sum()
        .reset_index()
        .sort_values('RENT_DT')
    )
    return result

def analyze_station_usage_with_location(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ['RENT_ID', 'RENT_NM']
    value_cols = ['USE_CNT', 'MOVE_METER']

    df_grouped = (
        df[group_cols + value_cols]
        .groupby(group_cols)
        .sum()
        .reset_index()
    )

    df_grouped['평균이동거리'] = df_grouped["MOVE_METER"] / df_grouped['USE_CNT']
    
    loc_df = pd.read_csv(os.path.join(DATA_PROCESSED_DIR, STATION_CSV_FILENAME))

    merged = pd.merge(df_grouped, loc_df, on="RENT_ID", how="inner")
    print(merged.head())
    print(merged.describe())
    
    output_path = os.path.join("outputs", "summary", "merged_locations.csv")
    merged.to_csv(output_path)
    return merged