from django.shortcuts import render
from .services import *
from .models import *
import json
from .models import *
from django.shortcuts import redirect,render
from django.http import JsonResponse
from config.settings import MEDIA_ROOT

def home_page(request):
    if request.GET:
        product = get_product_by_id(request.GET.get("product_id", 0))
        return JsonResponse(product)

def order_page(request):

    return render(request, "food/order.html")


def index(request):

    return render(request, "food/index.html")


def main_order(reques):

    return render(reques, "food/order.html")