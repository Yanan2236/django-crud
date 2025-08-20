from django.core.validators import MinValueValidator
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Item(TimeStampedModel, IsActiveMixin):
    name = models.CharField(max_length=255, verbose_name="商品名")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="値段",
        )
    description = models.TextField(blank=True, verbose_name="商品詳細")

    class Meta:
        ordering = ["price"]
        indexes = [
            models.Index(fields=['is_active']),
        ]

        
    