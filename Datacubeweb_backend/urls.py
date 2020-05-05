from django.conf.urls import url, include
from Datacubeweb_backend import views
urlpatterns = [
    url(r'add_book$', views.add_book, ), url(r'show_books$', views.show_books, ),
    url(r'^test$', views.post2),
    url(r'^pywt$', views.pywt),
    url(r'^ep$', views.test_ep),
    url(r'^c$', views.test_c),
    url(r'^epc$', views.test_ep_c),
    url(r'^predict$', views.predict),
               ]