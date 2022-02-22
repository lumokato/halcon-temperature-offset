from calib import calibration
from read_csv import read_tem, read_multi
import halcon as ha
from coeff import mark_coordinate
import numpy as np
import os


def param_change(index):
    """生成按温度变化的相机参数"""
    param_dict = {}
    calib_data_id, error = calibration([0, 0, 0, 0, 0, 0], 'G:/calib-data/0121-L/0121-L7/L/')
    param = ha.get_calib_data(calib_data_id, 'camera', 0, 'params')
    tem_data = read_tem(index)
    for index in tem_data.keys():
        paramT = param[:]
        paramT[1] = param[1] + 1.8e-07 * (tem_data[index] - 30)
        # paramT[9] = param[9] + 0.15499104 * (tem - 30)
        # paramT[10] = param[10] + 0.05490013 * (tem - 30)
        # paramT[1] = param[1] + 1.54858967e-07 * (tem - 30)
        # paramT[9] = param[9] + -0.0305621 * (tem - 30)
        # paramT[10] = param[10] + 0.06692445 * (tem - 30)
        param_dict[index] = paramT
    return param_dict


def tem_coordinate(camera, index, refer_pic=0, left=True, end_pic=0):
    """
    读取指定路径所有图片标志点的位置, 计算标志点与中心的距离, 利用温度修正后与参考位置做差值保存为csv文件

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
    param_data = param_change(str(camera) + '-' + str(index))
    disR = np.array(R0) - 1080
    disC = np.array(C0) - 2048
    R_list = [np.append(-3, distance), np.append(-2, disR), np.append(-1, disC)]
    C_list = [np.append(-3, distance), np.append(-2, disR), np.append(-1, disC)]
    for img in img_list:
        pic_index = int(img[6:9])   # 添加图片序号
        if pic_index in param_data.keys():
            Row, Column = mark_coordinate(os.path.join(path, img))
            pose = [0, 0, 1.7, 0, 0, 180, 0]
            world_x, world_y = ha.image_points_to_world_plane(param_data[pic_index], pose, Row, Column, 'm')
            cam0_hom_wcs = ha.pose_to_hom_mat3d(pose)
            world_z = [0] * len(world_x)
            x, y, z = ha.affine_trans_point_3d(cam0_hom_wcs, world_x, world_y, world_z)
            img_x, img_y = ha.project_3d_point(x, y, z, param_data[refer_pic+1])
            R_list.append(np.append(pic_index, np.array(img_x) - np.array(R0)))
            C_list.append(np.append(pic_index, np.array(img_y) - np.array(C0)))
    np.savetxt('data/multi_tem/Row-'+str(camera)+'-'+str(index)+('.csv' if left else 'R.csv'), R_list, fmt="%u"+77*",%.18e")
    np.savetxt('data/multi_tem/Column-'+str(camera)+'-'+str(index)+('.csv' if left else 'R.csv'), C_list, fmt="%u"+77*",%.18e")

    return False


if __name__ == '__main__':
    # a = param_change('N4-5')
    # tem_coordinate('N3', 3, 569, 43, True)
    tem_coordinate('N4', 2)
    # tem_coordinate('N3', 4, 682, 30, False)
