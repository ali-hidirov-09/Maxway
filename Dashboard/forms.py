from django import  forms
from Food.models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }

class ProductForm(forms.ModelForm):
    class  Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form_control'}),
            "description": forms.TextInput(attrs={'class': 'form_control'}),
            "category": forms.Select(attrs={'class': 'form_control'}),
            "cost": forms.IntegerField(attrs={'class': 'form_control'}),
            "price": forms.IntegerField(attrs={'class': 'form_control'}),
            "image": forms.ImageField(attrs={'class': 'form_control', 'onchange':'loadFile(event)'}),
        }

class UserForm(forms.ModelForm):
    model = Customer
    fields = "__all__"
    widgets = {
        "first_name": forms.TextInput(attrs={'class': 'form_control'}),
        "last_name": forms.TextInput(attrs={'class': 'form_control'}),
        "phone_number": forms.TextInput(attrs={'class': 'form_control'}),
    }