import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from matplotlib import font_manager
import math

font_path = 'C:\\Windows\\Fonts\\msyh.ttc'  # 微软雅黑字体路径，Windows系统
font_prop = font_manager.FontProperties(fname=font_path)

data = pd.read_excel('result.xlsx')

# refer to https://www.seiee.sjtu.edu.cn/xzzx_notice_bks_cat2/11274.html
major_hc = {
    '计算机': 92,
    '软件工程':76,
    '信息安全':72,
    '自动化':79,
    '微电子':69,
    '信息工程':124,
    '电子科学':67,
    '电气工程':116,
    '智能感知':76,
}
accept:Dict[str, List[int]] = {}

for rank, major in zip(data['Q5. 您的综合排名（整数）为'], data['Q6. 您的录取专业为']):
    if major not in accept.keys():
        accept[major] = []
    rank = int(rank)
    accept[major].append(rank)

major_list:List[Tuple[str, int, int, int, int]] = []
for major, ranks in accept.items():
    last_rank = max(ranks)
    first_rank = min(ranks)
    count_rank = len(ranks)
    hc = major_hc[major]
    major_list.append((major, first_rank, last_rank, count_rank, hc))
major_list = sorted(major_list, key=lambda x: x[2])

df = pd.DataFrame(columns=['录取专业', '样本排名最小值', '样本排名最大值', '样本数', '计划录取人数', '累计录取人数'])
df['录取专业'], df['样本排名最小值'], df['样本排名最大值'], df['样本数'], df['计划录取人数'] = zip(*major_list)
df['累计录取人数'] = df['计划录取人数'].cumsum()

total = pd.DataFrame([{
    '录取专业': '总计',
    '样本排名最小值': df['样本排名最小值'].min(),
    '样本排名最大值': df['样本排名最大值'].max(),
    '样本数': df['样本数'].sum(),
    '计划录取人数': df['计划录取人数'].sum(),
    '累计录取人数': '--',
}])
df = pd.concat([df, total], ignore_index=True)

fig, ax = plt.subplots(figsize=(8, 3))  # 可以根据需要调整figsize

# 隐藏 x 和 y 轴
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# 隐藏顶边和右边的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

tbl = plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colWidths=[0.2] * len(df.columns))

table_font_prop = font_manager.FontProperties(fname=font_path, size=10)
for key, cell in tbl.get_celld().items():
    cell.get_text().set_fontproperties(font_prop)
    cell.get_text().set_fontsize(10)
    cell.get_text().set_ha('center')
    cell.get_text().set_va('center')

    # 设置标题栏背景颜色
    if key[0] == 0:
        cell.set_facecolor("#cce5ff")  # 淡蓝色
    elif key[0] == len(df):
        cell.set_facecolor("#d9edf7")  # 更深的蓝色
    cell.set_edgecolor('black')

tbl.auto_set_font_size(False)
tbl.set_fontsize(12)
tbl.scale(1.2, 1.2)

# plt.show()
plt.tight_layout()
plt.margins(0, 0)
plt.savefig("./output/各专业录取概况表.png",dpi=600,bbox_inches='tight')
