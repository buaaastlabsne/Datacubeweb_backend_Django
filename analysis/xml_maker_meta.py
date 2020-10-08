from xml.dom.minidom import Document
import pandas as pd
import re

DATASOURCE = {"TPV": r"analysis/data/TPV.csv"}  # 保存相应文件的地址

dataDic = {
    'theme': 'Atmosphere',
    'xmlName': 'tpv.xml',
    'factList': 'TPV',  # 事实表
    'dimList': ['longitude','latitude','height'],   # 维度表
    # "time": ['2019', '2020'],  # 维度层级
    "longitude": ['108', '130'],
    "latitude":["15","25"],
    "height":["500","25000"],
    'ratio': ['0.2', '0.2','500'],  # 最小分辨率
    'measure': ["TEMPERATURE", "PRESSURE"],  # 环境要素
}
config_dic_default = {
    "xmlName": 'tpv_std.xml',
    "model": "grid",
    "format": "csv",
    "ecc": "ECC_ATMOSPHERE_PROPERTY_SET",
    "measures": [
        {"eac": "EAC_ATM_PRESSURE", "CHNName": "大气压强", "unit": "hPa"},
        {"eac": "EAC_AIR_TEMPERATURE", "CHNName": "大气温度", "unit": "℃"},
        {"eac": "EAC_WIND_SPEED_U", "CHNName": "经向风速", "unit": "m/s"},
        {"eac": "EAC_WIND_SPEED_V", "CHNName": "纬向风速", "unit": "m/s"},
        {"eac": "EAC_WIND_SPEED_W", "CHNName": "垂直风速", "unit": "m/s"},
    ],
    "data_type": "double",
    "range": [
        {"time_start": "20110428120000", "time_delta": "900", "time_n": "9"},
        {"longitude_min": "114.014400", "longitude_max": "116.863300", "longitude_delta": "0.2"},
        {"latitude_min": "18.047620", "latitude_max": "19.952380", "latitude_delta": "0.2"},
        # {"heights": "106.655  154.066  204.447  257.986  ","height_n": "4"},
        {"height_max": "25000", "height_min": "500", "height_delta": "500"}
    ]
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


def xml_make_std(config_dic=None, write_csv=False):
    if config_dic == None:
        config_dic = config_dic_default
    doc = Document()
    meta_data = doc.createElement('metadata')
    doc.appendChild(meta_data)

    # 写基本信息
    add_attribute(doc, meta_data, "model", config_dic["model"])
    add_attribute(doc, meta_data, "format", config_dic["format"])
    add_attribute(doc, meta_data, "ecc", config_dic["ecc"])
    # 写度量信息
    for element in config_dic["measures"]:
        for k, v in element.items():
            add_attribute(doc, meta_data, k, v)
    # 写数据类型信息
    add_attribute(doc, meta_data, "data_type", config_dic["data_type"])
    # 写数据范围信息
    for element in config_dic["range"]:
        for k, v in element.items():
            add_attribute(doc, meta_data, k, v)

    xmlPath = r"analysis/xml&csv/"+config_dic['xmlName']
    f = open(xmlPath, 'w')
    doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='GBK')
    f.close()

    if write_csv:
        # csvName是与本次生成的xml的同名的csv文件的名字，将要写入的是根据前端需求生成的数据
        csvName = r"analysis/xml&csv/"+re.sub(".xml", "", str(config_dic["xmlName"]))+".csv"
        print("csv name:",csvName)
        # 此处读取的是完整的数据文件，这里暂时写死为TPV，
        data = pd.read_csv(DATASOURCE["TPV"])

        lonMax = float(config_dic["range"][1]["longitude_max"])
        lonMin = float(config_dic["range"][1]["longitude_min"])
        lonDelta = float(config_dic["range"][1]["longitude_delta"])
        latMax = float(config_dic["range"][2]["latitude_max"])
        latMin = float(config_dic["range"][2]["latitude_min"])
        latDelta = float(config_dic["range"][2]["latitude_delta"])
        heightMax = float(config_dic["range"][3]["height_max"])
        heightMin = float(config_dic["range"][3]["height_min"])
        heightDelta = float(config_dic["range"][3]["height_delta"])

        j1 = int((lonMin - 108) / 0.2)
        j2 = int((lonMax - 108) / 0.2)
        i1 = int((latMin - 15) / 0.2)
        i2 = int((latMax - 15) / 0.2)
        k1 = int((heightMin - 500) / 500)
        k2 = int((heightMax - 500) / 500)

        measure_serial = set()
        for measure in config_dic["measures"]:
            if "PRESSURE" in measure["eac"]:
                measure_serial.add(0)
            if "TEMPERATURE" in measure["eac"]:
                measure_serial.add(1)
            if "PRESSURE" in measure["eac"]:
                measure_serial.add(2)
            if "PRESSURE" in measure["eac"]:
                measure_serial.add(3)
            if "PRESSURE" in measure["eac"]:
                measure_serial.add(4)
        measure_serial = list(measure_serial)
        measure_serial.sort()

        k_dt = 0
        j_dt = 0
        i_dt = 0
        for k in range(50):
            j_dt = 0
            i_dt = 0
            for j in range(111):
                i_dt = 0
                for i in range(51):
                    write_flag = False
                    cursor = i + j * 111 + k * 5661     # + timeStamp * 283050
                    if cursor == i_dt*latDelta+j_dt*111*lonDelta+k_dt*5661*heightDelta:
                        write_flag = True
                    elif cursor == (i_dt+1)*latDelta+j_dt*111*lonDelta+k_dt*5661*heightDelta:
                        write_flag =True
                        i_dt += 1
                    elif cursor == i_dt*latDelta+(j_dt+1)*111*lonDelta+k_dt*5661*heightDelta:
                        write_flag =True
                        j_dt += 1
                    elif cursor == i_dt*latDelta+j_dt*111*lonDelta+(k_dt+1)*5661*heightDelta:
                        write_flag =True
                        k_dt += 1

                    if i1 <= i <= i2 and j1 <= j <= j2 and k1 <= k <= k2 and write_flag:
                        lines = data.iloc[cursor].tolist()[0].split()
                        line_to_write = ""
                        for m in measure_serial:
                            line_to_write += (lines[m]+",")
                        line_to_write += "\n"
                        with open(csvName, 'a') as f:
                            f.writelines(line_to_write)
    return


def add_attribute(doc, father_node, child_name, child_value):
    child_node = doc.createElement("attribute")
    child_node.setAttribute("name", child_name)
    child_node.setAttribute("value", child_value)
    father_node.appendChild(child_node)


# xml_make(dataDic)
# xml_make_std(config_dic=config_dic_default)