from django.conf.urls import url

from postapi import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^index/$', views.Index.as_view(), name='index'),
    url(r'^api/$', views.Api.as_view(), name='index'),
]
