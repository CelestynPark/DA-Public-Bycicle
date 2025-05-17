import os
import argparse
import pandas as pd

from config.settings import (
    DATA_PROCESSED_DIR, PROCESSED_CSV_FILENAME, SUMMARY_DIR, FIGURE_DIR
)
from core.data_loader import load_all_json_files
from core.preprocessing import clean_and_engineer
from core.analysis import (
    analyze_by_hour, analyze_by_day, analyze_age_by_hour,
    analyze_top_station_by_distance,
    analyze_gender_age_heatmap,
    analyze_daily_energy_and_carbon,
    analyze_station_usage_with_location,
)
from core.visualization import (
    plot_bar, plot_line, plot_scatter, plot_age_hour_heatmap,
    plot_top_station_distance,
    plot_gender_age_heatmap,
    plot_energy_carbon_trend,
    plot_station_map,
)
from core.quality import (
    check_missing_dates,
    check_anomalie,
    check_duplicates,
    check_missing_columns,
)
from utils.logger import setup_logger

logger = setup_logger(__name__)

def run_preprocess():
    logger.info("PREPROCESS START")
    df = load_all_json_files()
    df_clean = clean_and_engineer(df)

    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
    out_path = os.path.join(DATA_PROCESSED_DIR, PROCESSED_CSV_FILENAME)
    df_clean.to_csv(out_path, index=False)
    logger.info(f"전처리 완료 → 저장 경로: {out_path}")

def run_analysis():
    logger.info("ANALYSIS START")
    csv_path = os.path.join(DATA_PROCESSED_DIR, PROCESSED_CSV_FILENAME)
    if not os.path.exists(csv_path):
        logger.error("전처리된 파일이 없습니다. 먼저 preprocess 모드를 실행하세요.")
        return
    
    df = pd.read_csv(csv_path)

    df_hour = analyze_by_hour(df)
    df_day = analyze_by_day(df)

    os.makedirs(SUMMARY_DIR, exist_ok=True)
    df_hour.to_csv(os.path.join(SUMMARY_DIR, 'by_hour.csv'), index=False)
    df_day.to_csv(os.path.join(SUMMARY_DIR, 'by_day.csv'), index=False)

    logger.info("분석 결과 저장 완료")

def run_visualization():
    logger.info("VISUALIZATION START")

    os.makedirs(FIGURE_DIR, exist_ok=True)

    dayhour_list = [
        {"csv": "by_day.csv", "img": "day_bar.png", "x": "대여_요일", "y": "대여건수", "title": "요일별 대여량", "func": plot_bar},
        {"csv": "by_hour.csv", "img": "hour_line.png", "x": "대여_시간", "y": "대여건수", "title": "시간대별 대여량", "func": plot_line},
    ]
    for dayhour in dayhour_list:
        if not os.path.exists(os.path.join(FIGURE_DIR, dayhour["img"])):
            df = pd.read_csv(os.path.join(SUMMARY_DIR, dayhour["csv"]))
            dayhour["func"](df, dayhour["x"], dayhour["y"], dayhour["title"], dayhour["img"])

    extra_analyze_list = [
        {"img": "age_hour_heatmap.png", "title": "연령대-시간대별 대여량 히트맵", "analyze_func": analyze_age_by_hour, "plot_func": plot_age_hour_heatmap},
        {"img": "top_station_distance.png", "title": "대여소별 평균 이동거리 Top 10", "analyze_func": analyze_top_station_by_distance, "plot_func": plot_top_station_distance},
        {"img": "gender_age_heatmap.png", "title": "성별-연령대별 대여량 히트맵", "analyze_func": analyze_gender_age_heatmap, "plot_func": plot_gender_age_heatmap},
        {"img": "energy_carbon_trend.png", "title": "일별 소모 칼로리 및 CO₂ 절감량", "analyze_func": analyze_daily_energy_and_carbon, "plot_func": plot_energy_carbon_trend},
        {"file": "station_map.html", "analyze_func": analyze_station_usage_with_location, "plot_func": plot_station_map},
    ]
    exist_list = [os.path.exists(os.path.join(FIGURE_DIR, target["img"] if "img" in target else target["file"])) for target in extra_analyze_list]
    if False in exist_list:
        csv_path = os.path.join(DATA_PROCESSED_DIR, PROCESSED_CSV_FILENAME)
        df = pd.read_csv(csv_path)

        for i in range(len(extra_analyze_list)):
            if not exist_list[i]:
                target = extra_analyze_list[i]
                df_output = target["analyze_func"](df)
                if "img" in target:
                    target["plot_func"](df_output, target["title"], target["img"])
                else:
                    target["plot_func"](df_output, target["file"])
        
    logger.info("시각화 이미지 저장 완료")

def run_quality_check():
    logger.info("데이터 품질 점검 시작")
    csv_path = os.path.join(DATA_PROCESSED_DIR, PROCESSED_CSV_FILENAME)

    if not os.path.exists(csv_path):
        logger.error("전처리된 파일이 없습니다. 먼저 preprocess를 실행해주세요.")
        return

    df = pd.read_csv(csv_path)

    logger.info("누락된 날짜 점검:")
    missing_dates = check_missing_dates(df)
    print(missing_dates.head())

    logger.info("이상치 점검:")
    anomalie = check_anomalie(df)
    print(anomalie.head())
    
    logger.info("중복 행 점검:")
    duplicates = check_duplicates(df)
    print(duplicates.head())

    logger.info("주요 컬럼 결측률 점검:")
    missing_columns = check_missing_columns(df)
    print(missing_columns.head())

    logger.info("데이터 품질 점검 완료")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='서울시 공공자전거 분석 CLI')
    parser.add_argument('--mode', required=True, choices=['preprocessing', 'analyze', 'visualize'])
    args = parser.parse_args()

    if args.mode == 'preprocess':
        run_preprocess()
    elif args.mode == 'analyze':
        run_analysis()
    elif args.mode == 'visualize':
        run_visualization()
    elif args.mode == 'quality':
        run_quality_check()