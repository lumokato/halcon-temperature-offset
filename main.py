from api.calib import calib_change
from api.coordinate import multi_coordinate, multi_cal_focus
from api.temperature import data_temperature


def cal_and_plot(camera, index):
    multi_coordinate(camera, index, 0, 1, 0)
    print('左相机坐标生成完毕')
    multi_coordinate(camera, index, 0, 0, 0)
    print('右相机坐标生成完毕')
    data_temperature(camera, index, 727.947, 1400.51, 1042.72, 2206.59)
    print('温度生成完毕')


if __name__ == '__main__':
    cal_and_plot('N5', '6')
    # cal_and_plot('N5', 4)
    # multi_cal_focus('N5', 4, 1, 0)
