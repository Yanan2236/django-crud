from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Item

class ItemListView(ListView):
    model = Item
    context_object_name = 'items'