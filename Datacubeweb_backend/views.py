from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import Book
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseBadRequest
from analysis import regression
# Create your views here.
# 以下字典根据Environmental Data Coding Specification (EDCS)
EDCS = {
         "ATM_PRESSURE": {"eac": "EAC_ATM_PRESSURE", "CHNName": "大气压强", "unit": "hPa"},
         "AIR_TEMPERATURE": {"eac": "EAC_AIR_TEMPERATURE", "CHNName": "大气温度", "unit": "℃"},
         "WIND_SPEED_U": {"eac": "EAC_WIND_SPEED_U", "CHNName": "经向风速", "unit": "m/s"},
         "WIND_SPEED_V": {"eac": "EAC_WIND_SPEED_V", "CHNName": "纬向风速", "unit": "m/s"},
         "WIND_SPEED_W": {"eac": "EAC_WIND_SPEED_W", "CHNName": "垂直风速", "unit": "m/s"},
}


@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        # books = Book.objects.filter()
        # bookList = json.loads(serializers.serialize("json", books))
        bookList = []
        bookitem1 = {
            'pk': 1,
            'model': 'myApp',
            'book_name': '金瓶梅',
            'add_time': '2020年1月17日'
        }
        bookitem2 = {
            'pk': 2,
            'model': 'myApp',
            'book_name': '我的祖国',
            'add_time': '2020年1月17日'
        }
        bookitem3 = {
            'pk': 2,
            'model': 'myApp',
            'book_name': '金瓶梅',
            'add_time': '2020年1月7日'
        }
        bookitem4 = {
            'pk': 2,
            'model': 'myApp',
            'book_name': '我的祖国',
            'add_time': '2020年1月1日'
        }
        bookitem5 = {
            'pk': 2,
            'model': 'myApp',
            'book_name': '我的祖国',
            'add_time': '2021年1月1日'
        }
        bookList.append(bookitem1)
        bookList.append(bookitem2)
        bookList.append(bookitem3)
        bookList.append(bookitem4)
        bookList.append(bookitem5)
        response['data'] = bookList
        response['code'] = '200'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 定义功能
def add_args(a, b):
    return a + b


# 接口函数
@csrf_exempt
def post2(request):
    if request.method == 'POST':  # 当提交表单时
        dic = {}
        # 判断是否传参
        print('this')
        print(request.POST)
        if request.POST:
            print('a+b')
            post_body = request.body
            post_body = json.load(post_body)
            print(post_body)
            a = post_body['a']
            b = post_body['b']
            if a and b:
                res = add_args(a, b)
                dic['number'] = res
                dic = json.dumps(dic)
                return HttpResponse(dic)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def pywt(request):
    if request.method == 'POST':  # 当提交表单时
        dic = {}
        if request.POST:
            # 两个地址分别是读取的原始数据和输出结果的地址
            address1 = request.POST.get('address1', 0)
            address2 = request.POST.get('address2', 0)
            # 判断参数中是否含有a和b
            if address1 and address2:
                original_data, level0, level1, level2, recoeffs = regression.pywt_data_new(address1, address2)
                dic['original-data'] = original_data
                dic['level10'] = level0.tolist()
                dic['level11'] = level1.tolist()
                dic['level12'] = level2.tolist()
                dic['recoeffs'] = recoeffs.tolist()
                dic = json.dumps(dic)
                return HttpResponse(dic)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def test_ep(request):
    if request.method == 'POST':  # 当提交表单时
        dic = {}
        if request.POST:
            address = request.POST.get('address', 0)
            # 判断参数中是否含有a和b
            if address:
                epsilons, train_scores, test_scores = regression.test_LinearSVR_epsilon_new(address)
                dic['epsilons'] = train_scores
                dic['train_scores'] = train_scores
                dic['test_scores'] = test_scores
                dic = json.dumps(dic)
                return HttpResponse(dic)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def test_c(request):
    if request.method == 'POST':  # 当提交表单时
        dic = {}
        if request.POST:
            address = request.POST.get('address', 0)
            # 判断参数中是否含有a和b
            if address:
                Cs, train_scores, test_scores = regression.test_LinearSVR_C_new(address)
                dic['Cs'] = Cs
                dic['train_scores'] = train_scores
                dic['test_scores'] = test_scores
                dic = json.dumps(dic)
                return HttpResponse(dic)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def test_ep_c(request):
    if request.method == 'POST':  # 当提交表单时
        dic = {}
        if request.POST:
            address = request.POST.get('address', 0)
            ep = float(request.POST.get('ep', 0))
            c = float(request.POST.get('c', 0))
            if address and ep and c:
                ep_train, ep_test = regression.test_LinearSVR_epsilon_new(address, ep)
                c_train, c_test = regression.test_LinearSVR_epsilon_new(address, c)
                dic['ep_train'] = ep_train
                dic['ep_test'] = ep_test
                dic['c_train'] = c_train
                dic['c_test'] = c_test
                dic = json.dumps(dic)
                return HttpResponse(dic)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def predict(request):
    if request.method == 'POST':  # 当提交表单时
        dic = {}
        if request.POST:
            address = request.POST.get('address', 0)
            ep = float(request.POST.get('ep', 0))
            c = float(request.POST.get('c', 0))
            if address and ep and c:
                x_label, y_test, y_predict = regression.predict_result_new(address, ep, c)
                dic['x_label'] = x_label
                dic['y_test'] = y_test
                dic['y_predict'] = y_predict
                dic = json.dumps(dic)
                return HttpResponse(dic)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


