from rest_framework import serializers
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

    def create(self, validated_data):
        print("entra create order detail serializer")
        # asd
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    order_details= OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        print("validated_data", validated_data)
        order_details_data = validated_data.pop('order_details')
        order = Order.objects.create(**validated_data)
        for order_detail_data in order_details_data:
            OrderDetail.objects.create(order=order, **order_detail_data)
        return order

        # return super().create(validated_data)
    
