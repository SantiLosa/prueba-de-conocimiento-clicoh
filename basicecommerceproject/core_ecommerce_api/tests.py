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
        print('')
        print("test_create_order_with_repeated_products response")
        print(response.data)
        print('')
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
        print('')
        print("test_create_order response")
        print(response.data)
        print('')
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
        print('')
        print("test_create_order_exceding_quantity response")
        print(response.data)
        print('')
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
        print('')
        print("test_create_order_for_multiple_products response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 9)
        self.assertEqual(Product.objects.get(name='producto2').stock, 9)
    
    
class OrderUpdateTests(APITestCase):


    def setUp(self):
        self.product1 = Product.objects.create(name='producto1', price=5.99, stock=10)
        self.product2 = Product.objects.create(name='producto2', price=9.99, stock=10)
        order = Order.objects.create(date_time="2022-07-23T22:29:00Z")
        OrderDetail.objects.create(order=order, product=self.product1, quantity=2)
        self.user = User.objects.create_superuser(
            username='santiago',
            password='admin',
            email='admin@admin.com'
        )


    def test_update_order_inexistent_id_detail(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('/orders/1/',
                               {
                                "order_details": [
                                    {
                                        "id": 5000,
                                        "quantity": 2,
                                        "product": 1
                                    }
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                            },
                            format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_inexistent_id_detail response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 10)
    

    def test_update_order_exceding_quantity(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('/orders/1/',
                               {
                                "order_details": [
                                    {
                                        "id": 1,
                                        "quantity": 80000,
                                        "product": 1
                                    }
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                            },
                            format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_exceding_quantity response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 10)
    

    def test_update_order_add_order_detail_with_repeated_product(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('/orders/1/',
                               {
                                "order_details": [
                                    {
                                        "quantity": 2,
                                        "product": 1
                                    }
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                            },
                            format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_add_order_detail_with_repeated_product response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 10)
    

    def test_update_order_increase_q_by_two_decrease_stock(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('/orders/1/',
                               {
                                "order_details": [
                                    {
                                        "id": 1,
                                        "quantity": 4,
                                        "order": 1,
                                        "product": 1
                                    }
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                            },
                            format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_increase_q_decrease_stock response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 4)
        self.assertEqual(Product.objects.get(name='producto1').stock, 8)
    

    def test_update_order_decrease_q_by_one_increase_stock(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('/orders/1/',
                               {
                                "order_details": [
                                    {
                                        "id": 1,
                                        "quantity": 1,
                                        "order": 1,
                                        "product": 1
                                    }
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                            },
                            format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_increase_q_decrease_stock response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 1)
        self.assertEqual(Product.objects.get(name='producto1').stock, 11)
    

    def test_update_order_change_product(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('/orders/1/',
                               {
                                "order_details": [
                                    {
                                        "id": 1,
                                        "quantity": 1,
                                        "order": 1,
                                        "product": 2
                                    }
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                            },
                            format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_increase_q_decrease_stock response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).product, self.product2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 12)
        self.assertEqual(Product.objects.get(name='producto2').stock, 9)


    def test_update_order_with_orphan_detail(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('/orders/1/',
                               {
                                "order_details": [
                                    {
                                        "quantity": 1,
                                        "order": 1,
                                        "product": 2
                                    }
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                            },
                            format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_with_orphan_detail response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 2)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 2)
        self.assertEqual(OrderDetail.objects.get(pk=1).product, self.product1)
        self.assertEqual(OrderDetail.objects.get(pk=2).quantity, 1)
        self.assertEqual(OrderDetail.objects.get(pk=2).product, self.product2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 10)
        self.assertEqual(Product.objects.get(name='producto2').stock, 9)


    def test_update_order_with_orphan_detail_and_update_existing_detail(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('/orders/1/',
                               {
                                "order_details": [
                                    {
                                        "quantity": 1,
                                        "order": 1,
                                        "product": 2
                                    },
                                    {
                                        "id": 1,
                                        "quantity": 1,
                                        "order": 1,
                                        "product": 1
                                    }
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                            },
                            format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_with_orphan_detail_and_update_existing_detail response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 2)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).product, self.product1)
        self.assertEqual(OrderDetail.objects.get(pk=2).quantity, 1)
        self.assertEqual(OrderDetail.objects.get(pk=2).product, self.product2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 11)
        self.assertEqual(Product.objects.get(name='producto2').stock, 9)


    def test_update_order_change_date(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'patch': 'partial_update'})
        request = factory.patch('/orders/1/',
                               {
                                "date_time": "2022-08-23T22:29:00Z"
                            },
                            format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_change_date response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get(pk=1).date_time.strftime("%Y-%m-%d, %H:%M:%S"), "2022-08-23, 22:29:00")
        self.assertEqual(OrderDetail.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 2)
        self.assertEqual(OrderDetail.objects.get(pk=1).product, self.product1)
        self.assertEqual(Product.objects.get(name='producto1').stock, 10)
    

class OrderDeleteTests(APITestCase):


    def setUp(self):
        self.product1 = Product.objects.create(name='producto1', price=5.99, stock=10)
        self.product2 = Product.objects.create(name='producto2', price=9.99, stock=10)
        order = Order.objects.create(date_time="2022-07-23T22:29:00Z")
        OrderDetail.objects.create(order=order, product=self.product1, quantity=2)
        OrderDetail.objects.create(order=order, product=self.product2, quantity=2)
        self.user = User.objects.create_superuser(
            username='santiago',
            password='admin',
            email='admin@admin.com'
        )


    def test_update_delete_order_multiple_details(self):
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'delete': 'delete'})
        request = factory.delete('/orders/1/', format='json')
        force_authenticate(request, user=self.user)
        response = view(request, pk=1)
        print('')
        print("test_update_order_inexistent_id_detail response")
        print(response.data)
        print('')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.get(pk=1).quantity, 2)
        self.assertEqual(Product.objects.get(name='producto1').stock, 12)
        self.assertEqual(Product.objects.get(name='producto2').stock, 12)