import numpy as np
import matplotlib.pyplot as plt

from sklearn import datasets, svm
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from pandas import DataFrame
import pywt
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import math


# 输入数据处理
# def ipt_process():
#     csv_data = pd.read_csv(r'F:\硕士毕设\支持向量回归预测洋流速度\T2017T-S7515S_new.csv', usecols=['speed']).values.tolist()
#     data_list = [[], [], [], [], [], [], [], [], [], []]
#     data_target = []
#     for i in range(0, 2191):
#         for j in range(0, 10):
#             data_list[j].append(csv_data[i+j][0])
#     for i in range(10, 2201):
#         data_target.append(csv_data[i][0])
#     # id = [j for j in range(2191)]
#     # 字典中的key值即为csv中列名
#     dataframe = pd.DataFrame({'t1': data_list[0], 't2': data_list[1], 't3': data_list[2], 't4': data_list[3],
#                               't5': data_list[4], 't6': data_list[5], 't7': data_list[6], 't8': data_list[7],
#                               't9': data_list[8],
#                               't10': data_list[9], 'pre': data_target})
#     # 将DataFrame存储为csv,index表示是否显示行名，default=True
#     dataframe.to_excel(r'F:\硕士毕设\支持向量回归预测洋流速度\T2017T-S7515S_new1.xlsx', index=False)
#     return csv_data


# 小波分解后的数据变换成svr模型并写入excel
def write_wave_excel(wave, file):
    data_list = [[], [], [], [], [], [], [], [], [], []]
    data_target = []
    for i in range(0, len(wave)-10):
        for j in range(0, 10):
            data_list[j].append('%.2f' % wave[i+j])
    for i in range(10, len(wave)):
        data_target.append('%.2f' % wave[i])
    dataframe = pd.DataFrame({'t1': data_list[0], 't2': data_list[1], 't3': data_list[2], 't4': data_list[3],
                                  't5': data_list[4], 't6': data_list[5], 't7': data_list[6], 't8': data_list[7],
                                  't9': data_list[8],
                                  't10': data_list[9], 'pre': data_target})
    dataframe.to_excel(file, index=False)
    return


def load_data_regression(file):
    """
    加载用于回归问题的数据集
    """
    excel_data = pd.read_excel(file).values.tolist()
    train_data = []
    train_target = []
    for i in range(len(excel_data)):
        train_data.append(excel_data[i][:10])
        train_target.append(excel_data[i][10])
    train_data_array = np.array(train_data)
    train_target_array = np.array(train_target)
    # diabetes = datasets.load_diabetes()  # 使用 scikit-learn 自带的一个糖尿病病人的数据集
    # 拆分成训练集和测试集，测试集大小为原始数据集大小的 1/4, random_state表示每次随机生成的数据一致
    # train_data = diabetes.data
    # train_target = diabetes.target
    # return excel_data
    return train_test_split(train_data, train_target, test_size=0.25, random_state=0)


# sgn符号函数
def sgn(num):
    if num > 0.0:
        return 1.0
    elif num == 0.0:
        return 0.0
    else:
        return -1.0


