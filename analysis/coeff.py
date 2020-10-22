import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


# 相关分析，计算三种系数
def coeff(filename=None, measures=None):
    if measures is None:
        print("Measures is None, calculate the first two measures in the csv file")
        # data = pd.read_excel(filename, header=None)
        data = pd.read_csv(filename)
        pearson = data.corr().iloc[0, 1]  # 计算pearson相关系数
        kendall = data.corr('kendall').iloc[0, 1]  # Kendall Tau相关系数
        spearman = data.corr('spearman').iloc[0, 1]  # spearman秩相关
        # 生成绘图的数据
        plotData = []
        for index, row in data.iterrows():
            # plotData.append({"gender": "male", "height": row[0], "weight": row[1]})
            plotData.append([row[0], row[1]])
        result = {"pearson": pearson, "kendall": kendall, "spearman": spearman, "data": plotData}
        return result
    else:
        data = pd.read_csv(filename)
        data[data > 10000000] = 0
        corr_data = data.loc[:,[measures[0], measures[1]]]
        col = list(corr_data.columns)
        corr_data[col] = corr_data[col].apply(pd.to_numeric, errors='coerce').fillna(0.0)
        pearson = corr_data.corr()  # 计算pearson相关系数
        kendall = corr_data.corr('kendall')  # Kendall Tau相关系数
        spearman = corr_data.corr('spearman')   # spearman秩相关
        plotData = []
        for i in range(len(data[measures[0]])):
            plotData.append([data[measures[0]][i], data[measures[1]][i]])
        return {"pearson": pearson[measures[0]][measures[1]], "kendall": kendall[measures[0]][measures[1]],
                "spearman": spearman[measures[0]][measures[1]], "data": plotData}

# io ="E:\\datacube_new\\yzz\\Datacubeweb_backend_Django\\analysis\\ptcoeff.xls"
# io = r"E:\datacube_new\weekend\Datacubeweb_backend_Django\analysis\xmlCsv\海洋环境\this3.csv"
# r = coeff(io, ["AIR_TEMPERATURE","ATM_PRESSURE"])
# print(r)
# 单因素方差分析，输入待分析文件的地址
def anova(filename):
    df = pd.read_excel(filename, header=None)
    df[df > 1000000] = 0
    data = df.values.T
    l = len(data)  # l个水平
    n = len(data[0])   # 每组的数据量
    N = l*n  # 总样本数
    groupSum = []  # 每组总和
    groupSqurSum = []  # 每组方差
    groupMean = []  # 每组均值
    groupSum2 = []  # 每组和的平方
    allSum2 = 0  # 每组和的平方的总和

    for i in range(l):
        groupSum.append(sum(data[i]))
        groupMean.append(np.mean(data[i]))
        # groupSqurSum.append(np.var(data[i]))
        groupSqurSum.append(sum(map(lambda x: x*x, data[i])))
        groupSum2.append(pow(sum(data[i]), 2))
        allSum2 += pow(sum(data[i]), 2)
    allSum = sum(groupSum)          # 总和
    allSqurSum2 = pow(allSum, 2)/N    # 总和的平方
    allSum2 = allSum2/n
    allSqurSum = sum(groupSqurSum)

    G1 = allSum2 - allSqurSum2
    G2 = allSqurSum - allSum2
    G3 = allSqurSum - allSqurSum2

    inDegree = l-1
    outDegree = N-l
    SSE = G2
    SSA = G1
    F = (G1 / (l - 1)) / (G2 / (N - l))
    '''
    组内自由度k-1；组间自由度n-k；样本总数
    组内离差平方和SSE；组间平方和SSA；单因素方差分析结果F
    data数据用于绘图'''
    data = data.tolist()
    result = {"inDegree": inDegree, "outDegree": outDegree, "N": N, "SSE": SSE, "SSA": SSA, "F": F, "data": data}
    return result


# io = "E:\\datacube_new\\yzz\\Datacubeweb_backend_Django\\analysis\\htAnova.xls"
# print(anova(io))

'''
# 使用stats进行单因素方差分析
io ="E:\\datacube_new\\yzz\\Datacubeweb_backend_Django\\analysis\\htAnova.xls"
df = pd.read_excel(io, header=None,names=["A", "B", "C", "D", "E"])
print(df.head())
model = ols('A ~ B', df).fit()
anovat = anova_lm(model)
print(anovat)
io2 ="E:\\datacube_new\\yzz\\Datacubeweb_backend_Django\\analysis\\htAnova2.xls"
df = pd.read_excel(io, header=None, names=["X", "Y"])
print(df.head())
model = ols('X ~ Y', df).fit()
anovat = anova_lm(model)
print(anovat)
# 使用stats多因素方差分析
formula = 'OD~ concentration + time'
formula = 'A~ B + C '
anova_results = anova_lm(ols(formula, df).fit())
print(anova_results)
'''


def anova_std(filename, measure, dimension):
    """
    :param filename: 需要进行相关分析的文件地址
    :param measure: 空气温度，大气压力等文件中包含的度量
    :param dimension: 维度：经纬高均可
    :return:
    """
    df = pd.read_csv(filename, encoding="utf-8")
    dim_levels = set()
    for element in df[dimension]:
        dim_levels.add(element)
    dim_levels = list(dim_levels)
    data_config = {}
    for dl in dim_levels:
        data_config[dl] = []
    print("选定维度的不同水平:{}：".format(dim_levels))
    for i in range(len(df[dimension])):
        data_config[df[dimension][i]].append(float(df[measure][i]))
    df = pd.DataFrame(data_config)
    data = df.values.T
    l = len(data)  # l个水平
    n = len(data[0])  # 每组的数据量
    N = l * n  # 总样本数
    groupSum = []  # 每组总和
    groupSqurSum = []  # 每组方差
    groupMean = []  # 每组均值
    groupSum2 = []  # 每组和的平方
    allSum2 = 0  # 每组和的平方的总和

    for i in range(l):
        groupSum.append(sum(data[i]))
        groupMean.append(np.mean(data[i]))
        # groupSqurSum.append(np.var(data[i]))
        groupSqurSum.append(sum(map(lambda x: x * x, data[i])))
        groupSum2.append(pow(sum(data[i]), 2))
        allSum2 += pow(sum(data[i]), 2)
    allSum = sum(groupSum)  # 总和
    allSqurSum2 = pow(allSum, 2) / N  # 总和的平方
    allSum2 = allSum2 / n
    allSqurSum = sum(groupSqurSum)

    G1 = allSum2 - allSqurSum2
    G2 = allSqurSum - allSum2
    G3 = allSqurSum - allSqurSum2

    inDegree = l - 1
    outDegree = N - l
    SSE = G2
    SSA = G1
    F = (G1 / (l - 1)) / (G2 / (N - l))
    '''
    组内自由度k-1；组间自由度n-k；样本总数
    组内离差平方和SSE；组间平方和SSA；单因素方差分析结果F
    data数据用于绘图'''
    data = data.tolist()
    result = {"inDegree": inDegree, "outDegree": outDegree, "N": N, "SSE": SSE, "SSA": SSA, "F": F, "data": data}
    return result


# io = r"E:\datacube_new\weekend\Datacubeweb_backend_Django\analysis\xmlCsv\地形环境\land2.csv"
# rs = anova_std(filename=io, measure="AIR_TEMPERATURE", dimension="LATITUDE")


