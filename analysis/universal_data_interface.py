# 提供统一的数据文件接口
# author：yzz    2020.8.23
import pandas as pd
import numpy as np

DATASOURCE = {"TPV": r"analysis/data/TPV.csv"}
# DATASOURCE = {"TPV": r"./data/TPV.csv"}
TPV_DATATYPE = {"temperature", "pressure"}
TPV_INDEPENDENT = {"latitude", "longitude", "height"}


# 线性拟合
def line_fit(X,Y,x):
    xArray = np.array(X)
    yArray = np.array(Y)
    f1 = np.polyfit(xArray, yArray, 3)
    p1 = np.poly1d(f1)
    return p1(x)


# 最小二乘法拟合曲面
def curve_fit(X,Y,Z,x,y):
    n = len(X)
    # 求方程系数
    sigma_x = 0
    for i in X: sigma_x += i
    sigma_y = 0
    for i in Y: sigma_y += i
    sigma_z = 0
    for i in Z: sigma_z += i
    sigma_x2 = 0
    for i in X: sigma_x2 += i * i
    sigma_y2 = 0
    for i in Y: sigma_y2 += i * i
    sigma_x3 = 0
    for i in X: sigma_x3 += i * i * i
    sigma_y3 = 0
    for i in Y: sigma_y3 += i * i * i
    sigma_x4 = 0
    for i in X: sigma_x4 += i * i * i * i
    sigma_y4 = 0
    for i in Y: sigma_y4 += i * i * i * i
    sigma_x_y = 0
    for i in range(n):
        sigma_x_y += X[i] * Y[i]
    # print(sigma_xy)
    sigma_x_y2 = 0
    for i in range(n): sigma_x_y2 += X[i] * Y[i] * Y[i]
    sigma_x_y3 = 0
    for i in range(n): sigma_x_y3 += X[i] * Y[i] * Y[i] * Y[i]
    sigma_x2_y = 0
    for i in range(n): sigma_x2_y += X[i] * X[i] * Y[i]
    sigma_x2_y2 = 0
    for i in range(n): sigma_x2_y2 += X[i] * X[i] * Y[i] * Y[i]
    sigma_x3_y = 0
    for i in range(n): sigma_x3_y += X[i] * X[i] * X[i] * Y[i]
    sigma_z_x2 = 0
    for i in range(n): sigma_z_x2 += Z[i] * X[i] * X[i]
    sigma_z_y2 = 0
    for i in range(n): sigma_z_y2 += Z[i] * Y[i] * Y[i]
    sigma_z_x_y = 0
    for i in range(n): sigma_z_x_y += Z[i] * X[i] * Y[i]
    sigma_z_x = 0
    for i in range(n): sigma_z_x += Z[i] * X[i]
    sigma_z_y = 0
    for i in range(n): sigma_z_y += Z[i] * Y[i]
    # 给出对应方程的矩阵形式
    a = np.array([[sigma_x4, sigma_x3_y, sigma_x2_y2, sigma_x3, sigma_x2_y, sigma_x2],
                  [sigma_x3_y, sigma_x2_y2, sigma_x_y3, sigma_x2_y, sigma_x_y2, sigma_x_y],
                  [sigma_x2_y2, sigma_x_y3, sigma_y4, sigma_x_y2, sigma_y3, sigma_y2],
                  [sigma_x3, sigma_x2_y, sigma_x_y2, sigma_x2, sigma_x_y, sigma_x],
                  [sigma_x2_y, sigma_x_y2, sigma_y3, sigma_x_y, sigma_y2, sigma_y],
                  [sigma_x2, sigma_x_y, sigma_y2, sigma_x, sigma_y, n]])
    b = np.array([sigma_z_x2, sigma_z_x_y, sigma_z_y2, sigma_z_x, sigma_z_y, sigma_z])
    # 高斯消元解线性方程
    try:
        res = np.linalg.solve(a, b)
        z = res[0] * x * x + res[1] * x * y + res[2] * y * y + res[3] * x + res[4] * y + res[5]
    except:
        print("a:",a)
        print("b:",b)
        z = np.array(Z).mean()
    return z