# 小波分解降噪与重构
def pywt_data():
    data = pd.read_csv(r'E:\datacube_new\代码和数据\T2017T-S7515S_new.csv', usecols=['speed']).values.tolist()
    data_access = []
    for i in range(len(data)):
        data_access.append(data[i][0])
    coeffs = pywt.wavedec(data_access, 'db8', level=2)
    # coeffs[0] = pywt.threshold(coeffs[0], 0.8*max(coeffs[0]), 'less', 0.8*max(coeffs[0]))
    # coeffs[1] = pywt.threshold(coeffs[1], 12, 'less', 12)
    # coeffs[1] = pywt.threshold(coeffs[1], -12, 'greater', -12)
    # coeffs[2] = pywt.threshold(coeffs[2], 12, 'less', 12)
    # coeffs[2] = pywt.threshold(coeffs[2], -12, 'greater', -12)
    # coeffs[0] = pywt.waverec([coeffs[0]], 'db8')
    # coeffs[1] = pywt.waverec([coeffs[1]], 'db8')
    # coeffs[2] = pywt.waverec([coeffs[2]], 'db8')
    # 绘制原始数据、小波分解数据
    # 去噪算法
    # 去噪后的系数项
    thcoeffs = []
    # 降噪阈值
    for i in range(1, len(coeffs)):
        tmp = coeffs[i].copy().tolist()
        Sum = 0.0
        for j in coeffs[i]:
            Sum = Sum + abs(j)
        N = len(coeffs[i])
        Sum = (1.0 / float(N)) * Sum
        sigma = (1.0 / 0.6745) * Sum
        lamda = sigma * math.sqrt(2.0 * math.log(float(N), math.e))
        for k in range(len(tmp)):
            if abs(tmp[k]) >= lamda:
                tmp[k] = sgn(tmp[k]) * (abs(tmp[k]) - 0.5 * lamda)
            else:
                tmp[k] = 0.0
        thcoeffs.append(tmp)
    recoeffs = pywt.waverec([coeffs[0], np.array(thcoeffs[0]), np.array(thcoeffs[1])], 'db8')
    plt.figure(figsize=(12, 6))
    plt.plot([i for i in range(len(data_access))], data_access, lw=0.5, color="blue", label="original")
    plt.plot([i for i in range(len(recoeffs))], recoeffs, lw=0.5, color="red", label="pywt_rec")
    plt.xlabel('Sample items')
    plt.ylabel('windspeed(m/s)')
    plt.legend()
    plt.show()
    # plt.figure(figsize=(6, 7))
    # plt.subplot(411)
    # plt.plot([i for i in range(len(data_access))], data_access, lw=0.5)
    # plt.xlabel('Sample items')
    # plt.ylabel('Original speed(m/s)')
    # plt.subplot(412)
    # plt.plot([i for i in range(len(coeffs[0]))], coeffs[0], lw=0.5)
    # plt.ylabel('Appr coeff')
    # plt.subplot(413)
    # plt.plot([i for i in range(len(coeffs[1]))], coeffs[1], lw=0.5)
    # plt.ylabel('Detail coeff1')
    # plt.subplot(414)
    # plt.plot([i for i in range(len(coeffs[2]))], coeffs[2], lw=0.5)
    # plt.ylabel('Detail coeff2')
    # plt.xlabel('Coefficient term')
    # # plt.ylabel('windspeed(m/s)')
    # plt.show()
    write_wave_excel(recoeffs.tolist(), r'E:\datacube_new\代码和数据\T2017T-S7515S_rec.xlsx')
    return data_access, coeffs[0], coeffs[1], coeffs[2]
    # 小波分解结果写入excel
    # write_wave_excel(coeffs[0], r'F:\硕士毕设\支持向量回归预测洋流速度\T2017T-S7515S_wave1.xlsx')
    # write_wave_excel(coeffs[1], r'F:\硕士毕设\支持向量回归预测洋流速度\T2017T-S7515S_wave2.xlsx')
    # write_wave_excel(coeffs[2], r'F:\硕士毕设\支持向量回归预测洋流速度\T2017T-S7515S_wave3.xlsx')

# 小波重构结果与原始对比
# def pywt_data_rec(*data):
#     wave0, wave1, wave2, original = data
#     pywtRec = pywt.waverec([wave0, wave1, wave2], 'db8')
#     plt.figure(figsize=(8, 4))
#     plt.plot([i for i in range(len(pywtRec))], pywtRec, lw=0.5, label='pywt-rec', color='red')
#     plt.plot([i for i in range(len(original))], original, lw=0.5, label='original', color='blue')
#     plt.xlabel('Sample items')
#     plt.ylabel('windspeed(m/s)')
#     plt.legend()
#     plt.show()
#     return pywtRec


