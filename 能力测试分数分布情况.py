import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple
from matplotlib import font_manager
import numpy as np
import math
from scipy import stats
from math import floor


font_path = 'C:\\Windows\\Fonts\\msyh.ttc'  # 微软雅黑字体路径，Windows系统
font_prop = font_manager.FontProperties(fname=font_path)

data = pd.read_excel('result.xlsx')
score_rank:List[Tuple[int, int]] = []

for score, rank in zip(data['Q2. 您的能力测试得分为'], data['Q3. 您的能力测试排名（整数）为']):
    try:
        score, rank = int(score), int(rank)
        if rank <= 0 or score <= 0:
            continue
    except ValueError:
        print('ValueError:', score, rank)
        continue
    score_rank.append((score, rank))
scores, ranks = zip(*sorted(score_rank, key=lambda x: x[0]))

scores = np.array(scores)
ranks = np.array(ranks)

def split_normals_outliers(x: np.ndarray, y: np.ndarray, xmin: float, xmax: float) ->\
    Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    """
    将数据点分为正常点和离群点，其中离群点为 xmin 到 xmax 范围内远离最小二乘法拟合直线的点。

    参数：
    x (np.ndarray): x 轴数据（例如，得分）。
    y (np.ndarray): y 轴数据（例如，排名）。
    xmin (float): x 轴的最小阈值。
    xmax (float): x 轴的最大阈值。

    返回：
    Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
        - 第一个元组包含正常点的 (x, y) 数组。
        - 第二个元组包含离群点的 (x, y) 数组。
    """
    # 使用最小二乘法拟合直线
    in_idx = np.where(np.logical_and(xmin <= x, x < xmax))[0]
    out_idx = np.where(np.logical_or(xmin > x, x >= xmax))[0]
    x_in, y_in = x[in_idx], y[in_idx]
    A = np.vstack([x_in, np.ones(len(x_in))]).T
    slope, intercept = np.linalg.lstsq(A, y_in, rcond=None)[0]

    # 计算拟合直线上的对应 y 值
    fitted_y = slope * x_in + intercept

    # 计算每个点到拟合直线的垂直距离
    distances = np.abs(y_in - fitted_y)

    # 设定一个距离阈值，使用距离的平均值加上 2 倍标准差作为阈值
    threshold = np.mean(distances) + 2 * np.std(distances)

    # 分离正常点和离群点
    outlier_idx = in_idx[np.where(distances > threshold)[0]]
    normal_idx = np.concatenate([out_idx, in_idx[np.where(distances <= threshold)[0]]])
    # 提取正常点和离群点的 x 和 y 值
    normal_x = x[normal_idx]
    normal_y = y[normal_idx]
    outlier_x = x[outlier_idx]
    outlier_y = y[outlier_idx]

    # 返回 (正常点的 (x, y), 离群点的 (x, y))
    return (normal_x, normal_y), (outlier_x, outlier_y)

(normal_x, normal_y), (outlier_x, outlier_y) = split_normals_outliers(scores, ranks, 70, 86)

grade = [0 for i in range(60)]
count = [0 for i in range(60)]
for x, y in zip(normal_x, normal_y):
    grade[x - 40] += y
    count[x - 40] += 1
for i in range(60):
    if count[i] != 0:
        grade[i] = grade[i] / count[i]
cnt = []
now = 59
while grade[now] == 0:
    now -= 1
count[now] = grade[now]
for i in range(round(grade[now])):
    cnt.append(now + 40)
last = now - 1
while last >= 0:
    while last >= 0 and grade[last] == 0:
        last -= 1
    if last < 0:
        break
    for i in range(last, now):
        count[i] = (grade[last] - grade[now]) / (now - last)
    for i in range(round(grade[now]), round(grade[last]) + 1):
        cnt.append(40 + round(last + (i - round(grade[now])) / (round(grade[last]) - round(grade[now])) * (now - last)))
    now = last
    last = now - 1

# plt.plot([i + 40 for i in range(60)], count)
# plt.xlabel("分数", fontproperties=font_prop)
# plt.ylabel("人数", fontproperties=font_prop)
# plt.title("能力测试分数分布情况", fontproperties=font_prop)
# plt.show()
# plt.tight_layout()
# plt.savefig("能力测试分数分布情况.png", dpi=600)

bins = np.arange(40, 100, 3)
hist, bin_edges = np.histogram(cnt, bins)

# 绘制柱状图
plt.bar(bin_edges[:-1], hist, width=3, align='edge')

# 添加标题和标签
plt.title('成绩分布柱状图', fontproperties=font_prop)
plt.xlabel('分数区间', fontproperties=font_prop)
plt.ylabel('人数', fontproperties=font_prop)

# 显示图形
# plt.show()
plt.tight_layout()
plt.savefig("./output/能力测试分数分布情况柱状图.png", dpi=600)