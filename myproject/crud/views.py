from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Product
from django.urls import reverse_lazy
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    paginate_by = 3

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("list")