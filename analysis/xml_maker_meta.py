from xml.dom.minidom import Document
from xml.dom.minidom import parse
import xml.dom.minidom
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
    'measure': ["AIR_TEMPERATURE", "ATM_PRESSURE"],  # 环境要素
}
config_dic_default = {
    'theme': 'Atmosphere',
    "factList": "TPV",
    "xmlName": 'tpv_std_1.xml',  # 想要保存的xml与csv文件的名字
    "model": "grid",
    "format": "csv",
    "ecc": "ECC_ATMOSPHERE_PROPERTY_SET",
    "measures": [
        {"eac": "EAC_AIR_TEMPERATURE", "CHNName": "大气温度", "unit": "℃"},
        {"eac": "EAC_ATM_PRESSURE", "CHNName": "大气压强", "unit": "hPa"},
        {"eac": "EAC_WIND_SPEED_U", "CHNName": "经向风速", "unit": "m/s"},
        {"eac": "EAC_WIND_SPEED_V", "CHNName": "纬向风速", "unit": "m/s"},
        {"eac": "EAC_WIND_SPEED_W", "CHNName": "垂直风速", "unit": "m/s"},
    ],
    "data_type": "double",
    "range": [
        {"time_start": "20110428120000", "time_delta": "900", "time_n": "9"},
        {"longitude_min": "108", "longitude_max": "130", "longitude_delta": "0.2"},
        {"latitude_min": "15", "latitude_max": "25", "latitude_delta": "0.2"},
        # {"heights": "106.655  154.066  204.447  257.986  ","height_n": "4"},
        {"height_max": "25000", "height_min": "500", "height_delta": "500"}
    ]
}


def add_attribute(doc, father_node, child_name, child_value):
    """
    :param doc:
    :param father_node:
    :param child_name:
    :param child_value:
    :return:
    """
    child_node = doc.createElement("attribute")
    child_node.setAttribute("name", child_name)
    child_node.setAttribute("value", child_value)
    father_node.appendChild(child_node)


def xml_make(dataDic):
    # 解析最初格式的XML
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


