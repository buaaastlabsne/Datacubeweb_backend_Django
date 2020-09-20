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
    url(r'^xml$', views.xml_make),
    url(r'^api/names$', views.get_names),
    url(r'^api/windt', views.wind_data),
    url(r'^api/delete', views.delete_files),
    url(r'data', views.get_data_for_plot),

    url(r'^api/FCM', views.FCM),

    url(r'^api/coeff', views.Coeff),
    url(r'^api/anova', views.Anova),
    url(r'^db/connect', views.connect),
    url(r'^db/tables', views.query_tables),
    url(r'^db/atable', views.query_a_tb),

    url(r'^api/cmeans$', views.cmeans),
    url(r'^api/cmeans/bar', views.bar),
    url(r'^api/cmeans/jms', views.jms),
    url(r'^api/cmeans/data', views.c_data),

    url(r'^api/meta_parse', views.meta_data_parse)
]
