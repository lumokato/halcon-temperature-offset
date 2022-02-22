import os
import halcon as ha
import matplotlib.pyplot as plt


def ocr_image(img_path, row_1, column_1, row_2, column_2):
    """
    利用OCR识别温度显示器上的数字

    输入参数
    ----
    img: 图片路径

    row_1, column_1, row_2, column_2: OCR识别区域, 可用Halcon提取数据

    返回值
    ---
    tem_OCR: 显示器上的温度, 0代表识别失败
    """
    image = ha.read_image(img_path)
    image_invert = ha.invert_image(image)
    # ROI_0 = ha.gen_rectangle1(1210, 1451.45, 1511.3, 2019)
    # ROI_0 = ha.gen_rectangle1(1217.5, 1918.36, 1536.71, 2579.42)
    ROI_0 = ha.gen_rectangle1(row_1, column_1, row_2, column_2)
    image_reduced = ha.reduce_domain(image_invert, ROI_0)
    regions = ha.threshold(image_reduced, 0, 120)
    region_closing = ha.closing_circle(regions, 5)
    region_connected = ha.connection(region_closing)
    region_select = ha.select_shape(region_connected, 'area', 'and', 2000, 30000)
    region_sorted = ha.sort_region(region_select, 'character', 'true', 'column')
    N1 = ha.count_obj(region_sorted)
    tem_OCR = 0
    if N1 == 3:
        try:
            OCRHandle = ha.read_ocr_class_mlp('Industrial_0-9_NoRej.omc')
            Class, Confidence = ha.do_ocr_multi_class_mlp(region_sorted, image_invert, OCRHandle)
            tem_OCR = int(Class[0])*10 + int(Class[1]) + int(Class[2])/10
        except Exception:
            print('识别失败')
    elif N1 == 2:
        try:
            OCRHandle = ha.read_ocr_class_mlp('Industrial_0-9_NoRej.omc')
            Class, Confidence = ha.do_ocr_multi_class_mlp(region_sorted, image_invert, OCRHandle)
            if int(Class[0]) > 5:
                tem_OCR = int(Class[0]) + int(Class[1])/10
        except Exception:
            print('识别失败')
    return tem_OCR


def data_temperature(camera, index, row_1, column_1, row_2, column_2, end_pic=0):
    """
    读取指定路径所有图片上的温度, 保存csv文件

    输入参数
    ----
    camera: 指定实验编号

    index: 实验组数

    row_1, column_1, row_2, column_2: OCR识别区域, 可用Halcon提取数据

    end_pic: 读取图片总数, 0代表读取文件夹全部图片

    输出文件
    ---
    data/tem文件夹: 温度变化文件, 命名规则为'实验编号-组别'
    """
    path = 'G:/point-data/' + str(camera) + '/T' + str(index) + '/L'
    img_list = os.listdir(path)
    if end_pic:
        img_list = img_list[:end_pic]
    tem_list = []
    for img in img_list:
        pic_index = int(img[6:9])   # 添加图片序号
        temperature = ocr_image(os.path.join(path, img), row_1, column_1, row_2, column_2)
        tem_list.append([pic_index, temperature])
    with open('data/tem/tem-'+str(camera)+'-'+str(index)+'.csv', 'w') as csvfile:
        for tem in tem_list:
            csvfile.writelines(str(tem[0])+','+str(tem[1])+'\n')
        csvfile.close()


if __name__ == '__main__':
    data_temperature('N4', 2, 727.947, 1400.51, 1042.72, 2206.59)
    # plot_tem('N3-1')
