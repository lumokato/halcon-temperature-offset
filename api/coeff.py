"""
随温度变化获取线性回归参数
"""
import os
import halcon as ha
import numpy as np
from sklearn import linear_model
from .calib import init_calib_camera


def mark_coordinate(img_name):
    """
    读取指定图片标志点的位置

    输入参数
    ----
    img_name: 图片路径名称

    返回值
    ---
    Row, Column: 77个标志点的行列坐标
    """
    # file_name = img_path + '/image_' + str(serial).zfill(3)
    image = ha.read_image(img_name)
    # width, height = ha.get_image_size(image)
    calib_data_id = init_calib_camera(image)
    try:
        ha.find_calib_object(image, calib_data_id, 0, 0, 1, [], [])
        Row, Column, Index, Pose = ha.get_calib_data_observ_points(calib_data_id, 0, 0, 1)
        return Row, Column
    except ha.ffi.HOperatorError:
        print('标志点读取失败')
    # return np.array(Row)-np.array([height[0]/2]*len(Row)), np.array(Column)-np.array([width[0]/2]*len(Column))


def multi_lineal_param(img0, img1):
    """
    读取两张图片标志点的位置, 生成多元线性回归函数

    输入参数
    ----
    img0, img1: 两张图片的路径, img0为参考图片

    返回值
    ---
    np.list: 二元线性函数参数, 1×6矩阵
    """
    R0, C0 = mark_coordinate(img0)
    R1, C1 = mark_coordinate(img1)
    dR, dC = np.array(R1)-np.array(R0), np.array(C1)-np.array(C0)
    HR = []
    HC = []
    for i in range(len(R0)):
        valuesR = []
        valuesC = []
        valuesR.append(R0[i])
        valuesR.append(C0[i])
        valuesR.append(dR[i])
        valuesC.append(R0[i])
        valuesC.append(C0[i])
        valuesC.append(dC[i])
        HR.append(valuesR)
        HC.append(valuesC)
    xR = np.array(HR)
    XR = xR[:, :-1]
    YR = xR[:, -1]
    # 训练数据
    regr = linear_model.LinearRegression()
    regr.fit(XR, YR)
    # print(regr.score(XR, YR))
    # print('coefficients(b1,b2...):', regr.coef_)
    # print('intercept(b0):', regr.intercept_)
    xC = np.array(HC)
    XC = xC[:, :-1]
    YC = xC[:, -1]
    # 训练数据
    regrC = linear_model.LinearRegression()
    regrC.fit(XC, YC)
    # deltaR = regrC.coef_[0]*R0 + regrC.coef_[1]*C0 + regrC.intercept_ - dC
    # print('coefficients(b1,b2...):', regrC.coef_)
    # print('intercept(b0):', regrC.intercept_)
    return np.append(np.append(regr.coef_, regr.intercept_), np.append(regrC.coef_, regrC.intercept_))


def multiple_coeff(camera, index, refer_pic=0, left=True, end_pic=0):
    """
    读取指定路径所有图片标志点的位置, 生成多元线性回归函数, 保存csv文件

    输入参数
    ----
    camera: 指定实验编号

    index: 实验组数

    refer_pic: 参考图片序号, 手动选取温度30°C对应的图片

    left: 默认左相机, 定义0/False为右相机

    end_pic: 读取图片总数, 0代表读取文件夹全部图片

    输出文件
    ---
    data/coeff文件夹: 线性回归参数随温度变化文件, 命名规则为'实验编号-组别(-R右相机)'
    """
    path = 'G:/point-data/' + str(camera) + '/' + str(index) + ('/L' if left else '/R')
    img_list = os.listdir(path)
    if refer_pic:
        img_refer = path + '/image_' + str(refer_pic).zfill(3)
    else:
        img_refer = os.path.join(path, img_list[0])
    if end_pic:
        img_list = img_list[:end_pic]
    H = np.array([0, 0, 0, 0, 0, 0, 0])
    # H = np.array(['r1', 'r2', 'r0', 'c1', 'c2', 'c0'])
    for img in img_list:
        pic_index = int(img[6:9])   # 添加图片序号
        h = multi_lineal_param(img_refer, os.path.join(path, img))
        H = np.row_stack((H, np.append(pic_index, h)))
    np.savetxt('data/coeff/coeff-'+str(camera)+'-'+str(index)+('.csv' if left else 'R.csv'), H[1:, :], fmt="%u"+6*",%.18e")


if __name__ == '__main__':
    multiple_coeff('N4', 5, 2, 1, 4)
    # multiple_coeffR('N3', 4, 682, 1, 470)
    # multiple_coeffR('N3', 1, 569, 1, 140)
    # multiple_coeffR('B2', 9, 200, 2)
    # multiple_coeff('S1', 5, 200, 1)
