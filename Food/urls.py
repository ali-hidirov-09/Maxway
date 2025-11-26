from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home_page/', views.home_page, name='home_page'),
    path('order_page/', views.order_page, name='order_page'),
    path('main_order/', views.main_order, name='main_order'),
]
