import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import seaborn as sns
import numpy as np
from typing import Dict, List
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

font_path = 'C:\\Windows\\Fonts\\msyh.ttc'
font_prop = font_manager.FontProperties(fname=font_path)

# 导入数据
data = pd.read_excel('result.xlsx')

accept:Dict[str, List[int]] = {}
reject:Dict[str, List[int]] = {}
for rank, major in zip(data['Q5. 您的综合排名（整数）为'], data['Q6. 您的录取专业为']):
    if major not in accept:
        accept[major] = []
        reject[major] = []
    rank = int(rank)
    if rank <= 0: continue
    accept[major].append(rank)
for rank, majors in zip(data['Q5. 您的综合排名（整数）为'], data['Q7. 您是否有未被录取的专业']):
    majors:str = majors.strip()
    rank = int(rank)
    if rank <= 0: continue
    if majors == '我是第一志愿录取的':
        continue
    for major in majors.split('、'):
        reject[major.strip()].append(rank)

min_rejected_rank:Dict[str, int] = {} # 每个专业的最高未录取志愿综合排名
for major, ranks in reject.items():
    if len(ranks) != 0:
        min_rejected_rank[major] = min(ranks)

# 按中位数排序专业
major_list = sorted(accept.items(), key=lambda x: np.median(x[1]))
x_labels = [major for major, _ in major_list]
data['Q6. 您的录取专业为'] = pd.Categorical(data['Q6. 您的录取专业为'], categories=x_labels, ordered=True)
data = data.sort_values(by='Q6. 您的录取专业为')

# 绘制箱型图
plt.figure(figsize=(18, 8))
boxplot = sns.boxplot(
    x='Q6. 您的录取专业为',
    y='Q5. 您的综合排名（整数）为',
    data=data,
    width=0.6,
    showmeans=True,
    meanprops={"marker": "X"},
    showfliers=False,
    whis=0,
    color='#47729E',
)

# 添加标题和标签
plt.title('电院分流排名', fontproperties=font_prop, fontsize=16)
plt.xlabel('专业', fontproperties=font_prop, fontsize=12)
plt.ylabel('排名', fontproperties=font_prop, fontsize=12)
plt.xticks(fontproperties=font_prop)

reject_scatter_x = []
reject_scatter_y = []
# 添加平均数、四分位数和离群点注释
for i, category in enumerate(x_labels):
    subset = data[data['Q6. 您的录取专业为'] == category]['Q5. 您的综合排名（整数）为']
    mean_val = subset.mean()
    q1 = subset.quantile(0.25)
    median = subset.median()
    q3 = subset.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = subset[(subset < lower_bound) | (subset > upper_bound)]
    min_reject = min_rejected_rank.get(category, None)
    if min_reject != None:
        reject_scatter_x.append(i)
        reject_scatter_y.append(min_reject)
        plt.text(i, min_reject+10, str(min_reject), ha='center', color='red')
    # 添加均值标签
    plt.text(i, mean_val, f'{int(mean_val)}', ha='center', va='bottom', color='black', fontproperties=font_prop)
    # 添加四分位数标签
    plt.text(i + 0.5, q1, f'{int(q1)}', ha='right', va='center', color='black', fontproperties=font_prop)
    plt.text(i + 0.5, median, f'{int(median)}', ha='right', va='center', color='black', fontproperties=font_prop)
    plt.text(i + 0.5, q3, f'{int(q3)}', ha='right', va='center', color='black', fontproperties=font_prop)

    lower_whisker = max(subset.min(), q1 - 1.5 * iqr)
    upper_whisker = min(subset.max(), q3 + 1.5 * iqr)

    plt.plot([i, i], [lower_whisker, q1], color='black', linewidth=1.5)  # 下须弥线
    plt.plot([i, i], [q3, upper_whisker], color='black', linewidth=1.5)  # 上须弥线

    plt.plot([i - 0.15, i + 0.15], [lower_whisker, lower_whisker], color='black', linewidth=1.5)  # 下须弥线横线
    plt.plot([i - 0.15, i + 0.15], [upper_whisker, upper_whisker], color='black', linewidth=1.5)  # 上须弥线横线

    # 标注最大和最小须弥线值
    plt.text(i + 0.25, lower_whisker, f'{int(lower_whisker)}', ha='center', va='top', color='black', fontproperties=font_prop)
    plt.text(i + 0.25, upper_whisker, f'{int(upper_whisker)}', ha='center', va='bottom', color='black',
             fontproperties=font_prop)
    # 添加离群点标签
    outliers = subset[(subset < lower_whisker) | (subset > upper_whisker)]
    for outlier in outliers:
        plt.plot(i, outlier, 'o', color='blue')  # 使用 'o' 绘制圆点表示离群点
        plt.text(i + 0.2, outlier, f'{int(outlier)}', ha='right', color='purple', fontproperties=font_prop,
                 size='medium')
min_rej_plt = plt.scatter(reject_scatter_x, reject_scatter_y, marker='x', color='red', label='排名最高的未录取志愿')
# 设置 y 轴范围
plt.ylim(0, 800)

# 创建自定义图例元素，使用 'X' 标记表示均值
main_patch = mpatches.Patch(color='#47729E', label=r'25%-75%分位数')
mean_marker = mlines.Line2D([], [], color='green', marker='X', linestyle='None', markersize=8, label='均值')
outlier_marker = mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=6, label='离群点')
minmax_line = mlines.Line2D([], [], color='black', linestyle='-', linewidth=2, label='上下须弥线')
median_line = mlines.Line2D([], [], color='black', linestyle='-', linewidth=1.5, label='中位排名')

# 添加图例
plt.legend(handles=[main_patch, mean_marker, outlier_marker, median_line, minmax_line, min_rej_plt], loc='upper left', prop=font_prop)

# 设置字体路径（根据系统情况调整路径）
plt.tight_layout()
plt.savefig("./output/电院分流排名箱型图.png", dpi = 600)
