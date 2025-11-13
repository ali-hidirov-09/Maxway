from django.contrib import admin
from Food.models import Customer, Category, Product, Order
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Product)
