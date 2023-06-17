from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.models import OrderItem, Item
from api.serializers import OrderItemSerializer


User = get_user_model()


class OrderItemsApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='test', password='test')

        item_1 = Item.objects.create(name='Dark Beer', price='20.00', qty=100)
        item_2 = Item.objects.create(name='Sider', price='30.00', qty=1000)
        item_3 = Item.objects.create(name='Vodka', price='10.00', qty=2000)

        cls.order_item_1 = OrderItem.objects.create(item=item_1, qty=50)
        cls.order_item_2 = OrderItem.objects.create(item=item_2, qty=500)
        cls.order_item_3 = OrderItem.objects.create(item=item_3, qty=550)

    def setUp(self):
        """
        Create super_user, get his token and add it to headers
        """
        self.client = APIClient()
        self.user = User.objects.get(username='test')
        url_token_auth = reverse('token')
        request_data = {"username": "test", "password": "test"}
        response = self.client.post(url_token_auth, request_data, format='json')
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_get_order_items(self):
        """ get list of order items"""
        url = reverse('order_items-list')
        response = self.client.get(url)
        serializer_data = OrderItemSerializer([self.order_item_1, self.order_item_2, self.order_item_3], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

    def test_get_detail_order_item(self):
        """ Get order item's details """

        url = reverse('order_items-detail', args=[self.order_item_1.id])

        response = self.client.get(url)
        serializer_data = OrderItemSerializer(self.order_item_1).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)


