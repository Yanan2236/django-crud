from django.contrib import admin 
from .models import Product, Category
from django.utils.safestring import mark_safe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'image')
    search_fields = ('name',)
    list_filter = ('category',)

    def image(self, obj):
        return mark_safe(f'<img src="{obj.img.url}" alt="商品画像" style="width:100px; height:auto;">')