from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()

    class Meta:
        verbose_name_plural = 'products'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product}'
