from django.db import models
from rest_framework import serializers
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

    def subtract_stock(self, quantity):
        """
        Updates stock given a validated order detail
        """
        self.stock -= quantity
        self.save()

class Order(models.Model):
    date_time = models.DateTimeField()

    def update_order_details(self, order_details_to_update):
        for order_detail in order_details_to_update:
            """We pop this so we dont allow order details to be moved between orders"""
            order_detail.pop('order')
            self.order_details.get(pk=order_detail.pop('id')).update(**order_detail)


    def add_new_order_details(self, new_order_details):
        for new_order_detail in new_order_details:
            new_order_detail.pop('order')
            product =  Product.objects.get(pk=new_order_detail.pop('product'))
            order_detail = OrderDetail.objects.create(product=product, order=self,**new_order_detail)
            order_detail.order = self
            order_detail.product.subtract_stock(order_detail.quantity)
            order_detail.save()


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_details')
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1,
                    message="You must at least order 1 of this product")],
        )
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_details')


    def update(self, **kwargs):
        """We already validated there's enough stock for this update in the serializer
        now we just find out if it's increasing or decreasing the stock"""
        new_product = Product.objects.get(pk=kwargs['product'])
        if new_product != self.product:
            """Changes product, restore quantity and subtract from new one"""
            self.product.subtract_stock(-1*self.quantity)
            self.product = new_product
            self.quantity = kwargs['quantity'] 
            self.product.subtract_stock(self.quantity)
        else:
            """ Has same product, subtract difference between quantities"""
            diff = kwargs['quantity'] - self.quantity
            self.quantity = kwargs['quantity'] 
            self.product.subtract_stock(diff)
        self.save()