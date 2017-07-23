from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^search_result/.+$', views.search_result, name='search_result'),
    url(r'^new_search_result/(?P<result>.*)$',
        views.new_search_result,
        kwargs={'result': ''},
        name='new_search_result')
]
