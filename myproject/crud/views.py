from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Product
from django.urls import reverse_lazy
from .forms import ProductForm
from .mixins import ProductSingleMixin, ProductListMixin

class ProductListView(ProductListMixin, ListView):
    paginate_by = 3

class ProductCreateView(ProductSingleMixin, CreateView):
    form_class = ProductForm
    template_name = "crud/product_create_form.html"
    success_url = reverse_lazy("list")

class ProductUpdateView(ProductSingleMixin, UpdateView):
    form_class = ProductForm
    template_name = "crud/product_update_form.html"
    success_url = reverse_lazy("list")

class ProductDeleteView(ProductSingleMixin, DeleteView):
    success_url = reverse_lazy("list")

class ProductDetailView(ProductSingleMixin, DetailView):
    pass