from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='food_menu'),
    path('order_page/', views.order_page, name='order_page'),
    path('index/', views.index, name='index'),
    path('main_order/', views.main_order, name='main_order'),
]
