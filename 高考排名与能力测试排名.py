import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import math
import numpy as np

font_path = 'C:\\Windows\\Fonts\\msyh.ttc'  # 微软雅黑字体路径，Windows系统
font_prop = font_manager.FontProperties(fname=font_path)

data = pd.read_excel('result.xlsx')

x = []
y = []
for rankgk, ranknl in zip(data['Q1. 您的高考排名为'], data['Q3. 您的能力测试排名（整数）为']):
    try:
        rankgk = int(rankgk)
        ranknl = int(ranknl)
    except:
        continue
    if rankgk == 0 or ranknl == 0: continue
    x.append(rankgk)
    y.append(ranknl)

# 使用NumPy函数计算相关系数矩阵

# 使用单独的NumPy函数提取相关系数
correlation = np.corrcoef(x, y)[0, 1]

table_data = [
    ["协方差", f"{correlation:.4f}"],
]

table_font_prop = font_manager.FontProperties(fname=font_path, size=10)

# 添加表格到图中
the_table = plt.table(cellText=table_data, cellLoc='center', colLoc='center', loc='right', bbox=[0.78, 0, 0.22, 0.1])
the_table.auto_set_font_size(False)
the_table.set_fontsize(10)

for key, cell in the_table.get_celld().items():
    cell.get_text().set_fontproperties(table_font_prop)

plt.title('高考排名与能力测试排名散点图', fontproperties=font_prop)
plt.scatter(x, y, marker='x', alpha=0.7)
plt.xlabel("高考排名", fontproperties=font_prop)
plt.ylabel("能力测试排名", fontproperties=font_prop)
plt.tight_layout()
# plt.show()
plt.savefig('./output/高考排名与能力测试排名散点图.png', dpi=600)
