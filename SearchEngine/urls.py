from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^search_result/.*$', views.search_result, name='search_result'),
    #url(r'^result/(?P<page>\d+)?.*$', views.change_page, name='change_page'),
    url(r'^signup/', views.signup_view, name='signup'),
]
