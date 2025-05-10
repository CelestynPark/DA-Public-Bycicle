# 서울시 공공자전거 이용 분석 프로젝트

서울시 공공자전거(따릉이) 데이터를 활용하여, 시간대, 요일, 성별, 연령대, 대여소 등의 다양한 조건에서 대여 패턴을 분석하고 시각화하는 프로젝트이다.

---

## 프로젝트

- **데이터 출처**: 서울열린데이터광장
- **데이터 형식**: 월별 JSON (예: `202401.json`)
- **분석 대상 기간**: 2024년 월 ~ 2025년 4월
- **활용 기술**: Python (Pandas, matplotlib, seaborn), CLI 기반 실행, 모듈화 구조

---

## 디렉토리 구조

```
da-public_bicycle/
├── Readme.md           # 프로젝트 문서
├── requirements.txt    # 설치 패키지 목록
├── main.py             # 전체 자동 실행용 메인
├── cli/                # CLI 실행 진입점 및 실행 함수
│   ├── main.py         # argparse CLI
│   └── __ini__.py      # main.py에서 함수 임포트용
├── config/             # 설정 정보 (경로 등)
│   └── settings.py
├── core/               # 핵심 로직
│   ├── analysis.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   └── visualization.py
├── data/               # 데이터 디렉토리
│   ├── raw/            # 원본 JSON 데이터
│   └── processed/      # 전처리된 CSV 저장
├── logs/
│   └── project.log     # 실행 로그
├── outputs/
│   ├── summary/        # 분석 요약 CSV
│   └── figures/        # 시각화 이미지
├── scripts/
│   └── scarpper.py     # 데이터를 스크래퍼
└── utils/              # 유틸리티 도구 (logger)
```

---

## 설치 및 실행 방법

### 1. 가상 환경 구성

```bash
bython -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. API 키 설정 (.env)

서울시 Open API를 사용하려면 `.env` 파일을 프로젝트 루트에 생성하고 다음처럼 설정한다:

```bash
SEOUL_API_KEY=서울시OpenAPI키
```

### 3. 데이터 수집 (크롤링)

서울열린데이터광장의 공공자전거 시간대별 API를 통해 월별 JSON 파일을 수집한다.

#### 실행 방법

```bash
python scripts/crawler.py
```

- 기본 저장 경로: data/raw/{YYYYMM}.json
- 기간: 2024년 1월 ~ 2025년 4월
- 하루 24시간, 최대 1000건 단위로 분할 수집
- API 요청 실패 시 최대 3회 재시도

### 4. 전체 파이프라인 실행

```bash
python main.py
```

또는 세부 실행

```bash
python cli/main.py --mode preprocess    # 전처리 실행
python cli/main.py --mode analyze       # 분석 CSV 생성
python cli/main.py --mode visualize     # 시각화 이미지 생성
```

---

## 주요 분석 내용 및 결과

### 시간대/요일별 대여량

- `by_hour.csv`, `by_day.csv`
- 시각화: `hour_line.png`, `day_bar.png`

### 연령대-시간대 이용 패턴

- 분석: `analyze_age_by_hour`
- 시각화: `age_hour_heatmap.png`

### 대여소별 평균 이동 거리

- Top 10 대여소 기준 평균 거리 추출
- 시각화: `top_station_distance.png`

### 성별-연령대별 대여량

- 분석: `analyze_gender_age_heatmap`
- 시각화: `gender_age_heatmap.png`

### 운동량 및 탄소 절감량 트렌드

- 일자별 `EXER_AMT`, `CARBON_AMT` 합계
- 시각화: `energy_carbon_trend.png`

---

## 사용된 주요 기술

| 구분        | 기술                                |
| ----------- | ----------------------------------- |
| 데이터 처리 | pandas, json                        |
| 시각화      | matplotlib, seaborn                 |
| 실행 관리   | argparse, logging                   |
| 구조화      | 모듈 기반 CLI 구조, main entry 분리 |

---

## 주요 컬럼 설명

| 컬럼명     | 설명                          |
| ---------- | ----------------------------- |
| RENT_DT    | 대여 날짜                     |
| RENT_HR    | 대여 시간 (0~23시)            |
| RENT_ID/NM | 대여소 ID 및 이름             |
| RENT_TYPE  | 대여 유형 (정기권, 일일권 등) |
| USE_CNT    | 해당 조건 내 이용 건수        |
| GENDER_CD  | 성별 (M, F, 비회원은 공백)    |
| AGE_TYPE   | 연령대 (예: "20대", "60대~")  |
| MOVE_METER | 이동 거리 (m)                 |
| MOVE_TIME  | 이동 시간 (분)                |
| EXER_AMT   | 소모 칼로리 (kcal)            |
| CARBON_AMT | 절감 CO₂량 (kg)               |

---

## 참고

- 월별 JSON은 `data/raw` 디렉토리에 스크래핑을 통해 배치
- 시각화 및 로그는 `outputs/`, `logs/` 폴더에 자동 생성됨

---

## 작성자

- Github: [CelestynPark]
- Contact: sbeep2001@gmail.com
