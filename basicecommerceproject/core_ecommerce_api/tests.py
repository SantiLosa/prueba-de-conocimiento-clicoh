from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from core_ecommerce.models import Order, Product, OrderDetail
from core_ecommerce_api.views import OrderDetailViewSet, OrderViewSet
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User



class OrderCreationTests(APITestCase):

    def setUp(self):
        Product.objects.create(name='producto1', price=5.99, stock=10)
        Product.objects.create(name='producto2', price=9.99, stock=10)
        self.user = User.objects.create_superuser(
            username='santiago',
            password='admin',
            email='admin@admin.com'
        )
    
    def test_create_order_with_repeated_products(self):
        """
        Ensure we cant create a new order object if it has repeated products in its order details.
        """
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'post': 'create'})
        request = factory.post('/orders/',
                                {
                                "order_details": [
                                    {
                                        "quantity": 1,
                                        "product": 1
                                    },
                                    {
                                        "quantity": 1,
                                        "product": 1
                                    },
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                                },
                                format='json')
        force_authenticate(request, user=self.user)
        # url = reverse('orders')
        # data = {'name': 'DabApps'}
        # print(request)
        # print("BODY")
        # print(request.body)
        # print(dir(request))
        response = view(request)
        # response = self.client.post(request)
        # print(response)
        # print(dir(response))
        print("test_create_order_with_repeated_products response")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderDetail.objects.count(), 0)
        self.assertEqual(Product.objects.get(name='producto1').stock, 10)

    def test_create_order(self):
        """
        Ensure we can create a new order object.
        """
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'post': 'create'})
        request = factory.post('/orders/',
                               {
                                "order_details": [
                                    {
                                        "quantity": 1,
                                        "product": 1
                                    },
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                                },
                               format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        print("test_create_order response")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 1)
        self.assertEqual(Product.objects.get(name='producto1').stock, 9)
    
    def test_create_order_exceding_quantity(self):
        """
        Ensure we can create a new order object.
        """
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'post': 'create'})
        request = factory.post('/orders/',
                               {
                                "order_details": [
                                    {
                                        "quantity": 100,
                                        "product": 1
                                    },
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                                },
                               format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        print("test_create_order_exceding_quantity response", response.data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderDetail.objects.count(), 0)
        self.assertEqual(Product.objects.get(name='producto1').stock, 10)

    def test_create_order_for_multiple_products(self):
        """
        Ensure we can create a new order object.
        """
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'post': 'create'})
        request = factory.post('/orders/',
                               {
                                "order_details": [
                                    {
                                        "quantity": 1,
                                        "product": 1
                                    },
                                    {
                                        "quantity": 1,
                                        "product": 2
                                    },
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                                },
                               format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        print("test_create_order_for_multiple_products response")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 9)
        self.assertEqual(Product.objects.get(name='producto2').stock, 9)
    
    
class OrderUpdateTests(APITestCase):

    def setUp(self):
        product1 = Product.objects.create(name='producto1', price=5.99, stock=10)
        product2 = Product.objects.create(name='producto2', price=9.99, stock=10)
        order = Order.objects.create(date_time=datetime.fromisoformat("2022-07-23T22:29:00Z"))
        OrderDetail.objects.create(order=order, product=product1, quantity=1)
        self.user = User.objects.create_superuser(
            username='santiago',
            password='admin',
            email='admin@admin.com'
        )
    
    def test_update_order(self):
        """
        Ensure we can create a new order object.
        """
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'update'})
        request = factory.patch('/orders/1',
                               {
                                "order_details": [
                                    {
                                        "id": 1
                                        "quantity": 2,
                                    },
                                ],
                                },
                               format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        print("test_update_order response")
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 9)
    
    # def test_create_order_with_repeated_products(self):
    #     """
    #     Ensure we cant create a new order object if it has repeated products in its order details.
    #     """
    #     factory = APIRequestFactory()
    #     view = OrderViewSet.as_view({'post': 'create'})
    #     request = factory.post('/orders/',
    #                             {
    #                             "order_details": [
    #                                 {
    #                                     "quantity": 1,
    #                                     "product": 1
    #                                 },
    #                                 {
    #                                     "quantity": 1,
    #                                     "product": 1
    #                                 },
    #                             ],
    #                             "date_time": "2022-07-23T22:29:00Z"
    #                             },
    #                             format='json')
    #     force_authenticate(request, user=self.user)
    #     # url = reverse('orders')
    #     # data = {'name': 'DabApps'}
    #     # print(request)
    #     # print("BODY")
    #     # print(request.body)
    #     # print(dir(request))
    #     response = view(request)
    #     # response = self.client.post(request)
    #     # print(response)
    #     # print(dir(response))
    #     print("test_create_order_with_repeated_products response")
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(Order.objects.count(), 0)
    #     self.assertEqual(OrderDetail.objects.count(), 0)
    #     self.assertEqual(Product.objects.get(name='producto1').stock, 10)
    
    # def test_create_order_exceding_quantity(self):
    #     """
    #     Ensure we can create a new order object.
    #     """
    #     factory = APIRequestFactory()
    #     view = OrderViewSet.as_view({'post': 'create'})
    #     request = factory.post('/orders/',
    #                            {
    #                             "order_details": [
    #                                 {
    #                                     "quantity": 100,
    #                                     "product": 1
    #                                 },
    #                             ],
    #                             "date_time": "2022-07-23T22:29:00Z"
    #                             },
    #                            format='json')
    #     force_authenticate(request, user=self.user)
    #     response = view(request)
    #     print("test_create_order_exceding_quantity response", response.data)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(Order.objects.count(), 0)
    #     self.assertEqual(OrderDetail.objects.count(), 0)
    #     self.assertEqual(Product.objects.get(name='producto1').stock, 10)

    # def test_create_order_for_multiple_products(self):
    #     """
    #     Ensure we can create a new order object.
    #     """
    #     factory = APIRequestFactory()
    #     view = OrderViewSet.as_view({'post': 'create'})
    #     request = factory.post('/orders/',
    #                            {
    #                             "order_details": [
    #                                 {
    #                                     "quantity": 1,
    #                                     "product": 1
    #                                 },
    #                                 {
    #                                     "quantity": 1,
    #                                     "product": 2
    #                                 },
    #                             ],
    #                             "date_time": "2022-07-23T22:29:00Z"
    #                             },
    #                            format='json')
    #     force_authenticate(request, user=self.user)
    #     response = view(request)
    #     print("test_create_order_for_multiple_products response")
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Order.objects.count(), 1)
    #     self.assertEqual(OrderDetail.objects.count(), 2)
    #     self.assertEqual(Product.objects.get(name='producto1').stock, 9)
    #     self.assertEqual(Product.objects.get(name='producto2').stock, 9)