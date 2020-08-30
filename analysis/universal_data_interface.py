# 提供统一的数据文件接口
# author：yzz    2020.8.23
import pandas as pd

DATASOURCE = {"TPV": r"analysis/data/TPV.csv"}
# DATASOURCE = {"TPV": r"./data/TPV.csv"}
TPV_DATATYPE = {"temperature", "pressure"}
TPV_INDEPENDENT = {"latitude", "longitude", "height"}

def get_data(Source="TPV",
             measure="temperature",
             lonMin=108,lonMax=130,
             latMin=15,latMax=25,
             heightMin = 500,heightMax= 25000,
             timeStamp=0):
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
            print("邪门------------",j1,j2,i1,i2,k1,k2)
            for k in range(50):
                for j in range(111):
                    for i in range(51):
                        cursor = i+j*111+k*5661
                        if i1<=i<=i2 and j1<=j<=j2 and k1<=k<=k2:
                            lines = data.iloc[cursor].tolist()[0].split()
                            factor1.append(lines[dt_i])
                            if flag1:
                                factor2.append(j*0.2+108)
                            elif flag2:
                                factor2.append(i*0.2+15)
                            elif flag3:
                                factor2.append(k*500+500)
            print({"xAxisData":factor1,"yAxisData":factor2})
            return {"axisName": axisName, "xAxisData":factor1,"yAxisData":factor2}
        else:
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
                            factor1.append(lines[dt_i])
                            factor2.append(i * 0.2 + 15)
                            factor3.append(j * 0.2 + 108)
                            factor4.append(k * 500 + 500)

            return {"axisName": axisName, "xAxisData": factor2, "yAxisData": factor3, "zAxisData": factor4, "data":factor1}
    else:
        print("无效数据源，全部数据为{}".format(DATASOURCE.keys()))
        return "无效数据源，全部数据为{}".format(DATASOURCE.keys())


# data = get_data(Source="TPV", measure="temperature",
#             lonMin=120, lonMax=120,
#              latMin=15, latMax=15,
#              heightMin=500,heightMax=25000,)
# print(data)



