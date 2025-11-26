from .models import Customer, Order, OrderProduct, Category, Product
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .services import *
from config.settings import MEDIA_ROOT
from .forms import *

def home_page(request):
    if request.GET:
        product = get_product_by_id(request.GET.get("product_id", 0))
        return JsonResponse(product)


def order_page(request):
    if request.GET:
        user = get_user_by_phone(request.GET.get("phone_number"))
        return JsonResponse(user)


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get("orders")
    total_price = request.COOKIES.get("total_price",0)
    print(orders_list)
    print(total_price)
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                "product": Product.objects.get(pk=int(key)),
                "count": val
                }
            )
    ctx = {
        'categories': categories,
        'products': products,
        'orders':orders,
        'total_price':total_price,
        'MEDIA_ROOT': MEDIA_ROOT
    }

    response = render(request, 'food/index.html', ctx)
    response.set_cookie("greeting", 'hello')
    return response


def main_orderr(request):
    model=Customer()
    if request.method == "POST":
        phone_number = request.POST.get("phone_number", "").strip()
        if phone_number:
            try:
                model = Customer.objects.get(phone_number=phone_number)
            except Customer.DoesNotExist:
                model = Customer()
            except Customer.MultipleObjectsReturned:
                model = Customer.objects.filter(phone_number=phone_number).last()
        else:
            model = Customer()
        form = CustomerForm(request.POST or None, instance=model)
        if form.is_valid():
            customer = form.save()
            formOrder = OrderForm(request.POST or None, instance=Order())
            if formOrder.is_valid():
                order = formOrder.save(commit=False)
                order.customer = customer
                order.save()
                print("order:",order)
                orders_list = request.COOKIES.get("orders")


                for key,value in json.loads(orders_list).items():

                    product = get_product_by_id(int(key))


                    counts = value
                    order_product = OrderProduct(
                        count=counts,
                        price = product['price'],
                        product_id = product['id'],
                        order_id = order.id
                    )
                    order_product.save()

                return redirect("index")
            else:
                print(formOrder.errors)
        else:
            print(form.errors)

    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get("orders", "{}")
    total_price = request.COOKIES.get("total_price", 0)
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                "product": Product.objects.get(pk=int(key)),
                "count": val
                }
            )
    ctx = {
        'categories': categories,
        'products': products,
        'orders': orders,
        'total_price': total_price,
        'MEDIA_ROOT': MEDIA_ROOT,
        'customer': model,
    }

    response = render(request, 'food/order.html', ctx)
    response.set_cookie("greeting", 'hello')
    return response



def main_order(request):
    if request.method == "GET":
        categories = Category.objects.all()
        products = Product.objects.all()
        orders = []
        orders_list = request.COOKIES.get("orders")
        total_price = request.COOKIES.get("total_price", "0")

        try:
            total_price = float(total_price)
        except (ValueError, TypeError):
            total_price = 0.0

        if orders_list:
            try:
                order_dict = json.loads(orders_list)
                for key, val in order_dict.items():
                    try:
                        product = Product.objects.get(pk=int(key))
                        orders.append({
                            "product": product,
                            "count": int(val)
                        })
                    except (ValueError, Product.DoesNotExist):
                        continue
            except json.JSONDecodeError:
                pass

        ctx = {
            'categories': categories,
            'products': products,
            'orders': orders,
            'total_price': total_price,
        }
        return render(request, 'food/order.html', ctx)

    if request.method == "POST":
        orders_list = request.COOKIES.get("orders")
        if not orders_list:
            return redirect("index")

        try:
            order_dict = json.loads(orders_list)
            if not order_dict:
                return redirect("index")
        except json.JSONDecodeError:
            return redirect("index")

        phone_number = request.POST.get("phone_number", "").strip()
        if phone_number:
            try:
                model = Customer.objects.get(phone_number=phone_number)
            except Customer.DoesNotExist:
                model = Customer()
            except Customer.MultipleObjectsReturned:
                model = Customer.objects.filter(phone_number=phone_number).last()
        else:
            model = Customer()
        form = CustomerForm(request.POST or None, instance=model)
        if form.is_valid():
            customer = form.save()

            formOrder = OrderForm(request.POST)
            if not formOrder.is_valid():
                print("OrderForm xatolik:", formOrder.errors)
                return redirect("index")

            order = formOrder.save(commit=False)
            order.customer = customer
            order.save()


        for product_id_str, count in order_dict.items():
            try:
                product_id = int(product_id_str)
                product = Product.objects.get(pk=product_id)

                OrderProduct.objects.create(
                    order=order,
                    product=product,
                    count=int(count),
                    price=product.price
                )
            except (ValueError, Product.DoesNotExist) as e:
                print(f"Mahsulot topilmadi: {product_id_str} | Xato: {e}")
                continue

        response = redirect("index")
        response.delete_cookie("orders")
        response.delete_cookie("total_price")
        return response