from rest_framework import viewsets
from ecommerce.models import Product
from ecommerce.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
