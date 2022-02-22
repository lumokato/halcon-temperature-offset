"""
相机标定
"""
import halcon as ha
import csv
import glob


def init_calib_camera(image, num_cameras=1):
    """
    初始化相机标定模型

    输入参数
    ----
    image: 任意图片路径, 用于获取图片尺寸

    num_cameras: 相机数目, 1或2

    返回值
    ---
    calib_data_id: Halcon标定模型
    """
    width, height = ha.get_image_size(image)
    caltab_descr = 'XJcaltabNew_410_235mm.cpd'
    num_calib_objects = 1
    calib_data_id = ha.create_calib_data('calibration_object', num_cameras, num_calib_objects)
    start_cam_par = (0.016, 0.0, 0.0, 0.0, 0.0, 0.0, 3.45e-6, 3.45e-6, width[0]*.5, height[0]*.5, width[0], height[0])
    ha.set_calib_data_cam_param(calib_data_id, 'all', 'area_scan_polynomial', start_cam_par)
    ha.set_calib_data_calib_object(calib_data_id, 0, caltab_descr)
    return calib_data_id


def point_change(Row, Column, regr):
    """
    像素点坐标变换

    输入参数
    ----
    Row, Column: 一组点的行列坐标

    regr: 二元线性函数参数, 1×6矩阵

    返回值
    ---
    Rowx, Columnx: 调整后的行列坐标
    """
    # regr = [1.590299564791942803e-04,1.667039812409792639e-05,-4.812939035537130983e-02,8.910823340469268292e-05,1.404109721016802317e-04,1.257129841732226527e+00]
    Rowx = []
    Columnx = []
    for i in range(len(Row)):
        Rowx.append(Row[i] + regr[0] * Row[i] + regr[1]*Column[i] + regr[2])
        Columnx.append(Column[i] + regr[3] * Row[i] + regr[4]*Column[i] + regr[5])
    return Rowx, Columnx


# 根据路径进行双目/单目标定
def calibration(regr, img_path_l, img_path_r=None):
    """
    根据路径进行双目/单目标定

    输入参数
    ----

    regr: 二元线性函数参数, 1×6矩阵

    img_path_l, img_path_r: 相机标定文件路径, img_path_r为None时进行单目标定

    返回值
    ---
    calib_data_id, error: Halcon标定模型与误差
    """
    # 获取图片像素尺寸
    file_name_l = img_path_l + 'image_01'
    image = ha.read_image(file_name_l)
    width, height = ha.get_image_size(image)
    # scale = .1
    # 读取标定板与标定图像路径
    caltab_descr = 'XJcaltabNew_410_235mm.cpd'
    # caltab_thickness = 0.001
    num_cameras = 1
    num_calib_objects = 1
    img_l = glob.glob(pathname=img_path_l + '*.png')
    if img_path_r:
        img_r = glob.glob(pathname=img_path_r + '*.png')
        num_cameras = 2
    num_poses = len(img_l)
    # 初始化标定模型
    calib_data_id = ha.create_calib_data('calibration_object', num_cameras, num_calib_objects)
    start_cam_par = (0.0125, 0.0, 0.0, 0.0, 0.0, 0.0, 3.45e-6, 3.45e-6, width[0]*.5, height[0]*.5, width[0], height[0])
    ha.set_calib_data_cam_param(calib_data_id, 'all', 'area_scan_polynomial', start_cam_par)
    ha.set_calib_data_calib_object(calib_data_id, 0, caltab_descr)
    # 标定过程
    num_ignored_img = 0
    for PoseIndex in range(num_poses):
        for CameraIndex in range(num_cameras):
            if CameraIndex == 0:
                file_name = img_l[PoseIndex]
            else:
                file_name = img_r[PoseIndex]
            image = ha.read_image(file_name)
            # 提取标志点
            try:
                ha.find_calib_object(image, calib_data_id, CameraIndex, 0, PoseIndex, [], [])
                ha.get_calib_data_observ_contours(calib_data_id, 'caltab', CameraIndex, 0, PoseIndex)
                ha.get_calib_data_observ_contours(calib_data_id, 'marks', CameraIndex, 0, PoseIndex)
                Row, Column, Index, Pose = ha.get_calib_data_observ_points(calib_data_id, CameraIndex, 0, PoseIndex)
                Rowx, Columnx = point_change(Row, Column, regr)
                ha.set_calib_data_observ_points(calib_data_id, CameraIndex, 0, PoseIndex, Rowx, Columnx, Index, Pose)
                # ha.dev_display(Caltab)
            except ha.ffi.HOperatorError:
                num_ignored_img = num_ignored_img + 1
    try:
        error = ha.calibrate_cameras(calib_data_id)
        # print(error)
        return calib_data_id, error
    except ha.ffi.HOperatorError:
        print('标定失败')


def calib_change(coeff_file):
    """
    根据相机在不同温度下拟合的像素点变化函数, 对实际的相机标定图片进行修正, 得到一组模拟标定图片，
    再对模拟标定图片进行标定, 可以认为得到的新标定模型为温度变化后的实际模型。(参考温度30°C)

    输入参数
    ----

    coeff_file: 已保存至data/coeff文件夹内的像素点变化函数文件, 如'N3-1R'代表N3实验过程第1组右相机

    输出文件
    ---
    data/param文件夹: 温度变化后的单目相机内参, 与coeff_file同名
    """
    regr_list = []
    with open('data/coeff/coeff-'+coeff_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            regr_list.append([int(line[0])]+[float(x) for x in line[1:]])
    H = []
    for i in range(len(regr_list)):
        calib_data_id, error = calibration(regr_list[i][1:], 'G:/calib-data/0121-L/0121-L7/L/')
        params = ha.get_calib_data(calib_data_id, 'camera', 0, 'params')
        params.append(error)
        print(error, i)
        H.append([regr_list[i][0]]+params)
    with open('data/param/param-'+coeff_file+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in H:
            writer.writerow(row)


if __name__ == '__main__':
    # calib_change('B2-9R')
    calib_change('N4-5')
    # calib_change('N3-4R')
    # calib_change('S1-5')
