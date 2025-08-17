from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="カテゴリ")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]
        verbose_name = "カテゴリ"
        verbose_name_plural = "カテゴリ一覧"

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="商品")
    price = models.PositiveIntegerField(verbose_name="価格")
    #カテゴリを埋めたらnull=False,bland=Falseにすること。
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", null=True, blank=True)
    img = models.ImageField(blank=True, default='noImage.png')
    description = models.TextField(blank=True, null=True, default='', verbose_name="商品詳細の説明")

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        raise NotImplementedError("詳細ページ実装時に定義予定")
    
    class Meta:
        ordering = ["name"]
        verbose_name = "アイテム"
        verbose_name_plural = "商品一覧"
