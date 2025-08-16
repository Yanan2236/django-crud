from django.urls import path
from . import views


urlpatterns = [
    path("", views.ProductListView.as_view(), name="list"),
    path("new/", views.ProductCreateView.as_view(), name="new"),
    path("edit/<int:pk>", views.ProductUpdateView.as_view(), name="edit")
]