from analysis import xml_maker
@csrf_exempt
def xml_make(request):
    if request.method == 'POST':  # 当提交表单时
        rq_p = request.POST
        if request.POST:
            post_body = json.loads(rq_p['data'])
            xml_maker.xml_make(post_body)
            if True:
                xmFolder = ''
                if post_body['theme'] == 'Atmosphere':
                    xmlFolder = '大气环境'
                elif post_body['theme'] == 'Ocean':
                    xmlFolder = '海洋环境'
                elif post_body['theme'] == 'Land':
                    xmlFolder = '地形环境'
                else:
                    xmlFolder = '空间环境'
                filePath = 'D:/综合自然环境数据立方库/' + xmlFolder + '/' + post_body['xmlName']
                return HttpResponse(open(filePath, "rb"), content_type="text/xml")
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def get_names(request):
    from os import listdir
    from analysis import xml_parser_meta
    if request.method == 'POST':  # 当提交表单时
        if request.POST:
            xmlFiles = []
            theme = request.POST.get('theme', 0)
            if theme:
                # names = json.dumps(listdir(address))
                address = 'D:\\综合自然环境数据立方库\\'
                address = 'E:\\datacube_new\\weekend\\Datacubeweb_backend_Django\\analysis\\xmlCsv\\'
                if theme == 'atmosphere':
                    address = address + '大气环境'
                elif theme == 'ocean':
                    address = address + '海洋环境'
                elif theme == 'land':
                    address = address + '地形环境'
                else:
                    address = address + '空间环境'
                names = listdir(address)
                for name in names:
                    if ".xml" in name:
                        dic = {}
                        address1 = address + '\\' + name
                        target = xml_parser_meta.xml_to_str_std(address1)  # target = xml_parser.xml_to_str(address1)
                        dic['name'] = name
                        dic['treeData'] = target
                        with open(address1, "r") as f:
                            xml_str = f.readlines()
                        for i in range(len(xml_str)):
                            xml_str[i] = xml_str[i].replace('\n', '').replace('\t', '')#.replace('\\','')
                        dic['xmlStr'] = json.dumps(xml_str)
                        dic['menuVisible'] = False
                        xmlFiles.append(dic)
                return HttpResponse(json.dumps(xmlFiles))
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def wind_data(request):
    if request.method == 'GET':
        with open("windtp.json") as f:
            loadData = json.load(f)
            jsonData = json.dumps(loadData)
        return HttpResponse(jsonData)
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def delete_files(request):
    from os import remove
    if request.method == "POST":
        if request.POST:
            address = request.POST.get('address', 0)
            if address:
                remove(address)
                return HttpResponse("成功删除{}".format(address))
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')