def xml_make_std_lat_lon(config_dic=None, write_csv=False):
    if config_dic is None:
        config_dic = config_dic_default
    # 根据数据源中factlist(事实表)选取数据源；首先读取数据源同名的XML文件的元数据信息
    meta_xml_path = re.sub(".csv", ".xml", DATASOURCE[config_dic["factList"]])
    xml_meta = open(meta_xml_path).read()
    xml_meta = xml_meta.replace('<?xml version="1.0" encoding="GBK"?>',
                                              '<?xml version="1.0" encoding="utf-8"?>')
    xml_meta.encode('utf-8')
    DOMTree_meta = xml.dom.minidom.parseString(xml_meta)
    meta_dt = DOMTree_meta.documentElement
    attibute_list = meta_dt.getElementsByTagName('attribute')
    # headerList列表用于存放从元数据XML中读取到的表头信息（也就是度量）,
    # 元数据XML中表头信息必须与数据文件中不同度量出现的顺序一一对应，因为这关系到后续的写文件
    headerList = []
    for attibute in attibute_list:
        attr_name = attibute.getAttribute("name")
        # 获取经纬高的范围
        if attr_name == "longitude_min":
            longitude_meta_min = float(attibute.getAttribute("value"))
        elif attr_name == "longitude_max":
            longitude_meta_max = float(attibute.getAttribute("value"))
        elif attr_name == "latitude_min":
            latitude_meta_min = float(attibute.getAttribute("value"))
        elif attr_name == "latitude_max":
            latitude_meta_max = float(attibute.getAttribute("value"))
        elif attr_name == "height_min":
            height_meta_min = float(attibute.getAttribute("value"))
        elif attr_name == "height_max":
            height_meta_max = float(attibute.getAttribute("value"))
        # 获取经纬高的分度
        elif attr_name == "longitude_delta":
            longitude_meta_delta = float(attibute.getAttribute("value"))
        elif attr_name == "latitude_delta":
            latitude_meta_delta = float(attibute.getAttribute("value"))
        elif attr_name == "height_delta":
            height_meta_delta = float(attibute.getAttribute("value"))
        elif attr_name == "eac":
            headerList.append(re.sub("EAC_", "", attibute.getAttribute("value")))

    # 根据主题选择csv文件与XML文件所保存的位置
    if config_dic['theme'] == 'Atmosphere':
        xmlFolder = '大气环境'
    elif config_dic['theme'] == 'Ocean':
        xmlFolder = '海洋环境'
    elif config_dic['theme'] == 'Land':
        xmlFolder = '地形环境'
    else:
        xmlFolder = '空间环境'

    # 根据前端查询需求生成的标准格式XML
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

    xmlPath = r"analysis/xmlCsv/"+xmlFolder+'/'+config_dic['xmlName']
    # xmlPath = r"E:/datacube_new/weekend/Datacubeweb_backend_Django/analysis/data/"+ r'/' + config_dic['xmlName']
    f = open(xmlPath, 'w')
    doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='GBK')
    f.close()

    # 如果有需求，则生成与查询的XML对应的csv数据文件信息
    if write_csv:
        # csvName是与本次生成的xml的同名的csv文件的名字，将要写入的是根据前端需求生成的数据
        csvName = r"analysis/xmlCsv/" + xmlFolder + '/'+re.sub(".xml", "", str(config_dic["xmlName"]))+".csv"
        # 此处根据事实表读取对应数据文件的位置
        data = pd.read_csv(DATASOURCE[config_dic["factList"]], header=None)

        lonMax = float(config_dic["range"][1]["longitude_max"])
        lonMin = float(config_dic["range"][1]["longitude_min"])
        lonDelta = float(config_dic["range"][1]["longitude_delta"])
        latMax = float(config_dic["range"][2]["latitude_max"])
        latMin = float(config_dic["range"][2]["latitude_min"])
        latDelta = float(config_dic["range"][2]["latitude_delta"])
        heightMax = float(config_dic["range"][3]["height_max"])
        heightMin = float(config_dic["range"][3]["height_min"])
        heightDelta = float(config_dic["range"][3]["height_delta"])

        j1 = int((lonMin - longitude_meta_min) / longitude_meta_delta)
        j2 = int((lonMax - longitude_meta_min) / longitude_meta_delta)
        i1 = int((latMin - latitude_meta_min) / latitude_meta_delta)
        i2 = int((latMax - latitude_meta_min) / latitude_meta_delta)
        k1 = int((heightMin - height_meta_min)/ height_meta_delta)
        k2 = int((heightMax - height_meta_min) / height_meta_delta)
        print("j1:{},j2:{},i1:{},i2:{},k1:{},k2:{}".format(j1, j2, i1, i2, k1, k2))
        measure_serial = set()
        header_num =len(headerList)
        for measure in config_dic["measures"]:
            for i in range(header_num):
                if headerList[i] in measure["eac"]:
                    measure_serial.add(i)
        measure_serial = list(measure_serial)
        measure_serial.sort()

        with open(csvName, 'w') as f:
            csvHeader = ""
            # allHeaders = ["AIR_TEMPERATURE", "ATM_PRESSURE",  "WIND_SPEED_U", "WIND_SPEED_V", "WIND_SPEED_W"]
            for m in measure_serial:
                csvHeader += (headerList[m] + ",")  # csvHeader += (allHeaders[m] + ",")
            csvHeader += "LATITUDE,LONGITUDE,HEIGHT"
            csvHeader += "\n"
            f.writelines(csvHeader)

        k_dt = 0
        height_n = int((height_meta_max-height_meta_min)/height_meta_delta+1)
        longitude_n = int((longitude_meta_max-longitude_meta_min)/longitude_meta_delta+1)
        latitude_n = int((latitude_meta_max-latitude_meta_min)/latitude_meta_delta+1)

        for k in range(height_n):
            j_dt = 0
            for j in range(longitude_n):
                i_dt = 0
                for i in range(latitude_n):
                    write_flag = False
                    cursor = i + j * longitude_n + k * latitude_n*longitude_n
                    if cursor == i_dt*(latDelta/latitude_meta_delta)+j_dt*longitude_n*(lonDelta/longitude_n) + \
                            k_dt*longitude_n*latitude_n*(heightDelta/height_meta_delta):
                        write_flag = True
                    elif cursor == (i_dt+1)*(latDelta/latitude_meta_delta)+j_dt*longitude_n\
                            *(lonDelta/longitude_meta_delta)+k_dt*longitude_n*latitude_n*(heightDelta/height_meta_delta):
                        write_flag = True
                        i_dt += 1
                    elif cursor == i_dt*(latDelta/latitude_meta_delta)+(j_dt+1)*longitude_n*\
                            (lonDelta/longitude_meta_delta)+k_dt*longitude_n*latitude_n*(heightDelta/height_meta_delta):
                        write_flag = True
                        j_dt += 1
                    elif cursor == i_dt*(latDelta/latitude_meta_delta)+j_dt*longitude_n*(lonDelta/longitude_meta_delta)\
                            +(k_dt+1)*longitude_n*latitude_n*(heightDelta/height_meta_delta):
                        write_flag = True
                        k_dt += 1

                    if i1 <= i <= i2 and j1 <= j <= j2 and k1 <= k <= k2 and write_flag:
                        lines = data.iloc[cursor].tolist()[0].split()
                        line_to_write = ""
                        for m in measure_serial:
                            line_to_write += (lines[m]+",")
                        line_to_write += str(i*latitude_meta_delta+latitude_meta_min)+","\
                                         +str(i*longitude_meta_delta+longitude_meta_min)+","\
                                         +str(k*height_meta_delta+height_meta_min)
                        line_to_write += "\n"
                        print("lines_to_write:{}".format(line_to_write))
                        with open(csvName, 'a') as f:
                            f.writelines(line_to_write)
    return


