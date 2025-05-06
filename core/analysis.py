import pandas as pd
from utils.logger import setup_logger

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
    result['대여_요일'] = pd.Categorial(result['대여_요일'], categories=weekday_order, ordered=True)
    return result.sort_values('대여_요일')

def analyze_age_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    df['AGE_TYPE'] = df['AGE_TYPE'].fillna('기타')
    pivot = pd.pivot_table(
        pf,
        index='AGE_TYPE',
        columns='대여_시간',
        values='USE_CNT',
        aggfunc='sum',
        fill_value=0
    )
    pivot = pivot.sort_index()
    return pivot