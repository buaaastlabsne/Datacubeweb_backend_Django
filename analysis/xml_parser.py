#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom

'''
# 直接解析输出
DOMTree = xml.dom.minidom.parse("../tpv.xml")
schema = DOMTree.documentElement
if schema.hasAttribute("name"):
    print("Root element : %s" % schema.getAttribute("name"))

cubelist = schema.getElementsByTagName('Cube')
cube = cubelist[0]
if cube.hasAttribute("name"):
    print(cube.getAttribute("name"))

tablelist = cube.getElementsByTagName('Table')
table = tablelist[0]
if table.hasAttribute("name"):
    print(table.getAttribute("name"))


dimensions = schema.getElementsByTagName('Dimension')
for dimension in dimensions:
    print(dimension.getAttribute("foreignKey"))
    levels = dimension.getElementsByTagName('Level')
    for level in levels:
        print(level.getAttribute("column"))

measures = schema.getElementsByTagName('Measure')
for measure in measures:
    print(measure.getAttribute("column"))
'''


def xml_to_str(filename):
    dic = {}
    children_list = []
    DOMTree = xml.dom.minidom.parse(filename)
    schema = DOMTree.documentElement
    if schema.hasAttribute("name"):
        schema_name = schema.getAttribute("name")  # 看起来没有用到

    cubelist = schema.getElementsByTagName('Cube')
    cube = cubelist[0]
    if cube.hasAttribute("name"):
        cube_name = cube.getAttribute("name")
    dic['label'] = 'Cube-'+cube_name

    tablelist = cube.getElementsByTagName('Table')
    table = tablelist[0]
    if table.hasAttribute("name"):
        table_name = table.getAttribute("name") # 也暂时没有用到，和上面cube_name同名

    dimensions = schema.getElementsByTagName('Dimension')
    for dimension in dimensions:
        dimension_dic = {}
        dimension_dic["label"] = "Dimension-"+dimension.getAttribute("foreignKey").lower().capitalize()+"Dim"
        c_list = []
        levels = dimension.getElementsByTagName('Level')
        for level in levels:
            c_list.append({"label": 'Level-'+level.getAttribute("column").lower()})
        dimension_dic["children"] = c_list
        children_list.append(dimension_dic)

    measures = schema.getElementsByTagName('Measure')
    for measure in measures:
        children_list.append({"label": "Measure-"+measure.getAttribute("column").lower().capitalize()+"(avg)"})

    dic["children"] = children_list
    return [dic]
