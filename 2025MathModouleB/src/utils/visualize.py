# src/utils/visualize.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib import font_manager
import warnings
warnings.filterwarnings("ignore")
font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'  # 适配 Linux
my_font = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = [my_font.get_name()]
def plot_scores(df: pd.DataFrame, score_col: str = '综合得分', top_n: int = 10):
    """
    绘制企业得分条形图
    """
    top_df = df.sort_values(by=score_col, ascending=False).head(top_n)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_df, x='企业编号', y=score_col, palette='Blues_d')
    plt.title(f'前{top_n}家企业综合得分柱状图')
    plt.ylabel("综合得分")
    plt.xlabel("企业编号")
    plt.tight_layout()
    plt.show()
