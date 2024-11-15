import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple
from matplotlib import font_manager
import math
from scipy.stats import linregress

font_path = 'C:\\Windows\\Fonts\\msyh.ttc'  # 微软雅黑字体路径，Windows系统
font_prop = font_manager.FontProperties(fname=font_path)

data = pd.read_excel('result.xlsx')

x = []
y = []
for rankgk, ranknl in zip(data['Q1. 您的高考排名为'], data['Q5. 您的综合排名（整数）为']):
    try:
        rankgk = int(rankgk)
        ranknl = int(ranknl)
    except:
        continue
    if rankgk == 0 or ranknl == 0: continue
    x.append(rankgk)
    y.append(ranknl)

slope, intercept, r_value, p_value, std_err = linregress(x, y)
table_data = [
    ["斜率", f"{slope:.2f}"],
    ["截距", f"{intercept:.2f}"],
    ["相关系数", f"{r_value:.2f}"],
]

table_font_prop = font_manager.FontProperties(fname=font_path, size=10)

# 添加表格到图中
the_table = plt.table(cellText=table_data, colLabels=["特征", "值"], cellLoc='center', colLoc='center', loc='right', bbox=[0.7, 0.2, 0.3, 0.4])
the_table.auto_set_font_size(False)
the_table.set_fontsize(10)

# 设置表格字体为中文字体
for key, cell in the_table.get_celld().items():
    cell.get_text().set_fontproperties(table_font_prop)

plt.subplots_adjust(right=0.8)

plt.title('高考排名与综合排名关系图', fontproperties=font_prop)
plt.scatter(x, y, marker='x', alpha=0.7, label='样本')
plt.xlabel("高考排名", fontproperties=font_prop)
plt.ylabel("综合排名", fontproperties=font_prop)
x_range = [min(x), max(x)]
y_range = [slope * x_val + intercept for x_val in x_range]
plt.plot(x_range, y_range, color="red", label="回归直线", alpha=0.7)
plt.legend(prop=font_prop)
plt.tight_layout()
# plt.show()
plt.savefig('./output/高考排名与综合排名散点图.png', dpi=600)
