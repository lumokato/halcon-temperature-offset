# from api.calib import calib_change
from api.coordinate import multi_coordinate
from api.temperature import data_temperature
import api.plot as plot


def cal_and_plot(camera, index):
    multi_coordinate(camera, index, 0, 1, 0)
    print('左相机坐标生成完毕')
    multi_coordinate(camera, index, 0, 0, 0)
    print('右相机坐标生成完毕')
    data_temperature(camera, index, 727.947, 1400.51, 1042.72, 2206.59)
    print('温度生成完毕')


def main(methods, index):
    for method in methods:
        if method == 'r':   # 单目数据读取
            multi_coordinate(index[:2], index[-1], 0, 1, 0)
        elif method == 'R':  # 双目数据读取
            multi_coordinate(index[:2], index[-1], 0, 1, 0)
            multi_coordinate(index[:2], index[-1], 0, 0, 0)
        elif method == 't':
            data_temperature(index[:2], index[-1], 727.947, 1400.51, 1042.72, 2206.59)
        elif method == 'p':
            plot.plot_multi(index)
        elif method == 'P':
            plot.plot_multi_LR(index)
        elif method == 'T':
            plot.plot_tem(index)


if __name__ == '__main__':
    plot.plot_multi_plus('N6-4')
    # main('rp', 'N6-4')