# 支持向量机线性回归SVR模型, 输出预测结果
def test_LinearSVR(*data):
    X_train, X_test, y_train, y_test = data
    linear_svr = SVR(kernel="linear", max_iter=100000)
    linear_svr.fit(X_train, y_train)
    linear_svr_y_predict = linear_svr.predict(X_train)
    # print("线性核函数支持向量机的R_squared值为：", r2_score(y_test, linear_svr_y_predict))
    # print("线性核函数支持向量机的均方误差值为：", mean_squared_error(y_test, linear_svr_y_predict))
    # print("线性核函数支持向量机的均方误差值为：", mean_absolute_error(y_test, linear_svr_y_predict))
    # print('', linear_svr.score(X_test, y_test))
    poly_svr = SVR(kernel="poly")
    poly_svr.fit(X_train, y_train)
    poly_svr_y_predict = poly_svr.predict(X_test)
    # print("多项式核函数支持向量机的R_squared值为：", r2_score(y_test, poly_svr_y_predict))
    # print("多项式核函数支持向量机的均方误差值为：", mean_squared_error(y_test, poly_svr_y_predict))
    # print("线性核函数支持向量机的均方误差值为：", mean_absolute_error(y_test, poly_svr_y_predict))
    # print('', poly_svr.score(X_test, y_test))
    rbf_svr = SVR(kernel="rbf")
    rbf_svr.fit(X_train, y_train)
    rbf_svr_y_predict = rbf_svr.predict(X_test)
    # print("rbf核函数支持向量机的R_squared值为：", r2_score(y_test, rbf_svr_y_predict))
    # print("rbf核函数支持向量机的均方误差值为：", mean_squared_error(y_test, rbf_svr_y_predict))
    # print("线性核函数支持向量机的均方误差值为：", mean_absolute_error(y_test, rbf_svr_y_predict))
    # print('', rbf_svr.score(X_test, y_test))
    return linear_svr_y_predict


def test_LinearSVR_loss(*data):
    """
   测试 LinearSVR 的预测性能随不同损失函数的影响
    """
    X_train, X_test, y_train, y_test = data
    losses = ['epsilon_insensitive', 'squared_epsilon_insensitive']
    for loss in losses:
        regr = svm.LinearSVR(loss=loss, max_iter=100000)
        regr.fit(X_train, y_train)
        print("loss：%s" % loss)
        print('Coefficients:%s, intercept %s' % (regr.coef_, regr.intercept_))
        print('Score: %.2f' % regr.score(X_test, y_test))


def test_LinearSVR_epsilon(*data):
    """
    测试 LinearSVR 的预测性能随 epsilon 参数的影响
    """
    X_train, X_test, y_train, y_test = data
    epsilons = np.logspace(-2, 2)
    train_scores = []
    test_scores = []
    for epsilon in epsilons:
        # regr = svm.SVR(kernel='rbf', gamma='auto', coef0=0.0, epsilon=epsilon, C=1.0, max_iter=-1)
        regr = svm.LinearSVR(epsilon=epsilon, loss='squared_epsilon_insensitive')
        regr.fit(X_train, y_train)
        train_scores.append(regr.score(X_train, y_train))
        test_scores.append(regr.score(X_test, y_test))
    return train_scores, test_scores, epsilons
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    # ax.plot(epsilons, train_scores, label="Training score ", marker='+')
    # ax.plot(epsilons, test_scores, label=" Testing  score ", marker='o')
    # ax.set_title("LinearSVR_epsilon ")
    # ax.set_xscale("log")
    # ax.set_xlabel(r"$\epsilon$")
    # ax.set_ylabel("score")
    # ax.set_ylim(-1, 1.05)
    # ax.legend(loc="best", framealpha=0.5)
    # plt.subplot(212)
    # plt.plot([i for i in range(len(y_test))], y_test)
    # plt.plot([i for i in range(len(y_predicts[0]))], y_predicts[0])
    # plt.show()


def test_LinearSVR_C(*data):
    """
    测试 LinearSVR 的预测性能随 C 参数的影响
    """
    X_train, X_test, y_train, y_test = data
    Cs = np.logspace(-2, 2)
    train_scores = []
    test_scores = []
    for C in Cs:
        regr = svm.LinearSVR(C=C, loss='squared_epsilon_insensitive')
        regr.fit(X_train, y_train)
        train_scores.append(regr.score(X_train, y_train))
        test_scores.append(regr.score(X_test, y_test))
    return train_scores, test_scores, Cs


