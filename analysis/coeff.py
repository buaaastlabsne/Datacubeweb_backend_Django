import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


# 相关分析，计算三种系数
def coeff(filename):
    data = pd.read_excel(filename, header=None)
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
# io ="E:\\datacube_new\\yzz\\Datacubeweb_backend_Django\\analysis\\ptcoeff.xls"
# r = coeff(io)


# 单因素方差分析，输入待分析文件的地址
def anova(filename):
    df = pd.read_excel(filename, header=None)
    data = df.values.T
    l =
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

