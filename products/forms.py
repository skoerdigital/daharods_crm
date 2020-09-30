from django import forms
from .models import Product, ProductParameter

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('owner','slug')

class ProductParameterCreateForm(forms.ModelForm):
    class Meta:
        model = ProductParameter
        exclude = ('product',)
