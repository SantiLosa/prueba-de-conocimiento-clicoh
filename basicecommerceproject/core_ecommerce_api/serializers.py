from rest_framework import serializers
from .utils import check_duplicates_in_list
from core_ecommerce.models import Product, Order, OrderDetail


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'
        extra_kwargs = {'order': {'read_only': True}}

    def validate(self, data):
        """
        Custom validations for each order detail
        """
        ok, error_message = data['product'].check_stock(data['quantity'])
        if not ok:
            raise serializers.ValidationError(error_message)
        return data


class OrderSerializer(serializers.ModelSerializer):
    order_details= OrderDetailSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        """
        Custom validations for order
        """
        # print("ENTRA VALIDATE OrderSerializer")
        # print("ENTRA VALIDATE OrderSerializer")
        if data.get('order_details', None):
            products_values = [order_detail['product'] for order_detail in data['order_details']]
            if check_duplicates_in_list(products_values):
                raise serializers.ValidationError('There cant be repeated products in the same order, just make one order detail with the total quantity')
        return data

    def create(self, validated_data):
        order_details_data = validated_data.pop('order_details')
        order = Order.objects.create(**validated_data)
        for order_detail_data in order_details_data:
            """We now know it's been validated that order details dont have repeated
            products and also there is enough stock to create each order, we now
            create each one and update the stock of each product"""
            new_order_detail = OrderDetail.objects.create(order=order, **order_detail_data)
            new_order_detail.product.subtract_stock(new_order_detail.quantity)
        return order

    
