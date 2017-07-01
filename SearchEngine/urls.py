from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^search_result/(?P<pk>\d+)/', views.search_result, name='search_result'),
]