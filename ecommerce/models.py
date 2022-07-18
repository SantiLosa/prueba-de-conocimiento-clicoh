from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()


class Order(models.Model):
    date_time = models.DateTimeField()


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1,
                    message="You must at least order 1 of this product")],
        )
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
