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


class OrderSerializer(serializers.ModelSerializer):
    order_details= OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
    
    def create(self, validated_data):
        for order in validated_data['order_details']:
            
        print("validated_data", validated_data)
        asd
        return super().create(validated_data)
