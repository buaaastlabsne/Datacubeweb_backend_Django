from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import Book
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
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
            #a = request.POST.get('a', 0)
            # b = request.POST.get('b', 0)
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


from analysis import regression
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
                original_data, level0, level1, level2 = regression.pywt_data_new(address1, address2)
                dic['original-data'] = original_data
                dic['level10'] = level0.tolist()
                dic['level11'] = level1.tolist()
                dic['level12'] = level2.tolist()
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
            ep = float(request.POST.get('ep', 0))
            # 判断参数中是否含有a和b
            if address and ep:
                train_score,test_score = regression.test_LinearSVR_epsilon_new(address, ep)
                dic['train_score'] = train_score
                dic['test_score'] = test_score
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
            c = float(request.POST.get('c', 0))
            # 判断参数中是否含有a和b
            if address and c:
                train_score, test_score = regression.test_LinearSVR_C_new(address,c)
                dic['train_score'] = train_score
                dic['test_score'] = test_score
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
                y_test, y_predict = regression.predict_result_new(address, ep, c)
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
