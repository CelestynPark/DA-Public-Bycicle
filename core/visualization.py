import os
import matplotlib as plt
import seaborn as sns
from config.settings import FIGURE_DIR

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