import os
import matplotlib.pyplot as plt
import seaborn as sns
from config.settings import FIGURE_DIR
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import platform

if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

def plot_bar(df, x, y, title, filename):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=x, y=y, data=df)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURE_DIR, filename))
    plt.close()

def plot_line(df, x, y, title, filename):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=x, y=y, data=df, markers='o')
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURE_DIR, filename))
    plt.close()

def plot_scatter(df, x, y, title, filename):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x, y=y, data=df)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURE_DIR, filename))
    plt.close()

def plot_age_hour_heatmap(df, title, filename):
    plt.figure(figsize=(10, 6))
    sns.heatmap(df, annot=True, fmt='g', cmap='YlGnBu')
    plt.title(title)
    plt.xlabel('시간대')
    plt.ylabel('연령대')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURE_DIR, filename))
    plt.close()

def plot_top_station_distance(df: pd.DataFrame, title: str, filename: str):
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x='평균이동거리',
        y='RENT_NM',
        data=df.sort_values('평균이동거리'),
        palette='Blues_d'
    )
    plt.title(title)
    plt.xlabel('평균 이동 거리 (m)')
    plt.ylabel('대여소명')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURE_DIR, filename))
    plt.close()

def plot_gender_age_heatmap(pivot_df: pd.DataFrame, title: str, filename: str):
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_df, annot=True, fmt='g', cmap='YlOrBr')
    plt.title(title)
    plt.xlabel('연령대')
    plt.ylabel('성별')
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURE_DIR, filename))
    plt.close()

def plot_energy_carbon_trend(df: pd.DataFrame, title: str, filename: str):
    plt.figure(figsize=(12, 6))
    plt.plot(df['RENT_DT'], df['EXER_AMT'], label='소모 칼로리 (kcal)', color='tomato')
    plt.plot(df['RENT_DT'], df['CARBON_AMT'], label='절감 CO₂ (kg)', color='seagreen')
    plt.title(title)
    plt.xlabel('날짜')
    plt.ylabel('값')
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURE_DIR, filename))
    plt.close()

def plot_station_map(df: pd.DataFrame, filename: str = 'station_map.html'):
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=14)
    cluster = MarkerCluster().add_to(m)
    
    for _, row in df.iterrows():
        lat, lng = row['LAT'], row['LONG']
        folium.CircleMarker(
            location=(lat, lng),
            radius=max(min(row['USE_CNT'] / 5000, 15), 5),
            color='black',
            fill=True,
            fill_color='orange',
            fill_opacity=0.7,
            popup=folium.Popup(
                f"<b>{row['RENT_NM_x']}</b><br>이용수: {int(row['USE_CNT'])}<br>평균거리: {row['평균이동거리']: 1f}m",
                max_width=250
            )
        ).add_to(cluster)

    output_path = os.path.join(FIGURE_DIR, filename)
    m.save(output_path)