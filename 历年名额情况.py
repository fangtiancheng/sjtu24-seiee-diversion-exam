import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = 'C:\\Windows\\Fonts\\msyh.ttc'  # 微软雅黑字体路径，Windows系统
font_prop = font_manager.FontProperties(fname=font_path, size=10)

# 表格数据
data = [
    ["计算机", 87, 82, 92, 94, 92],
    ["软件工程", 77, 72, 73, 75, 76],
    ["信息安全", 62, 58, 68, 71, 72],
    ["自动化", 56, 50, 60, 71, 79],
    ["微电子", 51, 49, 52, 63, 69],
    ["信息工程", 93, 95, 106, 118, 124],
    ["电子科学", 47, 46, 51, 62, 67],
    ["生物医学工程", None, None, 65, 75, None],
    ["电气工程", 91, 92, 96, 109, 116],
    ["测控/智能感知", 51, 49, 55, 66, 76],
]
cum_data = []

# 计算每列的总和，跳过第一列（专业名称额数）
total = ["合计"]
for i in range(len(data)):
    cum_data.append([data[i][0]])
    if i > 0:
        for j in range(1, len(data[0])):
            if data[i][j] != None:
                cum_data[i].append(cum_data[i-1][j]+data[i][j])
            else:
                cum_data[i].append(cum_data[i-1][j])
    else:
        for j in range(1, len(data[0])):
            if data[i][j] != None:
                cum_data[i].append(data[i][j])
            else:
                cum_data[i].append(0)
    if i + 1 == len(data):
        for j in range(1, len(data[0])):
            total.append(cum_data[i][j])

for i in range(len(data)):
    for j in range(1, len(data[0])):
        if data[i][j] == None:
            cum_data[i][j] = None

data.append(total)

def draw_table(ax, data, col_labels, last_blue: bool = True):
    table = ax.table(cellText=data, colLabels=col_labels, cellLoc='center', loc='center', edges='closed')
    ax.axis('off')

    for key, cell in table.get_celld().items():
        cell.get_text().set_fontproperties(font_prop)
        if key[0] == 0:
            cell.set_facecolor("#cce5ff")  # 淡蓝色
        elif last_blue and key[0] == len(data):
            cell.set_facecolor("#d9edf7")  # 更深的蓝色
        cell.set_edgecolor('black')
    table.auto_set_font_size(False)
    table.scale(1.2, 1.5)
    table.set_fontsize(12)

fig, axs = plt.subplots(2, 1, figsize=(9, 8))  # 创建2x1的图
col_label1 = ("专业名额数", "2020年", "2021年", "2022年", "2023年", "2024年")
col_label2 = ("累计名额数", "2020年", "2021年", "2022年", "2023年", "2024年")

draw_table(axs[0], data, col_label1, True)
draw_table(axs[1], cum_data, col_label2, False)

plt.tight_layout()
plt.savefig("./output/历年名额情况表.png", dpi=600, bbox_inches='tight',pad_inches=0.05)
# plt.show()