@csrf_exempt
def get_data_for_plot(request):
    from analysis import universal_data_interface
    if request.method == 'POST':
        if request.POST:
            Source = request.POST.get('source')
            measure = request.POST.get('measure')
            lonMax = float(request.POST.get('lonMax'))
            lonMin = float(request.POST.get('lonMin'))
            latMax = float(request.POST.get('latMax'))
            latMin = float(request.POST.get('latMin'))
            heightMax = int(request.POST.get('heightMax'))
            heightMin = int(request.POST.get('heightMin'))
            ratio_lon = float(request.POST.get('ratioLon'))
            ratio_lat = float(request.POST.get('ratioLat'))
            ratio_h = float(request.POST.get('ratioHeight'))
            timeStamp = int(request.POST.get('timeStamp'))
            rotate = int(request.POST.get('rotate'))
            if Source and measure and lonMax and lonMin and latMax and latMin and heightMin and heightMax:
                data = universal_data_interface.get_data(Source=Source, measure=measure,
                                                        lonMin=lonMin, lonMax=lonMax,
                                                        latMin=latMin, latMax=latMax,
                                                        heightMin=heightMin, heightMax=heightMax,
                                                        ratio_lon=ratio_lon, ratio_lat=ratio_lat, ratio_h=ratio_h,
                                                        timeStamp=timeStamp,
                                                        rotate=rotate)
                print(data)
                if type(data)== type("0"):
                    return  HttpResponseBadRequest
                data = json.dumps(data)
                return HttpResponse(data)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def FCM(request):
    from analysis import c_means
    if request.method == 'POST':  # 当提交表单时
        if request.POST:
            address = request.POST.get('address', 0)
            c = int(request.POST.get('c', 0))
            m = int(request.POST.get('m', 0))
            if address and c:
                target = json.dumps(c_means.c_means_n(address, c, m))
                return HttpResponse(target)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def cmeans(request):
    from analysis import c_means
    if request.method == 'POST':  # 当提交表单时
        if request.POST:
            address = request.POST.get('address', 0)
            if address:
                target = json.dumps(c_means.c_means_new(address).tolist())
                return HttpResponse(target)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')

    else:
        return HttpResponse('方法错误')


@csrf_exempt
def bar(request):
    from analysis import c_means
    if request.method == 'GET':
        y1s, y2s = c_means.bar_data()
        dict = {"y1s": y1s, "y2s": y2s}
        target = json.dumps(dict)
        return HttpResponse(target)
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def jms(request):
    from analysis import c_means
    if request.method == 'GET':
        target = json.dumps(c_means.jms_data())
        return HttpResponse(target)
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def c_data(request):
    from analysis import c_means
    if request.method == 'GET':
        if "type" in request.GET:
            type = request.GET["type"]
            if type == "jms":
                target = json.dumps(c_means.jms_data())
                return HttpResponse(target)
            elif type == "bar":
                y1s, y2s = c_means.bar_data()
                dict = {"y1s": y1s, "y2s": y2s}
                target = json.dumps(dict)
                return HttpResponse(target)
            else:
                return HttpResponse('选择h合适的数据类型')
        else:
            return HttpResponse('选择返回的数据类型')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def Coeff(request):
    from analysis import coeff
    if request.method == 'POST':  # 当提交表单时
        if request.POST:
            address = request.POST.get('address', 0)
            measure1 = request.POST.get('measure1', 0)
            measure2 = request.POST.get('measure2', 0)
            if address:
                if measure1 and measure2:
                    target = json.dumps(coeff.coeff(filename=address, measures=[measure1, measure2]))
                    return HttpResponse(target)
                else:
                    target = json.dumps(coeff.coeff(filename=address, measures=None))
                    return HttpResponse(target)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def Anova(request):
    from analysis import coeff
    if request.method == 'POST':  # 当提交表单时
        if request.POST:
            address = request.POST.get('address', 0)
            if address:
                target = json.dumps(coeff.anova(address))
                return HttpResponse(target)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')

