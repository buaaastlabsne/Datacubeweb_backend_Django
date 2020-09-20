from xml.dom.minidom import Document


dataDic = {
    'theme': 'Atmosphere',
    'xmlName': 'tpv.xml',
    # 事实表
    'factList': 'TPV',
     # 维度表
    'dimList': ['time', 'longitude'],
    # 维度层级
    "time": ['2019', '2020'],
    "longitude": ['30', '118'],
# 最小分辨率
    'ratio': ['60', '0.2'],
    # 环境要素
    'measure': ["TEMPERATURE", "PRESSURE", "WIND_U", "WIND_V", "WIND_W"],
}


def xml_make(dataDic):
    doc = Document()
    schema = doc.createElement('Schema')
    schema.setAttribute('name', dataDic['factList'])
    doc.appendChild(schema)

    # 写所有纬度的名，纬度的最大最小值，维度的分辨率
    dimension = doc.createElement('DIMENSION')
    schema.appendChild(dimension)
    dimList = dataDic['dimList']
    ratio_list = dataDic['ratio']
    for i in range(len(dimList)):
        dim = doc.createElement('Dim')
        dim.setAttribute('name', dimList[i])
        dim.setAttribute('range_min', dataDic[dimList[i]][0])
        dim.setAttribute('range_max', dataDic[dimList[i]][1])
        dim.setAttribute('resolution_ratio', ratio_list[i])
        dimension.appendChild(dim)

    measureList = dataDic['measure']
    Measures = doc.createElement('Measures')
    schema.appendChild(Measures)
    for i in range(len(measureList)):
        measure = doc.createElement('Measure')
        # measure.setAttribute('column', measureList[i])
        measure.setAttribute('name', measureList[i])
        Measures.appendChild(measure)

    # Ratios = doc.createElement('ratios')
    # for i in range(len(ratio_list)):
    #     ratio = doc.createElement('ratio')
    #     ratio.setAttribute('name',ratio_list[i])
    #     Ratios.appendChild(ratio)

    xmlPath = dataDic['xmlName']
    # if dataDic['theme'] == 'Atmosphere':
    #     xmlPath = 'E:/综合自然环境数据立方库/大气环境/' + dataDic['xmlName']
    # elif dataDic['theme'] == 'Ocean':
    #     xmlPath = 'E:/综合自然环境数据立方库/海洋环境/' + dataDic['xmlName']
    # elif dataDic['theme'] == 'Land':
    #     xmlPath = 'E:/综合自然环境数据立方库/地形环境/' + dataDic['xmlName']
    # else:
    #     xmlPath = 'E:/综合自然环境数据立方库/空间环境/' + dataDic['xmlName']

    f = open(xmlPath, 'w')
    doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
    f.close()
    return


xml_make(dataDic)
