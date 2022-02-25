import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from .read_csv import read_multi, read_coeff, read_coor, read_tem, read_param, read_focus
mpl.rcParams['font.sans-serif'] = ['SimHei', 'KaiTi', 'FangSong']  # 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
mpl.rcParams['font.size'] = 10  # 字体大小
mpl.rcParams['axes.unicode_minus'] = False  # 正常显示负号


def plot_coeff(index):
    """绘制线性回归参数"""
    coeff_data = read_coeff(index)
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 3, 1)
    ax2 = fig.add_subplot(2, 3, 2)
    ax3 = fig.add_subplot(2, 3, 3)
    ax4 = fig.add_subplot(2, 3, 4)
    ax5 = fig.add_subplot(2, 3, 5)
    ax6 = fig.add_subplot(2, 3, 6)
    x = np.linspace(0, len(coeff_data)/120, len(coeff_data))
    y = np.array(list(coeff_data.values()))
    # 绘制图像
    ax1.scatter(x, y[:, 0], color='navy', s=3)
    ax2.scatter(x, y[:, 1], color='navy', s=3)
    ax3.scatter(x, y[:, 2], color='navy', s=3)
    ax4.scatter(x, y[:, 3], color='black', s=3)
    ax5.scatter(x, y[:, 4], color='black', s=3)
    ax6.scatter(x, y[:, 5], color='black', s=3)
    # 坐标轴
    ax1.set_title("θ1")
    ax2.set_title("θ2")
    ax3.set_title("θ0")
    ax1.set_ylabel("行坐标回归参数")
    ax4.set_ylabel("列坐标回归参数")
    ax4.set_xlabel("时间/h")
    ax5.set_xlabel("时间/h")
    ax6.set_xlabel("时间/h")
    plt.show()


def plot_corr(index):
    """绘制标志点平均位置与参考位置的差值"""
    corr_data = read_coor(index)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    x = np.linspace(0, len(corr_data)/120, len(corr_data))
    y = np.array(list(corr_data.values()))
    ax1.scatter(x, y[:, 0], color='navy', s=3)
    ax1.set_title("行坐标变化")
    ax1.set_xlabel("时间/h")
    ax1.set_ylabel("像素")
    ax2.scatter(x, y[:, 1], color='black', s=3)
    ax2.set_title("列坐标变化")
    ax2.set_xlabel("时间/h")
    plt.show()


def plot_param(index):
    """绘制相机焦距与主点坐标参数"""
    param_data = read_param(index)
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(223)
    ax3 = fig.add_subplot(224)
    x = np.linspace(0, len(param_data)/120, len(param_data))
    y = np.array(list(param_data.values()))
    # 绘制图像
    ax1.scatter(x, y[:, 0], color='navy', s=3)
    ax2.scatter(x, y[:, 1], color='navy', s=3)
    ax3.scatter(x, y[:, 2], color='navy', s=3)
    # 坐标轴
    ax1.set_title("焦距")
    ax2.set_title("主点行坐标")
    ax3.set_title("主点列坐标")
    ax1.set_ylabel("mm")
    ax2.set_ylabel("像素")
    ax1.set_xlabel("时间/h")
    ax2.set_xlabel("时间/h")
    ax3.set_xlabel("时间/h")
    plt.show()


def plot_tem(index):
    """绘制温度变化曲线"""
    tem_data = read_tem(index)
    x = np.linspace(0, len(tem_data)/120, len(tem_data))
    y = np.array(list(tem_data.values()))
    plt.plot(x, y)
    plt.title("温度随时间变化曲线")
    plt.xlabel("时间/h")
    plt.ylabel("°C")
    plt.show()