user = ""
passwd = ""
db = ""
@csrf_exempt
def connect(request):
    from analysis import dataBase
    if request.method == 'POST':
        if request.POST:
            global user, passwd, db
            user = request.POST.get('user', 0)
            passwd = request.POST.get('passwd', 0)
            db = request.POST.get('db', 0)
            if user and passwd and db:
                state = dataBase.connect(user,passwd,db)
                if state != 2:
                    return HttpResponse('Unauthorized', status=401)
                state = json.dumps(state)
                return HttpResponse(state)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def query_tables(request):
    from analysis import dataBase
    if request.method == 'GET':
        try:
            tables = dataBase.query_tables(user, passwd, db)  # tables = [user, passwd, db]
            tables = json.dumps(tables)
            return HttpResponse(tables)
        except:
            return HttpResponse("请重新连接数据库")
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def query_a_tb(request):
    from analysis import dataBase
    if request.method == 'POST':  # 当提交表单时
        if request.POST:
            tb = request.POST.get('table', 0)
            if tb:
                info =dataBase.query_a_table(user, passwd, db, tb)
                info = json.dumps(info)
                return HttpResponse(info)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def meta_data_parse(request):
    # 此端口可以解析新统一格式的xml文件
    from analysis import xml_parser_meta
    if request.method == 'POST':  # 当提交表单时
        if request.POST:
            fileName = request.POST.get('fileName', 0)
            if fileName:
                info = xml_parser_meta.xml_to_str_std(fileName)
                info = json.dumps(info)
                return HttpResponse(info)
            else:
                return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')


@csrf_exempt
def xml_make_std(request):
    """此端口获取前端给出的查询命令，生成指定度量，指定范围，指定经度的csv格式环境数据及其对应的xml"""
    from analysis import xml_maker_meta
    if request.method == 'POST':
        rq_p = request.POST
        if request.POST:
            # try:
            post_body = json.loads(rq_p['data'])
            # 根据前端信息修改xml-config,用于生成xml
            config_dic = {
                'theme': 'Atmosphere',
                "factList": "TPV",
                "xmlName": 'tpv_std_test.xml',
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
                    {"longitude_min": "114.014400", "longitude_max": "116.863300", "longitude_delta": "0.2"},
                    {"latitude_min": "18.047620", "latitude_max": "19.952380", "latitude_delta": "0.2"},
                    # {"heights": "106.655  154.066  204.447  257.986  ","height_n": "4"},
                    {"height_max": "25000", "height_min": "500", "height_delta": "500"}
                ]
            }

            if "xmlName" in post_body:
                config_dic["xmlName"] = post_body["xmlName"]+".xml"
            if "time" in post_body:
                config_dic["range"][0]["time_start"] = post_body["time"][0]
                config_dic["range"][0]["time_delta"] = post_body["time"][1]
                config_dic["range"][0]["time_n"] = post_body["time"][2]
            if "longitude" in post_body:
                config_dic["range"][1]["longitude_min"] = post_body["longitude"][0]
                config_dic["range"][1]["longitude_max"] = post_body["longitude"][1]
                config_dic["range"][1]["longitude_delta"] = post_body["longitude"][2]
            if "latitude" in post_body:
                config_dic["range"][2]["latitude_min"] = post_body["latitude"][0]
                config_dic["range"][2]["latitude_max"] = post_body["latitude"][1]
                config_dic["range"][2]["latitude_delta"] = post_body["latitude"][2]
            if "height" in post_body:
                config_dic["range"][3]["height_min"] = post_body["height"][0]
                config_dic["range"][3]["height_max"] = post_body["height"][1]
                config_dic["range"][3]["height_delta"] = post_body["height"][2]
            if "variables" in post_body:
                config_dic["measures"] = []
                for variable in post_body["variables"]:
                    config_dic["measures"].append(EDCS[variable])
            if "theme" in post_body:
                config_dic["theme"] = post_body["theme"]
            if "factList" in post_body:
                config_dic["factList"] =post_body["factList"]
            # 生成包含临时生成的查询信息的xml文件
            xml_maker_meta.xml_make_std(config_dic=config_dic, write_csv=True)
            # 保存临时xml文件
            if config_dic['theme'] == 'Atmosphere':
                xmlFolder = '大气环境'
            elif config_dic['theme'] == 'Ocean':
                xmlFolder = '海洋环境'
            elif config_dic['theme'] == 'Land':
                xmlFolder = '地形环境'
            else:
                xmlFolder = '空间环境'
            # 下面这里只是为了读文件返还给前端
            # filePath = 'E:/综合自然环境数据立方库/' + xmlFolder + '/' + post_body['xmlName']
            filePath = r"analysis/xmlCsv/"+ xmlFolder + '/'+config_dic["xmlName"]
            return HttpResponse(open(filePath, "rb"), content_type="text/xml")
            # except:
            #     print("字典信息配置错误")
            #     return HttpResponse('输入错误')
        else:
            return HttpResponse('输入为空')
    else:
        return HttpResponse('方法错误')