from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product

class ProductSingleMixin(LoginRequiredMixin):
    model = Product
    context_object_name = "product"

class ProductListMixin(LoginRequiredMixin):
    model = Product
    context_object_name = "products"