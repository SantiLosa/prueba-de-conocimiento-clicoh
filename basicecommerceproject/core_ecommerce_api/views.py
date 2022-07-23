from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core_ecommerce.models import Product, Order, OrderDetail
from . import serializers


class ProductViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OrderDetailViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = OrderDetail.objects.all()
    serializer_class = serializers.OrderDetailSerializer