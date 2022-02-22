"""
读取csv文件中的数据
"""
import csv


def read_coeff(coeff_file):
    """读取线性回归参数, 返回以图片序号为键值的字典"""
    coeff_dict = {}
    with open('data/coeff/coeff-'+coeff_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            coeff_dict[int(line[0])] = [float(x) for x in line[1:]]
    return coeff_dict


def read_param(param_file):
    """读取按线性回归调整过的标定参数, 返回焦距与主点坐标"""
    param_dict = {}
    with open('data/param/param-'+param_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            param_dict[int(line[0])] = [float(line[2]), float(line[10]), float(line[11])]
    return param_dict


def read_tem(tem_file):
    """读取温度变化"""
    tem_dict = {}
    with open('data/tem/tem-'+tem_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            tem_dict[int(line[0])] = float(line[1])
    return tem_dict


def read_coor(coor_file):
    """读取标志点平均位置与参考位置的差值"""
    coor_dict = {}
    with open('data/coor/coor-'+coor_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            coor_dict[int(line[0])] = [float(x) for x in line[1:]]
    return coor_dict


def read_multi(multi_file, tem=False):
    """读取所有标志点位置与参考位置的差值, 前三行为标志点与中心点的直线距离、行列坐标距离, tem为True时读取温度修正后的数据"""
    Row_dict = {}
    with open(('data/multi_tem/Row-' if tem else 'data/multi/Row-')+multi_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            Row_dict[int(line[0])] = [float(x) for x in line[1:]]
    Column_dict = {}
    with open(('data/multi_tem/Column-' if tem else 'data/multi/Column-')+multi_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            Column_dict[int(line[0])] = [float(x) for x in line[1:]]
    return Row_dict, Column_dict


def read_focus(focus_file):
    """读取焦距变化"""
    focus_dict = {}
    with open('data/focus/focus-'+focus_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            focus_dict[int(line[0])] = [float(x) for x in line[1:]]
    return focus_dict


if __name__ == '__main__':
    a = read_tem('N3-6')
