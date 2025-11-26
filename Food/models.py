from django.db import models


class   Category(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Product(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    cost = models.IntegerField(null=False,blank=False)
    price = models.IntegerField(null=False,blank=False)
    image = models.ImageField(upload_to='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class Customer(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(unique=True, max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)
    adres = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    PAYMENT_CHOICES = (
        (1, "Naqd"),
        (2, "Terminal"),
    )
    STATUS_CHOICES = (
        (1, "Yangi"),
        (2, "Tasdiqlangan"),
    )

    payment_type = models.IntegerField(choices=PAYMENT_CHOICES, null=False, blank=False)
    status = models.IntegerField(choices=STATUS_CHOICES, null=False, blank=False)
    address = models.CharField(max_length=300, null=False, blank=False)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderProduct(models.Model):
    count = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)

