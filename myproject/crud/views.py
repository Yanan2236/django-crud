from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
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
    template_name = "crud/product_create_form.html"
    success_url = reverse_lazy("list")

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "crud/product_update_form.html"
    success_url = reverse_lazy("list")