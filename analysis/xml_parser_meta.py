#!/usr/bin/python
# -*- coding: UTF-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import re
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
                  "ratio_resoluyion": [0]*3}
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
            meta_info["ratio_resoluyion"][0] = attibute.getAttribute("value")
        elif attr_name == "latitude_delta":
            meta_info["ratio_resoluyion"][1] = attibute.getAttribute("value")
        elif attr_name == "height_delta":
            meta_info["ratio_resoluyion"][2] = attibute.getAttribute("value")
    return meta_info


# filename = r'E:/datacube_new/weekend/Datacubeweb_backend_Django/analysis/tpv.xml'
# adic = xml_to_str(filename)
# print(adic)

filename = r'E:/datacube_new/weekend/Datacubeweb_backend_Django/analysis/tpv_std.xml'
adic2 = xml_to_str_std(filename)
print(adic2)