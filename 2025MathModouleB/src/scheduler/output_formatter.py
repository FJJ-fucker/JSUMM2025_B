from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from matplotlib import font_manager
warnings.filterwarnings("ignore")
font_path = '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc'  # 适配 Linux
my_font = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = [my_font.get_name()]
def print_schedule_table(assignment):
    days = ['周一', '周二', '周三', '周四', '周五']
    areas = ['A1', 'A2', 'B1', 'B2']
    table = pd.DataFrame(index=days, columns=areas)
    for day in days:
        for area in areas:
            count = defaultdict(int)
            for booth in assignment[day][area]:
                count[booth['企业代号']] += 1
            table.loc[day, area] = ', '.join(f"{k} x{v}" for k, v in count.items()) if count else ''
    print(table)

def plot_assignment_distribution(assignment, enterprise_df):
    from collections import defaultdict
    assigned_time = defaultdict(float)
    for day in assignment:
        for area in assignment[day]:
            for booth in assignment[day][area]:
                assigned_time[booth['企业代号']] += booth['时长']

    df = pd.DataFrame([
        {'企业代号': k, '分配时间': v} for k, v in assigned_time.items()
    ])
    df = df.sort_values(by='分配时间', ascending=False)
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df, x='企业代号', y='分配时间', palette='crest')
    plt.title('各企业总分配时间')
    plt.ylabel('小时')
    plt.show()