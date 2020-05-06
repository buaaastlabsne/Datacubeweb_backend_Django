from xml.dom.minidom import Document


dataDic = {
    'theme': 'Atmosphere',
    'xmlName': 'tpv.xml',
    # 事实表
    'factList': 'TPV',
     # 维度表
    'dimList': ['TIME', 'LONGITUDE'],
    # 维度层级
    "TIME": ["YEAR", "QUARTER", "MONTH", "XUN", "DAY", "HOUR"],
    "LONGITUDE": ["LON_10", "LON_2", "LON_1", "LON_0_2"],
    # 环境要素
    'measure': ["TEMPERATURE", "PRESSURE", "WIND_U", "WIND_V", "WIND_W"]
}


def xml_make(dataDic):
    doc = Document()
    schema = doc.createElement('Schema')
    schema.setAttribute('name', "Mondrian")
    doc.appendChild(schema)

    cube = doc.createElement('Cube')
    cube.setAttribute('name', dataDic['factList'])
    schema.appendChild(cube)

    table = doc.createElement('Table')
    table.setAttribute('name', dataDic['factList'])
    cube.appendChild(table)

    dimList = dataDic['dimList']
    for i in range(len(dimList)):
        dimenson = doc.createElement('Dimension')
        dimenson.setAttribute('foreignKey', dimList[i])
        dimenson.setAttribute('name', dimList[i].lower().capitalize()+"Dim")

        hierarchy = doc.createElement('Hierarchy')
        hierarchy.setAttribute('allMemberName', "All"+dimList[i].lower().capitalize())
        hierarchy.setAttribute('hasAll', 'true')
        hierarchy.setAttribute('primaryKey', dimList[i])

        tab = doc.createElement('Table')
        tab.setAttribute('name', dimList[i])
        hierarchy.appendChild(tab)

        levelList = dataDic[dimList[i]]
        for j in range(len(levelList)):
            level = doc.createElement('Level')
            level.setAttribute('column', levelList[j])
            level.setAttribute('name', levelList[j].lower())
            hierarchy.appendChild(level)

        dimenson.appendChild(hierarchy)
        cube.appendChild(dimenson)

    measureList = dataDic['measure']
    for i in range(len(measureList)):
        measure = doc.createElement('Measure')
        measure.setAttribute('aggregator', 'avg')
        measure.setAttribute('column', measureList[i])
        measure.setAttribute('name', measureList[i].lower())
        cube.appendChild(measure)
    xmlPath = ''
    if dataDic['theme'] == 'Atmosphere':
        xmlPath = 'D:/综合自然环境数据立方库/大气环境/' + dataDic['xmlName']
    elif dataDic['theme'] == 'Ocean':
        xmlPath = 'D:/综合自然环境数据立方库/海洋环境/' + dataDic['xmlName']
    elif dataDic['theme'] == 'Land':
        xmlPath = 'D:/综合自然环境数据立方库/地形环境/' + dataDic['xmlName']
    else:
        xmlPath = 'D:/综合自然环境数据立方库/空间环境/' + dataDic['xmlName']
    f = open(xmlPath, 'w')
    doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
    f.close()
    return


# xml_make(dataDic)
