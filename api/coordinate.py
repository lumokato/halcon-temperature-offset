"""
随温度变化获取标志点坐标
"""
import os
import numpy as np
from .coeff import mark_coordinate


# 坐标差值
def coordinate_diff(img0, img1):
    """
    读取两张图片标志点的位置, 返回坐标差值

    输入参数
    ----
    img0, img1: 两张图片的路径, img0为参考图片

    返回值
    ---
    dR, dC: 坐标差值
    """
    R0, C0 = mark_coordinate(img0)
    R1, C1 = mark_coordinate(img1)
    dR, dC = np.array(R1)-np.array(R0), np.array(C1)-np.array(C0)
    return dR, dC


def mean_coordinate(camera, index, refer_pic=1, left=True, end_pic=0):
    """
    读取指定路径所有图片标志点的位置, 取平均值后与参考位置做差值, 保存csv文件

    输入参数
    ----
    camera: 指定实验编号

    index: 实验组数

    refer_pic: 参考图片序号, 手动选取温度30°C对应的图片

    left: 默认左相机, 定义0/False为右相机

    end_pic: 读取图片总数, 0代表读取文件夹全部图片

    输出文件
    ---
    data/coor: 平均坐标位置与参考位置差值文件, 命名规则为'实验编号-组别(-R右相机)'
    """
    path = 'G:/point-data/' + str(camera) + '/' + str(index) + ('/L' if left else '/R')
    img_list = os.listdir(path)
    if refer_pic:
        img_refer = path + '/image_' + str(refer_pic).zfill(3)
    else:
        img_refer = os.path.join(path, img_list[0])
    if end_pic:
        img_list = img_list[:end_pic]
    H = [0, 0]
    for img in img_list:
        pic_index = int(img[6:9])   # 添加图片序号
        h = coordinate_diff(img_refer, img)
        H = np.row_stack((H, [pic_index, np.mean(h[0]), np.mean(h[1])]))
    # a = H[:, 1]
    np.savetxt('data/coor/coor-'+str(camera)+'-'+str(index)+'.csv', H[1:, :], fmt="%u"+2*",%.18e")


def multi_coordinate(camera, index, refer_pic=0, left=True, end_pic=0):
    """
    读取指定路径所有图片标志点的位置, 计算标志点与中心的距离, 与参考位置做差值保存为csv文件

    输入参数
    ----
    camera: 指定实验编号

    index: 实验组数

    refer_pic: 参考图片序号, 默认与第一张图片做差, 可手动选取温度30°C对应的图片

    left: 默认左相机, 定义0/False为右相机

    end_pic: 读取图片总数, 0代表读取文件夹全部图片

    输出文件
    ---
    data/multi: 坐标位置文件, Row与Column分别保存, 命名规则为'实验编号-组别(-R右相机)'
    """
    path = 'G:/point-data/' + str(camera) + '/' + str(index) + ('/L' if left else '/R')
    img_list = os.listdir(path)
    if refer_pic:
        img_refer = path + '/image_' + str(refer_pic).zfill(3)
    else:
        img_refer = os.path.join(path, img_list[0])
    if end_pic:
        img_list = img_list[:end_pic]
    R0, C0 = mark_coordinate(img_refer)
    distance = np.sqrt((np.array(R0) - 1080) ** 2 + (np.array(C0) - 2048) ** 2)
    disR = np.array(R0) - 1080
    disC = np.array(C0) - 2048
    R_list = [np.append(-3, distance), np.append(-2, disR), np.append(-1, disC)]
    C_list = [np.append(-3, distance), np.append(-2, disR), np.append(-1, disC)]
    for img in img_list:
        # pic_index = int(img[6:9])   # 添加图片序号
        pic_index = int(img[-7:-4])   # 添加图片序号
        try:
            Row, Column = mark_coordinate(os.path.join(path, img))
            R_list.append(np.append(pic_index, np.array(Row) - np.array(R0)))
            C_list.append(np.append(pic_index, np.array(Column) - np.array(C0)))
        except ValueError:
            print('读取失败')
    np.savetxt('data/multi/Row-'+str(camera)+'-'+str(index)+('.csv' if left else 'R.csv'), R_list, fmt="%u"+len(R0)*",%.18e")
    np.savetxt('data/multi/Column-'+str(camera)+'-'+str(index)+('.csv' if left else 'R.csv'), C_list, fmt="%u"+len(C0)*",%.18e")


def caltar_diff(Row, Column):
    """计算单张图片上标定板行列坐标极值差"""
    Row_diff = np.mean(Row[-11:]) - np.mean(Row[:11])
    Column_diff = np.mean(Column[10::11]) - np.mean(Column[::11])
    return Row_diff, Column_diff


def multi_cal_focus(camera, index, refer_pic=0, left=True, end_pic=0):
    """
    读取指定路径所有图片标志点的位置, 通过行列坐标极值差推算焦距变化, 与参考位置做差值保存为csv文件

    输入参数
    ----
    camera: 指定实验编号

    index: 实验组数

    refer_pic: 参考图片序号, 默认为第一张图片

    left: 默认左相机, 定义0/False为右相机

    end_pic: 读取图片总数, 0代表读取文件夹全部图片

    输出文件
    ---
    data/focus: 焦距尺寸文件, 命名规则为'实验编号-组别(-R右相机)'
    """
    path = 'G:/point-data/' + str(camera) + '/' + str(index) + ('/L' if left else '/R')
    img_list = os.listdir(path)
    if refer_pic:
        img_refer = path + '/image_' + str(refer_pic).zfill(3)
    else:
        img_refer = os.path.join(path, img_list[0])
    if end_pic:
        img_list = img_list[:end_pic]
    R0, C0 = mark_coordinate(img_refer)
    R_d0, C_d0 = caltar_diff(R0, C0)
    focus_list = []
    f0 = 0.016126
    for img in img_list:
        pic_index = int(img[6:9])   # 添加图片序号
        Row, Column = mark_coordinate(os.path.join(path, img))
        R_d, C_d = caltar_diff(Row, Column)
        focus_list.append([pic_index, f0*R_d/R_d0, f0*C_d/C_d0])
    np.savetxt('data/focus/focus-'+str(camera)+'-'+str(index)+('.csv' if left else 'R.csv'), focus_list, fmt="%u"+2*",%.18e")


if __name__ == '__main__':
    # mean_coordinate('N3', 4, 682, 1, True)
    # multi_coordinate('N3', 3, 682, 42, False)
    multi_cal_focus('N4', 2, 1, 0)
    # multi_coordinate('N3', 1, 569, 1, False)
    # multi_coordinate('B2', 9, 370, 20, True)
    # multi_coordinate('S1', 4, 380, 30, True)
    # multi_coordinate('S1', 5, 360, 10, True)
