import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
FIGURE_DIR = os.path.join(BASE_DIR, 'outputs', 'figures')
SUMMARY_DIR = os.path.join(BASE_DIR, 'outputs', 'summary')
LOG_PATH = os.path.join(BASE_DIR, 'logs', 'project.log')

PROCESSED_CSV_FILENAME = 'bike_cleaned.csv'