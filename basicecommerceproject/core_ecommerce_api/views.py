from rest_framework import viewsets
from core_ecommerce.models import Product
from . import serializers


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
