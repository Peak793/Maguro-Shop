from django.contrib import admin
from django.urls import path,include,re_path
from myapp import views
#from store.myapp.views import aboutus

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('store/',views.store,name='store'),
    path('store/<slug:slug>/',views.detail,name='detail'),
    path('search/',views.search_item,name='search'),
    path('aboutus/',views.aboutus,name = 'aboutus'),
    path('manual/',views.manual,name = 'manual'),
    re_path(r'store/category/(?P<categoryid>[0-9]{1})/$',views.category,name = 'category'),
    re_path(r'store/sort/(?P<sortid>[0-9]{1})/$',views.sort,name = 'sort'),
    re_path(r'cart/add/(?P<slug>[\w-]+)/$', views.cart_add, name ='cart_add'),
    re_path(r'cart/delete/(?P<slug>[\w-]+)/$', views.cart_delete, name ='cart_delete'),
    re_path(r'cart/inc/(?P<slug>[\w-]+)/$', views.inc_qty, name ='inc_qty'),
    re_path(r'cart/dec/(?P<slug>[\w-]+)/$', views.dec_qty, name ='dec_qty'),
    re_path(r'cart/list/$', views.cart_list, name ='cart_list'),
]
