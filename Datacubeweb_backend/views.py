from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import Book
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from analysis import regression
# Create your views here.


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
    from analysis import xml_parser
    if request.method == 'POST':  # 当提交表单时
        if request.POST:
            xmlFiles = []
            theme = request.POST.get('theme', 0)
            if theme:
                # names = json.dumps(listdir(address))
                address = 'D:\\综合自然环境数据立方库\\'
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
                    dic = {}
                    address1 = address + '\\' + name
                    target = xml_parser.xml_to_str(address1)
                    dic['name'] = name
                    dic['treeData'] = target
                    with open(address1, "r") as f:
                        xml_str = f.readlines()
                    for i in range(len(xml_str)):
                        xml_str[i] = xml_str[i].replace('\n', '').replace('\t', '')
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
