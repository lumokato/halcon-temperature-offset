import numpy as np
import csv
from sklearn import linear_model


def read_param(param_file):
    regr_list = []
    with open('param/param-'+param_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            regr_list.append([float(line[1]), float(line[9]), float(line[10])])
    return regr_list


def read_tem(tem_file):
    tem_list = []
    with open('tem/tem-'+tem_file+'.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            tem_list.append(float(line[0]))
    return tem_list


# 线性回归
def lineal_param(camera_index, pic_index=1):
    param_list = read_param(camera_index)
    tem_list = read_tem(camera_index[:-1] if camera_index[-1] == 'R' else camera_index)
    length = min(len(param_list), len(tem_list))
    x = np.array(tem_list)[:length].reshape(-1, 1) - 30
    # x = np.column_stack((x, x*x))
    x = x[pic_index:]
    y = np.array(param_list)[:length]
    y0 = y[pic_index:, 0]
    y1 = y[pic_index:, 1]
    y2 = y[pic_index:, 2]
    # 训练数据
    regr0 = linear_model.LinearRegression()
    regr0.fit(x, y0)
    print(regr0.coef_, regr0.intercept_)
    print(regr0.score(x, y0))
    regr1 = linear_model.LinearRegression()
    regr1.fit(x, y1)
    print(regr1.coef_, regr1.intercept_)
    print(regr1.score(x, y1))
    regr2 = linear_model.LinearRegression()
    regr2.fit(x, y2)
    print(regr2.coef_, regr2.intercept_)
    print(regr2.score(x, y2))

    # print('coefficients(b1,b2...):', regr.coef_)
    # print('intercept(b0):', regr.intercept_)
    # xC = np.array(HC)
    # XC = xC[:, :-1]
    # YC = xC[:, -1]
    # # 训练数据
    # regrC = linear_model.LinearRegression()
    # regrC.fit(XC, YC)
    # # deltaR = regrC.coef_[0]*R1 + regrC.coef_[1]*C1 + regrC.intercept_ - dC
    # # print('coefficients(b1,b2...):', regrC.coef_)
    # # print('intercept(b0):', regrC.intercept_)
    # return np.append(np.append(regr.coef_, regr.intercept_), np.append(regrC.coef_, regrC.intercept_))


if __name__ == '__main__':
    lineal_param('N3-1R', 30)
