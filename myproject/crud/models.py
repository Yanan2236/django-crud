from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="商品")
    price = models.PositiveIntegerField(verbose_name="価格")
    
    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        raise NotImplementedError("詳細ページ実装時に定義予定")
    
    class Meta:
        ordering = ["name"]
        verbose_name = "アイテム"
        verbose_name_plural = "商品一覧"
