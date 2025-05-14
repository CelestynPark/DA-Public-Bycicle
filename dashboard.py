import streamlit as st
import os
from PIL import Image
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

FIGURE_DIR = "outputs/figures"
SUMMARY_DIR = "outputs/summary"
PROCESSED_PATH = "data/processed/bike_cleaned.csv"

st.set_page_config(page_title="서울시 공공자전거 분석 대시보드", layout="wide")

st.title("서울시 공공자전거 분석 대시보드")
st.markdown("""
이 대시보드는 서울시 공공자전거(따릉이)의 이용 데이터를 기반으로
시간대, 요일, 연령대, 대여소, 운동량 등의 분석 결과를 시각적으로 제공한다.
""")

st.sidebar.header("시각화 옵션")
mode = st.sidebar.radio("시각화 방식 선택", ["이미지 보기", "실시간 그래프 그리기"])

if mode == "이미지 보기":
    IMAGE_MAP = {
        "요일별 대여량": "day_bar.png",
        "시간대별 대여량": "hour_line.png",
        "연령대-시간대 히트맵": "age_hour_heatmap.png",
        "성별-연령대 히트맵": "gender_age_heatmap.png",
        "대여소별 평균 이동거리": "top_station_distance.png",
        "운동량/탄소량 트렌드": "energy_carbon_trend.png",
    }

    option = st.selectbox("보고 싶은 분석 결과를 선택하세요", list(IMAGE_MAP.keys()))
    image_path = os.path.join(FIGURE_DIR, IMAGE_MAP[option])

    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption=option, use_column_width=True)
    else:
        st.error(f"이미지 파일을 찾을 수 없습니다: {image_path}")

elif mode == "실시간 그래프 그리기":
    GRAPH_OPTIONS = [
        "시간대별 대여량",
        "요일별 대여량",
        "연령대별 대여량",
        "성별 대여량",
        "운동량/탄소량 추이"
    ]
    choice = st.selectbox("실시간 분석 그래프 선택", GRAPH_OPTIONS)

    try:
        df = pd.read_csv(PROCESSED_PATH)
    except FileNotFoundError:
        st.error("전처리된 CSV 파일이 존재하지 않습니다. 먼저 분석을 실행해주세요.")
    else:
        fig, ax = plt.subplots(figsize=(10, 6))

        if choice == "시간대별 대여량":
            hourly = df.groupby("대여_시간")["USE_CNT"].sum().reset_index()
            sns.lineplot(data=hourly, x="대여_시간", y="USE_CNT", ax=ax)
            ax.set_title("시간대별 대여량")
            ax.set_ylabel("대여 건수")
        
        elif choice == "요일별 대여량":
            weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            day = df.groupby("대여_요일")['USE_CNT'].sum().reindex(weekday_order).reset_index()
            sns.barplot(data=day, x='대여_요일', y='USE_CNT', ax=ax)
            ax.set_title('요일별 대여량')
            ax.set_ylabel("대여 건수")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        
        elif choice == "연령별 대여량":
            age = df.groupby("AGE_TYPE")['USE_CNT'].sum().reset_index()
            sns.barplot(data=age, x='AGE_TYPE', y='USE_CNT', ax=ax)
            ax.set_title('연령별 대여량')
            ax.set_ylabel("대여 건수")
        
        elif choice == "성별 대여량":
            gender = df["GENDER_CD"].replace('', "기타").value_counts().reset_index()
            gender.columns = ['성별', '건수']
            sns.barplot(data=gender, x='성별', y='건수', ax=ax)
            ax.set_title('성별 대여량')
            ax.set_ylabel("대여 건수")
        
        elif choice == "운동량/탄수량 추이":
            df['RENT_DT'] = pd.to_datetime(df['RENT_DT'])
            df['EXER_AMT'] = pd.to_numeric(df['EXER_AMT'], errors='ceorce')
            df['CARBON_AMT'] = pd.to_numeric(df['CARBON_AMT'], errors='coerce')
            daily = df.groupby('RENT_DT')[['EXER_AMT', 'CARBON_AMT']].sum().reset_index()
            ax.plot(daily['RENT_DT'], daily['EXER_AMT'], label='칼로리(kcal)', color='tomato')
            ax.plot(daily['RENT_DT'], daily['CARBON_AMT'], label='탄소절감량(kg)', color='seagreen')
            ax.legend()
            ax.set_title('운동량/탄소량 일별 추이')
            
        st.pyplot(fig)