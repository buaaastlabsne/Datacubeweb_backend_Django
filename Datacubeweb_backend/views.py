from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
import json
from .models import Book

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