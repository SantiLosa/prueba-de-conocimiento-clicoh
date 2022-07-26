from core_ecommerce.models import Product, Order, OrderDetail
from rest_framework import serializers

def check_duplicates_in_list(list):
    set_list = set()
    for item in list:
        if item in set_list:
            return True
        else:
            set_list.add(item)
    return False


def validate_order_detail_ids_and_get_existing_ones(request_data):
    """ Matches order details in request against the ones that exist in the database,
    if they have an id field sent in the request, THEY MUST EXIST """
    order_details = [order_detail for order_detail in request_data['order_details']]
    inexistent_order_detail_ids_index = []
    order_details_to_update = []
    new_order_details = []
    for i,order_detail in enumerate(order_details):
        id = order_detail.get('id', None)
        if id: 
            if not OrderDetail.objects.filter(pk=id).exists():
                inexistent_order_detail_ids_index.append(i)
            else:
                order_details_to_update.append(order_detail)
        else:
            new_order_details.append(order_detail)

    if inexistent_order_detail_ids_index:
        raise serializers.ValidationError(f'The order details sent in this positions {inexistent_order_detail_ids_index} have ids that doesnt correspond to any order')
    
    return order_details_to_update, new_order_details


def check_for_duplicate_product_ids(new_order_details, order):
    """ Validates patch request data against current products id in the current order being edited """
    order_details_with_repeated_product_ids = []
    for order_detail in new_order_details:
        if OrderDetail.objects.filter(order=order,product=order_detail['product']).exists():
            order_details_with_repeated_product_ids.append(order_detail)

    if order_details_with_repeated_product_ids:
        raise serializers.ValidationError(f'This order already has a product with theese product ids: {order_details_with_repeated_product_ids}')