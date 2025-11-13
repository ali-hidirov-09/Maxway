from django.db.models import Count
from  django.shortcuts import render, redirect
from Food.models import *
from . import forms
from . import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, user_login_failed


def login_required_decorator(func):
    return login_required(func, login_url="login_page" )


@login_required_decorator
def main_dashboard(request):
    categories = Category.objects.annotate(product_count=Count('product'))
    products = Product.objects.all()
    orders = Order.objects.all()
    customers = Customer.objects.all()
    categories_products = []
    table_list = services.get_table()
    for c in categories:
        categories_products.append(
            {
                "category": c.title,
                'product': len(Product.objects.filter(category_id=c.id))
             }
        )
    ctx = {
        "counts":{
            'categories': len(categories),
            'products': len(products),
            'orders': len(orders),
            'customers': len(customers)
        },
        "categories_products": categories_products,
        "table_list": table_list,
    }
    return render(request, 'dashboard/index.html', ctx)


def login_page(request):
    if request.POST:
        username = request.POST.get('username',None )
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_dashboard')
    return render(request, 'dashboard/login.html')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect('login_page')

