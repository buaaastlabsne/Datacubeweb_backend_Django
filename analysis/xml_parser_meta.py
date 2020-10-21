#!/usr/bin/python
# -*- coding: UTF-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import re
import datetime
# from lxml import html


def xml_to_str(filename):
    dic = {"dimensions": [], "measures": [], "resolution_ratio": []}
    DOMTree = xml.dom.minidom.parse(filename)
    schema = DOMTree.documentElement
    if schema.hasAttribute("name"):
        schema_name = schema.getAttribute("name")
        dic['name'] = schema_name

    dimensionList = schema.getElementsByTagName('Dim')
    for dim in dimensionList:
        if dim.hasAttribute("name"):
            dim_name = dim.getAttribute("name")
            dic["dimensions"].append(dim_name)
            dic[dim_name] = [dim.getAttribute("range_min"), dim.getAttribute("range_max")]
            dic["resolution_ratio"].append(dim.getAttribute("resolution_ratio"))

    measureList = schema.getElementsByTagName("Measure")
    for measure in measureList:
        if measure.hasAttribute("name"):
            measure_name = measure.getAttribute("name")
            dic["measures"].append(measure_name)

    return [dic]


def xml_to_str_std(filename):
    meta_info = { "name": "",
                  "measures": [],
                  "dimensions": ["longitude", "latitude", "height", "time"],
                  "longitude": [],
                  "latitude": [],
                  "height": [],
                  "time": [],   # 时间开始和结束的两个时刻
                  "allTimes":[],  # 所有时刻的时间的字符串
                  "ratio_resolution": [0]*4}  # 按照经、纬、高、时间的顺序存放分辨率
    print(filename)
    meta_info["name"] = re.search(r'([a-zA-Z0-9_]{1,100})\.(xml)$', filename).group(0)
    xml_file_string = open(filename).read()
    xml_file_string = xml_file_string.replace('<?xml version="1.0" encoding="GBK"?>',
                                              '<?xml version="1.0" encoding="utf-8"?>')
    xml_file_string.encode('utf-8')
    DOMTree = xml.dom.minidom.parseString(xml_file_string)
    meta_data = DOMTree.documentElement
    attibute_list = meta_data.getElementsByTagName('attribute')
    for attibute in attibute_list:
        attr_name = attibute.getAttribute("name")
        if attr_name == "eac":
            meta_info["measures"].append(re.sub("EAC_", "", attibute.getAttribute("value")))
        elif attr_name == "CHNName":
            pass
        elif attr_name == "unit":
            pass
        # 获取经纬高的范围
        elif attr_name == "longitude_min":
            meta_info["longitude"].insert(0, attibute.getAttribute("value"))
        elif attr_name == "longitude_max":
            meta_info["longitude"].append(attibute.getAttribute("value"))
        elif attr_name == "latitude_min":
            meta_info["latitude"].insert(0, attibute.getAttribute("value"))
        elif attr_name == "latitude_max":
            meta_info["latitude"].append(attibute.getAttribute("value"))
        elif attr_name == "height_min":
            meta_info["height"].insert(0, attibute.getAttribute("value"))
        elif attr_name == "height_max":
            meta_info["height"].append(attibute.getAttribute("value"))
        # 获取经纬高的分度
        elif attr_name == "longitude_delta":
            meta_info["ratio_resolution"][0] = attibute.getAttribute("value")
        elif attr_name == "latitude_delta":
            meta_info["ratio_resolution"][1] = attibute.getAttribute("value")
        elif attr_name == "height_delta":
            meta_info["ratio_resolution"][2] = attibute.getAttribute("value")
        elif attr_name == "time_delta":
            meta_info["ratio_resolution"][3] = attibute.getAttribute("value")
            time_delta = int(attibute.getAttribute("value"))
        # 获取时间的范围，首先保存时间开始，时间间隔，以及时刻的数量
        elif attr_name == "time_start":
            time_start = int(attibute.getAttribute("value"))
            # meta_info["time"].append(timeFormat(time_start).strftime("%Y-%m-%d %H:%M:%S"))
            meta_info["time"].append(time_start)
        elif attr_name == "time_n":
            time_n = int(attibute.getAttribute("value"))

    # meta_info["time"].append((timeFormat(time_start)+datetime.timedelta(seconds=(time_n-1)*time_delta)).strftime("%Y-%m-%d %H:%M:%S"))
    time_end = timeFormat(time_start)+datetime.timedelta(seconds=(time_n-1)*time_delta)
    time_end = stdTime2xmlTime(time_end)
    meta_info["time"].append(time_end)

    for i in range(time_n):
        first_time = timeFormat(time_start)
        this_time = first_time+datetime.timedelta(seconds=i*time_delta)
        time_str = this_time.strftime("%Y-%m-%d %H:%M:%S")
        meta_info["allTimes"].append(time_str)
    return meta_info


def xml_to_tree_dic(fileName):
    xml_file_string = open(fileName).read()
    xml_file_string = xml_file_string.replace('<?xml version="1.0" encoding="GBK"?>',
                                              '<?xml version="1.0" encoding="utf-8"?>')
    xml_file_string.encode('utf-8')
    DOMTree = xml.dom.minidom.parseString(xml_file_string)
    meta_data = DOMTree.documentElement
    attibute_list = meta_data.getElementsByTagName('attribute')
    tree_dic = {'label': 'meta_data',
                'children': [

                ]}
    for attibute in attibute_list:
        attr_name = attibute.getAttribute("name")
        attr_value = attibute.getAttribute("value")
        tree_dic['children'].append({'label':attr_name, 'children': [{'label': attr_value}]})
    return [tree_dic]
# filename = r'E:/datacube_new/weekend/Datacubeweb_backend_Django/analysis/tpv.xml'
# adic = xml_to_str(filename)
# print(adic)

# filename = r'E:/datacube_new/weekend/Datacubeweb_backend_Django/analysis/tpv_std.xml'
# adic2 = xml_to_str_std(filename)
# print(adic2)

# 直接读取xml原文的方法
# with open(filename, "r") as f:
#     xml_str = f.readlines()
# print("xml_str1----------------", xml_str)
# for i in range(len(xml_str)):
#     xml_str[i] = xml_str[i].replace('\n', '').replace('\t', '')
# print("xml_str1----------------", xml_str)

# 解析XML为前端树所需的字典
# tree_str = xml_to_tree_dic(filename)
# print("tree:", tree_str)


def timeFormat(time_num):
    # 输入的是XML文件中类似于20110428120000格式的数据,转换为python内置类型的时间
    YYYY = time_num//10000000000
    time_num = time_num % 10000000000

    MM = time_num//100000000
    time_num = time_num % 100000000

    DD = time_num//1000000
    time_num = time_num % 1000000

    hh = time_num // 10000
    time_num = time_num % 10000

    mm = time_num // 100
    ss = time_num % 100
    time_std = datetime.datetime(YYYY, MM, DD, hh, mm, ss)
    time_str = time_std.strftime("%Y-%m-%d %H:%M:%S")
    # print(time_str)
    # print(YYYY, MM, DD, hh, mm, ss)
    return time_std


def stdTime2xmlTime(stdTime):
    # python内置类型的时间转为XML格式的时间
    YYYY = stdTime.year
    MM = stdTime.month
    DD = stdTime.day
    hh = stdTime.hour
    mm = stdTime.minute
    ss = stdTime.second
    xmlTime = YYYY*10000000000+MM*100000000+DD*1000000+hh*10000+mm*100+ss
    return xmlTime

# timeFormat(20110428123059)