def xml_make_std(config_dic=None, write_csv=False):
    if config_dic is None:
        config_dic = config_dic_default
    # 根据数据源中factlist(事实表)选取数据源；首先读取数据源同名的XML文件的元数据信息
    meta_xml_path = re.sub(".csv", ".xml", DATASOURCE[config_dic["factList"]])
    xml_meta = open(meta_xml_path).read()
    xml_meta = xml_meta.replace('<?xml version="1.0" encoding="GBK"?>',
                                              '<?xml version="1.0" encoding="utf-8"?>')
    xml_meta.encode('utf-8')
    DOMTree_meta = xml.dom.minidom.parseString(xml_meta)
    meta_dt = DOMTree_meta.documentElement
    attibute_list = meta_dt.getElementsByTagName('attribute')
    # headerList列表用于存放从元数据XML中读取到的表头信息（也就是度量）,
    # 元数据XML中表头信息必须与数据文件中不同度量出现的顺序一一对应，因为这关系到后续的写文件
    headerList = []
    for attibute in attibute_list:
        attr_name = attibute.getAttribute("name")
        # 获取经纬高的范围
        if attr_name == "longitude_min":
            longitude_meta_min = float(attibute.getAttribute("value"))
        elif attr_name == "longitude_max":
            longitude_meta_max = float(attibute.getAttribute("value"))
        elif attr_name == "latitude_min":
            latitude_meta_min = float(attibute.getAttribute("value"))
        elif attr_name == "latitude_max":
            latitude_meta_max = float(attibute.getAttribute("value"))
        elif attr_name == "height_min":
            height_meta_min = float(attibute.getAttribute("value"))
        elif attr_name == "height_max":
            height_meta_max = float(attibute.getAttribute("value"))
        # 获取经纬高的分度
        elif attr_name == "longitude_delta":
            longitude_meta_delta = float(attibute.getAttribute("value"))
        elif attr_name == "latitude_delta":
            latitude_meta_delta = float(attibute.getAttribute("value"))
        elif attr_name == "height_delta":
            height_meta_delta = float(attibute.getAttribute("value"))
        elif attr_name == "eac":
            headerList.append(re.sub("EAC_", "", attibute.getAttribute("value")))

    # 根据主题选择csv文件与XML文件所保存的位置
    if config_dic['theme'] == 'Atmosphere':
        xmlFolder = '大气环境'
    elif config_dic['theme'] == 'Ocean':
        xmlFolder = '海洋环境'
    elif config_dic['theme'] == 'Land':
        xmlFolder = '地形环境'
    else:
        xmlFolder = '空间环境'

    # 根据前端查询需求生成的标准格式XML
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

    xmlPath = r"analysis/xmlCsv/"+xmlFolder+'/'+config_dic['xmlName']
    # xmlPath = r"E:/datacube_new/weekend/Datacubeweb_backend_Django/analysis/data/"+ r'/' + config_dic['xmlName']
    f = open(xmlPath, 'w')
    doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='GBK')
    f.close()

    # 如果有需求，则生成与查询的XML对应的csv数据文件信息
    if write_csv:
        # csvName是与本次生成的xml的同名的csv文件的名字，将要写入的是根据前端需求生成的数据
        csvName = r"analysis/xmlCsv/" + xmlFolder + '/'+re.sub(".xml", "", str(config_dic["xmlName"]))+".csv"
        # 此处根据事实表读取对应数据文件的位置
        data = pd.read_csv(DATASOURCE[config_dic["factList"]], header=None)

        lonMax = float(config_dic["range"][1]["longitude_max"])
        lonMin = float(config_dic["range"][1]["longitude_min"])
        lonDelta = float(config_dic["range"][1]["longitude_delta"])
        latMax = float(config_dic["range"][2]["latitude_max"])
        latMin = float(config_dic["range"][2]["latitude_min"])
        latDelta = float(config_dic["range"][2]["latitude_delta"])
        heightMax = float(config_dic["range"][3]["height_max"])
        heightMin = float(config_dic["range"][3]["height_min"])
        heightDelta = float(config_dic["range"][3]["height_delta"])

        i1 = int(round(float(format((lonMin - longitude_meta_min) / longitude_meta_delta, ".8f"))))
        i2 = int(round(float(format((lonMax - longitude_meta_min) / longitude_meta_delta, ".8f"))))
        j1 = int(round(float(format((latMin - latitude_meta_min) / latitude_meta_delta, ".8f"))))
        j2 = int(round(float(format((latMax - latitude_meta_min) / latitude_meta_delta, ".8f"))))
        k1 = int(round(float(format((heightMin - height_meta_min) / height_meta_delta, ".8f"))))
        k2 = int(round(float(format((heightMax - height_meta_min) / height_meta_delta, ".8f"))))

        measure_serial = set()
        header_num =len(headerList)
        for measure in config_dic["measures"]:
            for i in range(header_num):
                if headerList[i] in measure["eac"]:
                    measure_serial.add(i)
        measure_serial = list(measure_serial)
        measure_serial.sort()

        with open(csvName, 'w') as f:
            csvHeader = "HEIGHT,LATITUDE,LONGITUDE,"
            for m in measure_serial:
                csvHeader += (headerList[m] + ",")  # csvHeader += (allHeaders[m] + ",")
            csvHeader += "\n"
            f.writelines(csvHeader)
        # 对于数据集而言的经纬高的数据量
        height_n = int((height_meta_max-height_meta_min)/height_meta_delta+1)
        longitude_n = int((longitude_meta_max-longitude_meta_min)/longitude_meta_delta+1)
        latitude_n = int((latitude_meta_max-latitude_meta_min)/latitude_meta_delta+1)
        # 对于某次查询而言的经纬高的数据量
        height_num = int((heightMax-heightMin)//heightDelta)+1
        longitude_num = int((lonMax-lonMin)/lonDelta)+1
        latitude_num = int((latMax-latMin)/latDelta)+1
        print("height_num:{} lat_num:{} lon_num:{}_".format(height_num,latitude_num, longitude_num))
        tail_h = int(round(float(format((heightMin - height_meta_min) % heightDelta, ".8f")) / height_meta_delta))
        tail_lon = int(round(float(format((lonMin - longitude_meta_min) % lonDelta, ".8f")) / longitude_meta_delta))
        tail_lat = int(round(float(format((latMin - latitude_meta_min) % latDelta, ".8f")) / latitude_meta_delta))
        ratio_h = heightDelta/height_meta_delta
        ratio_lon = lonDelta/longitude_meta_delta
        ratio_lat = latDelta/latitude_meta_delta

        for k in range(height_num):
            for j in range(latitude_num):
                for i in range(longitude_num):
                    cursor = (i*ratio_lon+tail_lon) + (j*ratio_lat+tail_lat)*longitude_n \
                             + (k*ratio_h+tail_h)*latitude_n*longitude_n

                    lines = data.iloc[int(cursor)].tolist()[0].split()
                    line_to_write = str((k*ratio_h+tail_h)*height_meta_delta+height_meta_min)+","\
                                    + str((j*ratio_lat+tail_lat)*latitude_meta_delta+latitude_meta_min)+","\
                                    + str((i*ratio_lon+tail_lon)*longitude_meta_delta+longitude_meta_min)+","
                    for m in measure_serial:
                        line_to_write += (lines[m]+",")
                    line_to_write += "\n"
                    with open(csvName, 'a') as f:
                        f.writelines(line_to_write)

    return


# xml_make(dataDic)
# xml_make_std(config_dic=config_dic_default)
# xml_make_std( )  # 生成数据元数据信息的XML时候可以直接在默认字典上配置
