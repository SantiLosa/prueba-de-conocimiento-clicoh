from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from core_ecommerce.models import Order, Product, OrderDetail
from core_ecommerce_api.views import OrderDetailViewSet, OrderViewSet
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User



class OderTests(APITestCase):

    def setUp(self):
        Product.objects.create(name='producto1', price=5.99, stock=10)
        self.user = User.objects.create_superuser(
            username='santiago',
            password='admin',
            email='admin@admin.com'
        )


    def test_create_order(self):
        """
        Ensure we can create a new order object.
        """
        print("Creo el producto si esto es 1=", Product.objects.count())
        factory = APIRequestFactory()
        view = OrderViewSet.as_view({'post': 'create'})
        request = factory.post('/orders/',
                               {
                                "order_details": [
                                    {
                                        "quantity": 3,
                                        "product": 1
                                    },
                                ],
                                "date_time": "2022-07-23T22:29:00Z"
                                },
                               format='json')
        force_authenticate(request, user=self.user)
        # url = reverse('orders')
        # data = {'name': 'DabApps'}
        print(request)
        print("BODY")
        print(request.body)
        print(dir(request))
        response = view(request)
        # response = self.client.post(request)
        print(response)
        print(dir(response))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderDetail.objects.count(), 1)
        self.assertEqual(Product.objects.get(name='producto1').stock, 7)