def plt_LinearSVR_score(*score):
    train_score1, test_score1, Epsilons, train_score2, test_score2, cs = score
    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 2, 1)
    ax.plot(Epsilons, train_score1, label="Training score", lw="0.5")
    ax.plot(Epsilons, test_score1, label=" Testing  score", lw="0.5")
    ax.set_title("LinearSVR_epsilon")
    ax.set_xscale("log")
    ax.set_xlabel(r"$\epsilon$")
    ax.set_ylabel("score")
    ax.set_ylim(-1, 1.05)
    ax.legend(loc="best", framealpha=0.5)
    ax1 = fig.add_subplot(1, 2, 2)
    ax1.plot(cs, train_score2, label="Training score", lw="0.5")
    ax1.plot(cs, test_score2, label=" Testing  score", lw="0.5")
    ax1.set_title("LinearSVR_C")
    ax1.set_xscale("log")
    ax1.set_xlabel("C")
    ax1.set_ylim(-1, 1.05)
    ax1.legend(loc="best", framealpha=0.5)
    plt.show()


def predict_result(*data):
    X_train, X_test, y_train, y_test = data
    regr = svm.LinearSVR(epsilon=4, C=3, loss='squared_epsilon_insensitive')
    regr.fit(X_train, y_train)
    y_predict = regr.predict(X_test)
    plt.figure(figsize=(8, 5))
    plt.plot([i for i in range(len(y_test))], y_test, lw=0.5, color="blue", label="speed_test")
    plt.plot([i for i in range(len(y_predict))], y_predict, lw=0.5, color="red", label="speed_predict")
    plt.xlabel('Sample items')
    plt.ylabel('windspeed(m/s)')
    plt.legend()
    plt.show()
    return y_test[0:10], y_predict[0:10].tolist()


# 小波分解降噪与重构
def pywt_data_new(address1, address2):
    data = pd.read_csv(address1, usecols=['speed']).values.tolist()
    data_access = []
    for i in range(len(data)):
        data_access.append(data[i][0])
    coeffs = pywt.wavedec(data_access, 'db8', level=2)
    thcoeffs = []
    for i in range(1, len(coeffs)):
        tmp = coeffs[i].copy().tolist()
        Sum = 0.0
        for j in coeffs[i]:
            Sum = Sum + abs(j)
        N = len(coeffs[i])
        Sum = (1.0 / float(N)) * Sum
        sigma = (1.0 / 0.6745) * Sum
        lamda = sigma * math.sqrt(2.0 * math.log(float(N), math.e))
        for k in range(len(tmp)):
            if abs(tmp[k]) >= lamda:
                tmp[k] = sgn(tmp[k]) * (abs(tmp[k]) - 0.5 * lamda)
            else:
                tmp[k] = 0.0
        thcoeffs.append(tmp)
    recoeffs = pywt.waverec([coeffs[0], np.array(thcoeffs[0]), np.array(thcoeffs[1])], 'db8')
    # write_wave_excel(recoeffs.tolist(), address2)
    return data_access, coeffs[0], coeffs[1], coeffs[2], recoeffs


def test_LinearSVR_epsilon_new(address):
    X_train, X_test, y_train, y_test = load_data_regression(address)
    epsilons = np.logspace(-2, 2)
    train_scores = []
    test_scores = []
    for epsilon in epsilons:
        regr = svm.LinearSVR(epsilon=epsilon, loss='squared_epsilon_insensitive')
        regr.fit(X_train, y_train)
        train_scores.append(regr.score(X_train, y_train))
        test_scores.append(regr.score(X_test, y_test))
    return epsilons.tolist(), train_scores, test_scores


def test_LinearSVR_C_new(address):
    X_train, X_test, y_train, y_test = load_data_regression(address)
    Cs = np.logspace(-2, 2)
    train_scores = []
    test_scores = []
    for C in Cs:
        regr = svm.LinearSVR(C=C, loss='squared_epsilon_insensitive')
        regr.fit(X_train, y_train)
        train_scores.append(regr.score(X_train, y_train))
        test_scores.append(regr.score(X_test, y_test))
    return Cs.tolist(), train_scores, test_scores
    # regr = svm.LinearSVR(C=c, loss='squared_epsilon_insensitive')
    # regr.fit(X_train, y_train)
    # train_score = regr.score(X_train, y_train)
    # test_score = regr.score(X_test, y_test)
    # return train_score, test_score


def predict_result_new(address, ep, c):
    X_train, X_test, y_train, y_test = load_data_regression(address)
    regr = svm.LinearSVR(epsilon=ep, C=c, loss='squared_epsilon_insensitive')
    regr.fit(X_train, y_train)
    y_predict = regr.predict(X_test)
    x_label = [i for i in range(len(y_test))]
    return x_label, y_test, y_predict.tolist()