def plot_multi_tem(index, tem=False):
    """位置差值与温度变化显示在同一张图中, tem为True时读取温度修正后的数据"""
    Row_data, Column_data = read_multi(index, tem)
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    timeline = np.linspace(0, (len(Row_data)-3)/120, len(Row_data)-3)
    Row_array = np.array(list(Row_data.values()))
    for i in range(77):
        ax1.plot(timeline, Row_array[3:, i], linewidth=0.3)
    ax1.set_title("行坐标变化随时间分布")
    ax1.set_xlabel("时间/h")
    ax1.set_ylabel("像素")
    ax2 = fig.add_subplot(2, 2, 2)
    Column_array = np.array(list(Column_data.values()))
    for i in range(77):
        ax2.plot(timeline, Column_array[3:, i], linewidth=0.3)
    ax2.set_title("列坐标变化随时间分布")
    ax2.set_xlabel("时间/h")
    # 绘制温度
    ax3 = fig.add_subplot(2, 2, 4)
    tem_data = read_tem(index)
    x = np.linspace(0, len(tem_data)/120, len(tem_data))
    y = np.array(list(tem_data.values()))
    ax3.plot(x, y)
    ax3.set_title("温度随时间变化曲线")
    ax3.set_xlabel("时间/h")
    ax3.set_ylabel("°C")
    plt.show()


def plot_tem_all():
    """绘制温度变化曲线"""
    tem_data = read_tem('N4-2')
    tem_data1 = read_tem('N4-4')
    tem_data2 = read_tem('N4-5')
    x = np.linspace(0, len(tem_data)/120, len(tem_data))
    y = np.array(list(tem_data.values()))
    plt.plot(x, y, label='4-2')
    plt.plot(np.linspace(0, len(tem_data1)/120, len(tem_data1)), np.array(list(tem_data1.values())), label='4-3')
    plt.plot(np.linspace(0, len(tem_data2)/120, len(tem_data2)), np.array(list(tem_data2.values())), label='4-5')
    plt.title("温度随时间变化曲线")
    plt.xlabel("时间/h")
    plt.ylabel("°C")
    plt.legend()
    plt.show()


def plot_multi_tem_plus(index, tem=False):
    """位置差值与温度变化显示在同一张图中, 加入2h与0h坐标点对比, tem为True时读取温度修正后的数据"""
    Row_data, Column_data = read_multi(index, tem)
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 3, 1)
    timeline = np.linspace(0, (len(Row_data)-3)/120, len(Row_data)-3)
    Row_array = np.array(list(Row_data.values()))
    for i in range(77):
        ax1.plot(timeline, Row_array[3:, i], linewidth=0.3)
    ax1.set_title("行坐标变化随时间分布")
    ax1.set_xlabel("时间/h")
    ax1.set_ylabel("像素")
    ax2 = fig.add_subplot(2, 3, 4)
    Column_array = np.array(list(Column_data.values()))
    for i in range(77):
        ax2.plot(timeline, Column_array[3:, i], linewidth=0.3)
    ax2.set_title("列坐标变化随时间分布")
    ax2.set_xlabel("时间/h")
    # 绘制2h与0h坐标点对比
    ax3 = fig.add_subplot(2, 3, 2)
    ax3.scatter(Row_data[-2], Row_array[330], color='black', s=3)
    ax4 = fig.add_subplot(2, 3, 3)
    ax4.scatter(Row_data[-2], Column_array[330], color='black', s=3)
    ax5 = fig.add_subplot(2, 3, 5)
    ax5.scatter(Column_data[-1], Row_array[330], color='black', s=3)
    ax6 = fig.add_subplot(2, 3, 6)
    ax6.scatter(Column_data[-1], Column_array[330], color='black', s=3)
    plt.show()


def plot_focus(index):
    """绘制所有标志点位置与参考位置的差值, tem为True时读取温度修正后的数据"""
    focus_data = read_focus(index)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    timeline = np.linspace(0, len(focus_data)/120, len(focus_data))
    focus_array = np.array(list(focus_data.values()))
    focus = []
    for i in focus_data.keys():
        focus.append(np.sqrt(focus_data[i][0]**2/2+focus_data[i][1]**2/2))
    ax1.plot(timeline, focus, linewidth=0.3)
    # ax1.plot(timeline, focus_array[:, 1], linewidth=0.3)
    plt.show()
    # ax1.set_title("行坐标变化随时间分布")
    # ax1.set_xlabel("时间/h")
    # ax1.set_ylabel("像素")
    # ax2 = fig.add_subplot(1, 2, 2)
    # Column_array = np.array(list(Column_data.values()))
    # for i in range(77):
    #     ax2.plot(timeline, Column_array[3:, i], linewidth=0.3)
    # ax2.set_title("列坐标变化随时间分布")
    # ax2.set_xlabel("时间/h")
    # plt.show()


