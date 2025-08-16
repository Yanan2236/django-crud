from django import forms
from .models import Product

BASE_INPUT_CLS = "block w-full rounded border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": BASE_INPUT_CLS, "placeholder": "商品名"
            }),
            "price": forms.NumberInput(attrs={
                "class": BASE_INPUT_CLS, "min": "0", "step": "1", "placeholder": "価格"
            }),
        }
        labels = {
            "name": "商品名",
            "price": "価格",
        }