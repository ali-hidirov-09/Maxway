from django import forms
from .models import *

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

    def save(self, commit=True, *args, **kwargs):
        model = super().save(commit=False)
        model.customer = kwargs.get("customer", None)
        if commit:
            model.save()
        return model

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

    def save(self, commit=True, *args, **kwargs):
        customer = kwargs.get("customer", None)
        model = super().save(commit=False)
        model.customer = customer

        if hasattr(model, 'email') and customer:
            model.email = customer.email
        if hasattr(model, 'address') and customer:
            model.address = customer.address

        if commit:
            model.save()
        return model


class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = "__all__"
