from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()


class Order(models.Model):
    date_time = models.DateTimeField()


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_details')
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1,
                    message="You must at least order 1 of this product")],
        )
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_details')

    def save(self, *args, **kwargs):
        if not self.pk:
            # This code only happens if the objects is
            # not in the database yet. Otherwise it would
            # have pk
            # print(self.product)
            print("ENTRA NUEVO PK")
            print(self.product)
            
        super(OrderDetail, self).save(*args, **kwargs)
