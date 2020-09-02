import numpy as np
import pandas as pd
from skfuzzy.cluster import cmeans
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D

#
def excel2Arr():
    excel_data = pd.read_csv(r'E:\datacube_new\代码和数据\OSDO_sample_data.csv').values.tolist()
    retArr = []
    for item in excel_data:
        floatArr = ["%0.1f" % float(i) for i in item]
        floatArr = [float(i) for i in floatArr]
        retArr.append(floatArr)
    # # retArr = retArr[0:10]
    # 归一化处理
    arr = np.array(retArr).T.tolist()
    for i in range(len(arr)):
        amin, amax = min(arr[i]), max(arr[i])
        for j in range(len(arr[i])):
            arr[i][j] = (arr[i][j] - amin) / (amax - amin)
            arr[i][j] = float('%0.2f' % arr[i][j])
    return np.array(arr)


def plot_3d_scatter(data, center_list):
    fig = pl.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = [float(i) for i in data[0]]
    ys = [float(i) for i in data[1]]
    zs = [float(i) for i in data[2]]
    # xs = [1.0, 2.0]
    # ys = [1.2, 2.4]
    # zs = [1.3, 2.5]
    cs = data[3]
    ax.set_xlabel('temperature')
    ax.set_ylabel('pressure')
    ax.set_zlabel('density')
    ax.scatter(xs, ys, zs, c=cs)
    ax.scatter(center_list[0][0], center_list[0][1], center_list[0][2], marker="+", c='k')
    ax.scatter(center_list[1][0], center_list[1][1], center_list[1][2], marker="+", c='k')
    ax.scatter(center_list[2][0], center_list[2][1], center_list[2][2], marker="+", c='k')
    ax.scatter(center_list[3][0], center_list[3][1], center_list[3][2], marker="+", c='k')
    fig.show()


def bar_plot():
    xs = ['A', 'B', 'C', 'D']
    y1s = [35, 49, 44, 72]
    y2s = [38, 47, 48, 67]
    pl.figure()
    pl.ylabel('number of items', fontsize=14)
    pl.tick_params(labelsize=10)
    pl.grid(linestyle=':', axis='y')
    x = np.arange(4)
    a = pl.bar(x - 0.2, y1s, 0.4, color='dodgerblue', label='Actual', align='center')
    b = pl.bar(x + 0.2, y2s, 0.4, color='orangered', label='Classified', align='center')
    # 设置标签
    for i in a + b:
        h = i.get_height()
        pl.text(i.get_x() + i.get_width() / 2, h, '%d' % int(h), ha='center', va='bottom')
    pl.xticks(x, ['A', 'B', 'C', 'D'])
    pl.legend()
    pl.show()


def add_class_tag(arr, u_rec):
    arr_tagged = []
    arr_t = arr.T.tolist()
    u_t = u_rec.T.tolist()
    r = g = b = y = 0
    for i in range(len(arr_t)):
        amx = max(u_t[i])
        if u_t[i][0] == amx:
            arr_t[i].append('r')
            r += 1
        elif u_t[i][1] == amx:
            arr_t[i].append('g')
            g += 1
        elif u_t[i][2] == amx:
            arr_t[i].append('b')
            b += 1
        else:
            arr_t[i].append('y')
            y += 1
        arr_tagged.append(arr_t[i])
    return arr_tagged


def c_means_new(address):
    ndArr = excel2Arr(address)
    print(ndArr.shape)
    print(ndArr)
    center, u, u0, d, jm, p, fpc = cmeans(ndArr, m=2, c=4, error=0.05, maxiter=1000)
    data_tag = add_class_tag(ndArr, u)
    print(data_tag)
    return center


def bar_data():
    y1s = [35, 49, 44, 72]
    y2s = [38, 47, 48, 67]
    return y1s, y2s


def jms_data():
    jms = [16.0, 11.2, 9.2, 6.5, 4.2, 2.6, 1.8, 0.9, 0.4, 0.2]
    return jms

# c是聚类的类别
def c_means_n(address, c, m):
    ndArr = excel2Arr(address)  # (3,200)的
    center, u, u0, d, jm, p, fpc = cmeans(ndArr, m=m, c=c, error=0.05, maxiter=1000)
    print(center)
    cluster = []
    arr_t = ndArr.T.tolist()
    u_t = u.T.tolist()

    for i in range(c):
        cluster.append([["x", "y", "z"], center[i].tolist()])
    for i in range(len(arr_t)):
        sq = u_t[i].index(max(u_t[i]))
        cluster[sq].append(arr_t[i])
    return cluster


# addr = "E://datacube_new//yzz//Datacubeweb_backend_Django//analysis//OSDO_sample_data.csv"
