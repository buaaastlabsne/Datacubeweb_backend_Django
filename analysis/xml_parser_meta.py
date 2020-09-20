#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

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

# filename = r'analysis/tpv.xml'
#
# adic = xml_to_str(filename)
# print(adic)