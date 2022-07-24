from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()

    def check_stock(self, quantity):
        """
        Checks if there is enough stock for an order detail with this quantity
        """
        if self.stock < quantity:
            return False, f"There is not enough stock to make this order, try with something less or equal to {self.stock}"
        return True, None

    def update_stock(self, quantity):
        """
        Updates stock given a validated order detail
        """
        self.stock -= quantity
        self.save()

class Order(models.Model):
    date_time = models.DateTimeField()


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_details')
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1,
                    message="You must at least order 1 of this product")],
        )
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_details')

