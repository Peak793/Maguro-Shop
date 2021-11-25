from django.contrib import admin
from django.urls import path,include,re_path
from myapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('store/',views.store,name='store'),
    path('store/<slug:slug>/',views.detail,name='detail'),
    re_path(r'cart/add/(?P<slug>[\w-]+)/$', views.cart_add, name ='cart_add'),
    re_path(r'cart/list/$', views.cart_list, name ='cart_list'),
]