def subplot(sub, multi_data):
    """绘制坐标变化趋势子图"""
    timeline = np.linspace(0, (len(multi_data)-3)/120, len(multi_data)-3)
    array = np.array(list(multi_data.values()))
    for i in range(len(array[0])):
        Rowi = array[3:, i]
        Index = np.argwhere(abs(Rowi) > 15)  # 排除中途识别到的点
        if Rowi[1] > 0:  # 排除一直未识别到的点
            sub.plot(np.delete(timeline, Index), np.delete(Rowi, Index), linewidth=0.3)


def plot_multi(index, tem=False):
    """绘制所有标志点位置与参考位置的差值, tem为True时读取温度修正后的数据"""
    Row_data, Column_data = read_multi(index, tem)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    subplot(ax1, Row_data)
    subplot(ax2, Column_data)
    ax1.set_title("行坐标变化随时间分布")
    ax1.set_xlabel("时间/h")
    ax1.set_ylabel("像素")
    ax2.set_title("列坐标变化随时间分布")
    ax2.set_xlabel("时间/h")
    plt.show()


def plot_multi_LR(index, tem=False):
    """绘制所有标志点位置与参考位置的差值, tem为True时读取温度修正后的数据"""
    Row_data, Column_data = read_multi(index, tem)
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    subplot(ax1, Row_data)
    subplot(ax2, Column_data)
    ax1.set_title("行坐标变化随时间分布")
    ax1.set_ylabel("左相机/像素")
    ax2.set_title("列坐标变化随时间分布")
    # 右相机
    Row_dataR, Column_dataR = read_multi(index+'R', tem)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    subplot(ax3, Row_dataR)
    subplot(ax4, Column_dataR)
    ax3.set_xlabel("时间/h")
    ax3.set_ylabel("右相机/像素")
    ax4.set_xlabel("时间/h")
    plt.show()


def plot_multi_plus(index, tem=False):
    """位置差值加入2h与0h坐标点对比, tem为True时读取温度修正后的数据"""
    Row_data, Column_data = read_multi(index, tem)
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 4, 1)
    ax2 = fig.add_subplot(2, 4, 5)
    subplot(ax1, Row_data)
    subplot(ax2, Column_data)
    ax1.set_title("行坐标变化随时间分布")
    ax1.set_xlabel("时间/h")
    ax1.set_ylabel("像素")
    ax2.set_title("列坐标变化随时间分布")
    ax2.set_xlabel("时间/h")
    # 绘制2h与0h坐标点对比
    compare = 233
    Row_array = np.array(list(Row_data.values()))
    Column_array = np.array(list(Column_data.values()))
    ax3 = fig.add_subplot(242)
    ax3.scatter(Row_data[-2], Row_array[compare], color='black', s=3)
    ax4 = fig.add_subplot(243)
    ax4.scatter(Row_data[-1], Row_array[compare], color='black', s=3)
    ax7 = fig.add_subplot(244)
    ax7.scatter(Row_data[-3], Row_array[compare], color='black', s=3)

    ax5 = fig.add_subplot(246)
    ax5.scatter(Column_data[-2], Column_array[compare], color='black', s=3)
    ax6 = fig.add_subplot(247)
    ax6.scatter(Column_data[-1], Column_array[compare], color='black', s=3)
    ax8 = fig.add_subplot(248)
    ax8.scatter(Column_data[-3], Column_array[compare], color='black', s=3)
    plt.show()


if __name__ == '__main__':
    plot_multi_LR('N5-4')
