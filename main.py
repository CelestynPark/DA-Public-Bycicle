from cli.main import run_preprocess, run_analysis, run_visualization, run_quality_check
from utils.logger import setup_logger

logger = setup_logger(__name__)

if __name__ == '__main__':
    logger.info('main.py 실행 시작')

    try:
        # run_preprocess()
        # run_analysis()
        # run_visualization()
        run_quality_check()
    except Exception as e:
        logger.error(f"실행 중 오류 발생: {e}")
    
    logger.info("전체 분석 파이프라인 완료")