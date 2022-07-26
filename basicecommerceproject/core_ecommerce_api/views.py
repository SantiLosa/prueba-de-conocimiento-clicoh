from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core_ecommerce.models import Product, Order, OrderDetail
from . import serializers
from .utils import validate_order_detail_ids_and_get_existing_ones, check_for_duplicate_product_ids


class ProductViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def update(self, request, pk=None):
        
        pass

    def partial_update(self, request, pk=None):
        """ Validate all order details in the request that have an id present, do have a counterpart existing in the database """
        if request.data.get('order_details', None):
            order_details_to_update, new_order_details = validate_order_detail_ids_and_get_existing_ones(request.data)
            has_order_details = True
        else:
            has_order_details = False
        order=Order.objects.get(pk=pk)
        serializer = serializers.OrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            """ Product ids in current serializer payload are fine, have to check for repeated products ids in orphan order details
            which are going to be created against current order existing details"""
            if has_order_details:
                check_for_duplicate_product_ids(new_order_details, order)
                order.update_order_details(order_details_to_update)
                order.add_new_order_details(new_order_details)
            elif serializer.data['date_time']:
                order.date_time = serializer.data['date_time']
                order.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    queryset = OrderDetail.objects.all()
    serializer_class = serializers.OrderDetailSerializer