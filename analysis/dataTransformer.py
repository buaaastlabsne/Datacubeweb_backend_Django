# #coding=utf-8
# import xml.dom.minidom
# 中国 = "china"
# print(中国)
#
# xml_file_string=open('E:/datacube_new/weekend/Datacubeweb_backend_Django/analysis/tpv.xml','r').read()
# xml_file_string=xml_file_string.replace('<?xml version="1.0" encoding="GBK"?>','<?xml version="1.0" encoding="utf-8"?>')
# xml_file_string.encode('utf-8')
# # xml_file_string=unicode(xml_file_string, encoding='gbk').encode('utf-8')
#
#
# dom = xml.dom.minidom.parseString(xml_file_string)
#
# root = dom.documentElement
#
# itemlist=root.getElementsByTagName('record')
#
# item=itemlist[0]
# un=item.getAttribute('name')
# print (un)
# import re
# fileName = r'E:/datacube_new/weekend/Datacubeweb_backend_Django/analysis/tpv456_std.xml'
# name = re.search(r'([a-zA-Z0-9_]{1,100})\.(xml)$',fileName)
# print(name)
# if name:
#     print(name.group(0))
#     print(name.group(1))
#
# sett  = {1,2,3}
# for s in sett:
#     print(s)
#

#
# # time_set = {"time_start": "20110428120000", "time_delta": "900", "time_n": "9"}   # YYYY MM DD HH MM SS
# import pandas as pd
# import numpy as np
# io = r"E:\datacube_new\weekend\Datacubeweb_backend_Django\analysis\xmlCsv\海洋环境\this3.csv"
# df =pd.read_csv(io)
# df2 = df.loc[:,['AIR_TEMPERATURE', 'ATM_PRESSURE']]  # df['AIR_TEMPERATURE']
# # df2 = df2.apply(lambda x:x.astype(float))
# corr = df.corr(method='pearson')
# # 找到列名，转化为列表
# col = list(df2.columns)
# df2[col] = df2[col].apply(pd.to_numeric, errors='coerce').fillna(0.0)  # 把所有列的类型都转化为数值型，出错的地方填入NaN，再把NaN的地方补0
# df2 = pd.DataFrame(df2, dtype='float')  # 转为float
# corr2 = df2.corr(method='pearson')
# print(df2.info())
# # for row in df2.values:
# #     try:
# #         row[0] = float(row[0])
# #         row[1] = float(row[1])
# #     except:
# #         print("这是表头")
# # df2 = df2.apply(lambda x:x.astype(float))
# print(df2.info())
# print("df_shape:{}".format(df.shape))
# print("df2_shape:{}".format(df2.shape))
# print("corr:{}".format(corr))
# print("corr2:{}".format(corr2))
# print("colums:{}".format(df.columns))
# print(df2)

# 创建一个dataframe对象,B列是A列的3次幂
# a_list = np.arange(4)
# b_list = [4 * x ** 3 + 3 for x in a_list]
# df = pd.DataFrame({'A': a_list, 'B': b_list})
# print(df)
# # 模式可选值{‘pearson’, ‘kendall’, ‘spearman’}
# print(df.corr(method='pearson'))
# print(df.corr(method='spearman'))

# import datetime
# # 当前日期时间
# now=datetime.datetime.now()
# print(now)
# print(type(now))
# #<type 'datetime.datetime'>
# # strftime把时间格式化为字符串
# cur=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# print(cur)
# print(type(cur))
# #<type 'str'>
# #strptime把字符串转化为datetime
# today = datetime.datetime.strptime('20200427', '%Y%m%d')
# print(today)
# cur='2020-03-21'+' 09:30:00'
# cur_shift=datetime.datetime.strptime(cur,'%Y-%m-%d %H:%M:%S')
# print("当前班次是cur_shift:%s" %(cur_shift))      #2020-03-21 09:30:00
# next_shift=cur_shift+datetime.timedelta(days=0.5)
# print("下个班次是next_shift:%s" %(next_shift))
# next_shift1=cur_shift+datetime.timedelta(hours=12)
# print("下个班次是next_shift1:%s" %(next_shift1)) #2020-03-21 21:30:00
# next_shift2=cur_shift+datetime.timedelta(seconds=900)
# print("下个班次是next_shift2:%s" %(next_shift2)) #2020-03-21 21:30:00
#
# print("作差:{}".format(next_shift2-next_shift1))
# print("作差LX:{}".format(type(next_shift2-next_shift1)))
# print("作差:{}".format((next_shift2-next_shift1).total_seconds()))
# print("作差LX:{}".format(type(int((next_shift2-next_shift1).total_seconds()))))

import pandas as pd
import datetime
import os
"""
海流数据说明
2004/7/1 0:00－ 2004/8/1 0:00，间隔1小时 31天*24小时
水深0~600m，非等间隔；北纬15~25，间隔0.1度；东经108~120，间隔0.1度
"""
fileName = r'E:/datacube_new/weekend/Datacubeweb_backend_Django/analysis/data/海流数据/current_all.csv'
starttime = datetime.datetime.now()
#long running
# data = pd.read_csv(fileName) # 直接读取整个文件需要44秒
file_sieze=os.path.getsize(fileName)
print("file_size", file_sieze)   # 2 521 025 770 2G
chunks = pd.read_csv(fileName, iterator=True, header=None)
chunk = chunks.get_chunk(200000)
print(chunk.head())
print(chunk.index)
print(chunk.columns)
print(chunk.shape)

endtime = datetime.datetime.now()
print(endtime - starttime)

import pandas as pd


starttime = datetime.datetime.now()
chunkSize = 50000
reader = pd.read_csv(fileName, iterator=True)
# 对数据进行分块保存
loop = True
chunks = []
# while loop:
#     try:
#         # 每次读取5百万行数据
#         chunk = reader.get_chunk(chunkSize)
#         # print("分批读取数据时前10行数据是:", chunk[0:10])
#         chunks.append(chunk)
#     except StopIteration:
#         loop = False
#         print("Iteration is stopped.")
for i in range(10):
    try:
        chunk = reader.get_chunk(chunkSize)
        # print("分批读取数据时前10行数据是:", chunk[0:10])
        chunks.append(chunk)
    except StopIteration:
        print("读完了")
print("使用分块读取最后生成的list数据集是:\n", type(chunks[0]), chunks[0][0:5])
# df = pd.concat(chunks, ignore_index=True)
data_frame = pd.concat(chunks)
print("经过get_chunk函数处理的数据集", data_frame[0:5])
endtime = datetime.datetime.now()
print(endtime - starttime)