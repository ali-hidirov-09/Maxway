from django.db.models import Count
from  django.shortcuts import render, redirect
from Food.models import *
from . import forms
from . import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate


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


"""Product: bu erda product yaratish, o'chirish, ozgartirish, ro'yhatini korish mumkin"""

@login_required_decorator
def product_create(request):
    model = Product()
    form = forms.ProductForm(request.POST or None,request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect("product_list")
    ctx = {
        "model":model,
        'form':form
    }
    return render(request, "dashboard/product/form.html", ctx)


@login_required_decorator
def product_edit(request, pk):
    model = Product.objects.get(pk=pk)
    form = forms.ProductForm(request.POST or None, request.FILES or None,instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect("product_list")
    ctx = {
        "model":model,
        "form":form
    }
    return render(request, "dashboard/product/form.html", ctx)


@login_required_decorator
def product_delete(request, pk):
    model = Product.objects.get(pk=pk)
    model.delete()
    return redirect("product_list")


@login_required_decorator
def product_list(request):
    products = Product.objects.all()
    ctx = {
        'products': products
    }
    return render(request, "dashboard/product/list.html", ctx)



"Category: Bu erda categoriyalar bilan ishlaymiz"
@login_required_decorator
def category_list(request):
    categories = Category.objects.all()
    ctx = {
        'categories':categories
    }
    return render(request, "dashboard/category/list.html", ctx)


@login_required_decorator
def category_create(request):
    model = Category()
    form = forms.CategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect("category_list")
    ctx = {
        'model':model,
        'form': form
    }
    return render(request, "dashboard/category/form.html", ctx)


@login_required_decorator
def category_edit(request, pk):
    model = Category.objects.get(pk=pk)
    form = forms.CategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect("category_list")

    ctx = {
        'model':model,
        'form':form
    }
    return render(request, "dashboard/category/form.html",ctx)

@login_required_decorator
def category_delete(request, pk):
    model = Category.objects.get(pk=pk)
    model.delete()
    return redirect("category_list")


"""User: userlar bilan ishlash"""
@login_required_decorator
def user_list(request):
    users = Customer.objects.all()
    ctx = {
        "users":users
    }
    return render(request, "dashboard/user/list.html", ctx)


@login_required_decorator
def user_delete(request, pk):
    model = Customer.objects.get(pk=pk)
    model.delete()
    return redirect("user_list")

@login_required_decorator
def user_create(request):
    model = Customer()
    form = forms.UserForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect("user_list")
    ctx = {
        'model':model,
        'form':form
    }
    return render(request, "dashboard/user/form.html",ctx)


@login_required_decorator
def user_edit(request, pk):
    model = Customer.objects.get(pk=pk)
    form = forms.UserForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()
        return redirect("user_list")
    ctx = {
        'model':model,
        'form':form
    }
    return render(request, "dashboard/user/form.html", ctx)


@login_required_decorator
def order_list(request):
    """Xamma zakazlar ro'yxati"""
    orders = Order.objects.all()
    ctx = {
        'orders':orders
    }
    return render(request, "dashboard/order/list.html", ctx)


@login_required_decorator
def orderproduct_list(request, id):
    productorders = services.get_product_by_order(id=id)
    for pro in productorders:
        pro['total'] = pro['count'] * pro['price']
    ctx = {
        'productorders': productorders
    }
    return render(request, "dashboard/productorder/list.html", ctx)


@login_required_decorator
def customer_order_list(request, id):
    customer_orders = services.get_order_by_user(id)
    ctx = {
        'customer_orders':customer_orders
    }
    return render(request, "dashboard/customer_order/list.html", ctx)