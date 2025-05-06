import os
import argparse
import pandas as pd

from config.settings import (
    DATA_PROCESSED_DIR, PROCESSED_CSV_FILENAME, SUMMARY_DIR, FIGURE_DIR
)
from core.data_loader import load_all_json_files
from core.preprocessing import clean_and_engineer
from core.analysis import (
    analyze_by_hour, analyze_by_day, analyze_age_by_hour
)
from core.visualization import (
    plot_bar, plot_line, plot_scatter, plot_age_hour_heatmap
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

    df_hour = pd.read_csv(os.path.join(SUMMARY_DIR, 'by_hour.csv'))
    df_day = pd.read_csv(os.path.join(SUMMARY_DIR, 'by_day.csv'))

    plot_bar(df_day, '대여_요일', '대여건수', '요일별 대여량', 'day_bar.png')
    plot_line(df_hour, '대여_시간', '대여건수', '시간대별 대여량', 'hour_line.png')

    csv_path = os.path.join(DATA_PROCESSED_DIR, PROCESSED_CSV_FILENAME)
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        pivot_age_hour = analyze_age_by_hour(df)
        plot_age_hour_heatmap(pivot_age_hour, '연령대-시간대별 대여량 히트맵', 'age_hour_heatmap.png')
        
    logger.info("시각화 이미지 저장 완료")

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