# 数据统一获取接口
def get_data(Source="TPV",
             measure="temperature",
             lonMin=108, lonMax=130,
             latMin=15, latMax=25,
             heightMin = 500,heightMax= 25000,
             timeStamp=0,
             ratio_lon=1, ratio_lat=1, ratio_h=1,
             rotate=0):
    """
    :param Source: 数据源地址
    :param measure: 度量，如温度，压强
    :param lonMin: 查询最小经度范围
    :param lonMax:  查询最大经度范围
    :param latMin:  查询最小纬度范围
    :param latMax:  查询最大纬度范围
    :param heightMin:  查询最小高度范围
    :param heightMax:  查询最大高度范围
    :param timeStamp:  时间offset
    :param ratio_lon:  经度放大比率，整型
    :param ratio_lat:  纬度放大比率，整型
    :param ratio_h:  高度放大比率 整型
    :param rotate:  旋转方式 默认：0  x<->y:1  x<->z:2  y<->z:3
    :return: 查询到的数据名，数据或报错信息
    """
    if Source == "TPV":
        # 高度500~25000m，间隔500m；共50
        # 北纬15~25，间隔0.2度：51
        # 东经108~130，间隔0.2度:111  51*111 = 5661
        # 温度、压强、风速U、V、W
        # 2011/4/28 12:00－14:00 间隔15分钟:9
        print("tpv数据被载入")
        # 进行数据源，数据类型，数据范围的检验
        if lonMin<108 or lonMax>130 or latMin<15 or latMax>25 or heightMax>25000 or heightMin<500:
            print("经纬度设置超出范围，TPV地域范围：东经108~130，北纬15~25，高度500~25000m")
            return "经纬度设置超出范围，TPV地域范围：东经108~130，北纬15~25，高度500~25000m"
        if measure not in TPV_DATATYPE:
            print("数据类型选择错误，TPV数据类型为".format(TPV_DATATYPE))
            return "数据类型选择错误，TPV数据类型为".format(TPV_DATATYPE)
        # 根据经纬高载入数据
        filePath = DATASOURCE[Source]
        data = pd.read_csv(filePath)
        flag = 0
        flag1 = True
        flag2 = True
        flag3 = True
        axisName = []
        if lonMin == lonMax:
            flag+= 1
            flag1 = False
        else:
            axisName.append('longitude')

        if latMax == latMin:
            flag+=1
            flag2 =False
        else:
            axisName.append('latitude')

        if heightMax == heightMin:
            flag+= 1
            flag3 = False
        else:
            axisName.append('height')

        axisName.append(measure)
        # 柱状图和折线图
        if flag == 2:
            if lonMax!=lonMin:
                ratio = ratio_lon
            elif latMax!=latMin:
                ratio = ratio_lat
            else:
                ratio = ratio_h
            factor1 = []
            factor2 = []
            if measure == "temperature":
                dt_i = 0
            elif measure == "pressure":
                dt_i = 1
            j1 = int((lonMin - 108) / 0.2)
            j2 = int((lonMax - 108) / 0.2)
            i1 = int((latMin - 15) / 0.2)
            i2 = int((latMax - 15) / 0.2)
            k1 = int((heightMin - 500) / 500)
            k2 = int((heightMax - 500) / 500)
            print("邪门------------",j1, j2, i1, i2, k1, k2)
            for k in range(50):
                for j in range(111):
                    for i in range(51):
                        cursor = i+j*111+k*5661+timeStamp*283050
                        if i1<=i<=i2 and j1<=j<=j2 and k1<=k<=k2:
                            lines = data.iloc[cursor].tolist()[0].split()
                            factor1.append(float(lines[dt_i]))
                            if flag1:
                                factor2.append(j*0.2+108)
                            elif flag2:
                                factor2.append(i*0.2+15)
                            elif flag3:
                                factor2.append(k*500+500)
            print({"xAxisData":factor2,"yAxisData":factor1})
            xData = []
            yData = []
            if ratio < len(factor2):
                for i in range(len(factor2)//ratio):
                    xi = np.array(factor2[i*ratio:(i+1)*ratio]).mean()
                    xData.append(xi)
                    yData.append(line_fit(factor2[i*ratio:(i+1)*ratio], factor1[i*ratio:(i+1)*ratio], xi))
                # return {"axisName": axisName, "xAxisData": factor1, "yAxisData": factor2}
                if rotate == 0:
                    return {"axisName": axisName, "xAxisData": xData, "yAxisData": yData}
                elif rotate == 1:
                    axisName[0], axisName[1] = axisName[1], axisName[0]
                    return {"axisName": axisName, "xAxisData": yData, "yAxisData": xData}
                else:
                    return "旋转方式出错"
            else:
                return "分辨率设定不合适"
        else:
            if flag == 1:
                axisName = ['longitude', 'latitude', 'height', measure]
            factor1 = []
            factor2 = []
            factor3 = []
            factor4 = []
            if measure == "temperature":
                dt_i = 0
            elif measure == "pressure":
                dt_i = 1

            j1 = int((lonMin - 108) / 0.2)
            j2 = int((lonMax - 108) / 0.2)
            i1 = int((latMin - 15) / 0.2)
            i2 = int((latMax - 15) / 0.2)
            k1 = int((heightMin - 500) / 500)
            k2 = int((heightMax - 500) / 500)
            for k in range(50):
                for j in range(111):
                    for i in range(51):
                        cursor = i + j * 111 + k * 5661
                        if i1 <= i <= i2 and j1 <= j <= j2 and k1 <= k <= k2:
                            lines = data.iloc[cursor].tolist()[0].split()
                            factor1.append(float(lines[dt_i]))
                            factor2.append(i * 0.2 + 15)
                            factor3.append(j * 0.2 + 108)
                            factor4.append(k * 500 + 500)
            if ratio_h == 1 and ratio_lat == 1 and ratio_lon == 1:
                if rotate == 0:
                    return {"axisName": axisName, "xAxisData": factor2, "yAxisData": factor3, "zAxisData": factor4,
                            "data": factor1}
                elif rotate == 1:
                    axisName[0], axisName[1] = axisName[1], axisName[0]
                    return {"axisName": axisName, "xAxisData": factor3, "yAxisData": factor2, "zAxisData": factor4,
                            "data": factor1}
                elif rotate == 2:
                    axisName[0], axisName[2] = axisName[2], axisName[0]
                    return {"axisName": axisName, "xAxisData": factor4, "yAxisData": factor3, "zAxisData": factor2,
                            "data": factor1}
                elif rotate == 3:
                    axisName[2], axisName[1] = axisName[1], axisName[2]
                    return {"axisName": axisName, "xAxisData": factor2, "yAxisData": factor4, "zAxisData": factor3,
                            "data": factor1}
                else:
                    return "旋转方式出错"
            else:
                if (j2-j1+1)< ratio_lon or (i2-i1+1)<ratio_lat or (k2-k1+1)<ratio_h:
                    return "分辨率设定不合适"
                else:
                    # 先对每一个高度上进行最小二乘曲面拟合
                    lat_offset = (i2-i1+1)//ratio_lat
                    lon_offset = (j2-j1+1)//ratio_lon
                    height_offset = (k2-k1+1)//ratio_h
                    new_x_data = []  # 存纬度
                    new_y_data = []  # 存经度
                    new_z_data = []  # 存高度
                    new_v_data = []  # 存值
                    for k in range(k2-k1+1):
                        for j in range(lon_offset):
                            for i in range(lat_offset):
                                xData = []
                                yData = []
                                vData = []
                                for jj in range(ratio_lon):
                                    for ii in range(ratio_lat):
                                        # 第j层的第i个小块：ii每个小块中维度小循环的遍历 jj每个小块每层经度的遍历
                                        xData.append(factor2[ii+jj*(i2-i1+1)+i*ratio_lat+j*ratio_lon*(i2-i1+1)+k*(i2-i1+1)*(j2-j1+1)])
                                        yData.append(factor3[ii+jj*(i2-i1+1)+i*ratio_lat+j*ratio_lon*(i2-i1+1)+k*(i2-i1+1)*(j2-j1+1)])
                                        vData.append(factor1[ii+jj*(i2-i1+1)+i*ratio_lat+j*ratio_lon*(i2-i1+1)+k*(i2-i1+1)*(j2-j1+1)])
                                x_temp = np.array(xData).mean()
                                y_temp = np.array(yData).mean()
                                new_x_data.append(x_temp)
                                new_y_data.append(y_temp)
                                new_z_data.append(factor4[ii+jj*(i2-i1+1)+i*ratio_lat+j*ratio_lon*(i2-i1+1)+k*(i2-i1+1)*(j2-j1+1)])
                                new_v_data.append(curve_fit(xData, yData, vData, x_temp, y_temp))
                    print("k2-k1+1", k2 - k1 + 1)
                    print("lon_offset", lon_offset)
                    print("lat_offset", lat_offset)
                    print("***:", (k2 - k1 + 1) * lon_offset * lat_offset)
                    print("fact_len", len(new_x_data))
                    # 再对不同高度上的通过线性插值拟合
                    print("new_x_data",len(new_x_data), new_x_data)
                    print("new_y_data",len(new_y_data), new_y_data)
                    print("new_z_data",len(new_z_data), new_z_data)
                    print("new_v_data",len(new_v_data), new_v_data)
                    if ratio_h == 1:
                        if rotate == 0:
                            return {"axisName": axisName, "xAxisData": new_x_data, "yAxisData": new_y_data,
                                    "zAxisData": new_z_data, "data": new_v_data}
                        elif rotate == 1:
                            axisName[0], axisName[1] = axisName[1], axisName[0]
                            return {"axisName": axisName, "xAxisData": new_y_data, "yAxisData": new_x_data,
                                    "zAxisData": new_z_data, "data": new_v_data}
                        elif rotate == 2:
                            axisName[0], axisName[2] = axisName[2], axisName[0]
                            return {"axisName": axisName, "xAxisData": new_z_data, "yAxisData": new_y_data,
                                    "zAxisData": new_x_data, "data": new_v_data}
                        elif rotate == 3:
                            axisName[2], axisName[1] = axisName[1], axisName[2]
                            return {"axisName": axisName, "xAxisData": new_x_data, "yAxisData": new_z_data,
                                    "zAxisData": new_y_data, "data": new_v_data}
                        else:
                            return "旋转方式出错"
                    else:
                        x_final_data = []
                        y_final_data = []
                        z_final_data = []
                        v_final_data = []
                        for k in range(height_offset):
                            zData = []
                            vData = []
                            for j in range(lon_offset):
                                for i in range(lat_offset):
                                    for kk in range(ratio_h):
                                        # print("************************************************************")
                                        # print(i+j*lat_offset+k*ratio*lon_offset*lat_offset+kk*ratio*lon_offset*lat_offset)
                                        zData.append(new_z_data[i+j*lat_offset+k*ratio_h*lon_offset*lat_offset+kk*lon_offset*lat_offset])
                                        vData.append(new_v_data[i+j*lat_offset+k*ratio_h*lon_offset*lat_offset+kk*lon_offset*lat_offset])
                                    z_temp = np.array(zData).mean()
                                    z_final_data.append(z_temp)
                                    v_final_data.append(line_fit(zData, vData, z_temp))
                                    x_final_data.append(new_x_data[i+j*lat_offset+k*ratio_h*lon_offset*lat_offset])
                                    y_final_data.append(new_y_data[i+j*lat_offset+k*ratio_h*lon_offset*lat_offset])
                    print(len(x_final_data))
                    if rotate == 0:
                        return {"axisName": axisName, "xAxisData": new_x_data, "yAxisData": new_y_data,
                                "zAxisData": new_z_data, "data": new_v_data}
                    elif rotate == 1:
                        axisName[0], axisName[1] = axisName[1], axisName[0]
                        return {"axisName": axisName, "xAxisData": new_y_data, "yAxisData": new_x_data,
                                "zAxisData": new_z_data, "data": new_v_data}
                    elif rotate == 2:
                        axisName[0], axisName[2] = axisName[2], axisName[0]
                        return {"axisName": axisName, "xAxisData": new_z_data, "yAxisData": new_y_data,
                                "zAxisData": new_x_data, "data": new_v_data}
                    elif rotate == 3:
                        axisName[2], axisName[1] = axisName[1], axisName[2]
                        return {"axisName": axisName, "xAxisData": new_x_data, "yAxisData": new_z_data,
                                "zAxisData": new_y_data, "data": new_v_data}
                    else:
                        return "旋转方式出错"
    else:
        print("无效数据源，全部数据为{}".format(DATASOURCE.keys()))
        return "无效数据源，全部数据为{}".format(DATASOURCE.keys())


