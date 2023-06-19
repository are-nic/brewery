from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.models import OrderItem, Item, Order
from api.serializers import OrderListSerializer, OrderDetailSerializer


User = get_user_model()


class OrderApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='test')

        cls.item_1 = Item.objects.create(name='Test Dark Beer', price='20.00', qty=100)
        cls.item_2 = Item.objects.create(name='Test Sider', price='30.00', qty=1000)

        cls.order_1 = Order.objects.create(customer=cls.user, is_placed=False)
        cls.order_2 = Order.objects.create(customer=cls.user, is_placed=False)

        cls.order_item_1 = OrderItem.objects.create(order=cls.order_2, item=cls.item_1, qty=50)
        cls.order_item_2 = OrderItem.objects.create(order=cls.order_2, item=cls.item_2, qty=500)
        cls.order_item_3 = OrderItem.objects.create(order=cls.order_1, item=cls.item_2, qty=500)

    def setUp(self):
        """
        Get user token and add it to headers
        """
        self.client = APIClient()
        self.user = User.objects.get(username='test')
        url_token_auth = reverse('token')
        request_data = {"username": "test", "password": "test"}
        response = self.client.post(url_token_auth, request_data, format='json')
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.unauthorized_client = APIClient()

    def test_get_orders(self):
        """ get list of orders"""
        url = reverse('orders-list')
        response = self.client.get(url)
        serializer_data = OrderListSerializer([self.order_1, self.order_2], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_details(self):
        """ Get order's details """

        url = reverse('orders-detail', args=[self.order_1.id])

        response = self.client.get(url)
        serializer_data = OrderDetailSerializer(self.order_1).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_order(self):
        """ Create an order """
        order_data = {
            "items": [
                {
                    "item": 1,
                    "qty": 100
                },
                {
                    "item": 2,
                    "qty": 100
                }
            ],
            "is_placed": False
        }

        url = reverse('orders-list')
        response = self.client.post(url, order_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.unauthorized_client.post(url, order_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_order(self):
        """ Update the order """
        order_data = {
            "items": [
                {
                    "item": 1,
                    "max_qty": True
                },
                {
                    "item": 2,
                    "qty": 100
                }
            ],
            "is_placed": False
        }

        url = reverse('orders-detail', args=[self.order_2.id])
        response = self.client.put(url, order_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.unauthorized_client.put(url, order_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_order(self):
        """ Partial update the order """
        order_data = {
            "items": [
                {
                    "item": 2,
                    "qty": 50
                }
            ],
            "is_placed": True
        }

        url = reverse('orders-detail', args=[self.order_2.id])
        response = self.client.patch(url, order_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.unauthorized_client.patch(url, order_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_order(self):
        """ Delete the Order """
        url = reverse('orders-detail', args=[self.order_2.id])
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.unauthorized_client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)