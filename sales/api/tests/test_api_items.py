from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from api.models import Item
from api.serializers import ItemSerializer


User = get_user_model()


class ItemsApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='test', password='test')

    def setUp(self):
        """
        Get user token and add it to headers. Create some items
        """
        self.client = APIClient()
        url_token_auth = reverse('token')
        request_data = {"username": "test", "password": "test"}
        response = self.client.post(url_token_auth, request_data, format='json')
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.item_1 = Item.objects.create(name='Test Dark Beer', price='20.00', qty=100)
        self.item_2 = Item.objects.create(name='Test Sider', price='30.00', qty=1000)
        self.item_3 = Item.objects.create(name='Test Vodka', price='10.00', qty=2000)

        self.unauthorized_client = APIClient()

    def test_get_items(self):
        """ create some items and get list of them"""
        url = reverse('items-list')
        response = self.client.get(url)
        serializer_data = ItemSerializer([self.item_1, self.item_2, self.item_3], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_item(self):
        """ Get item's details"""
        url = reverse('items-detail', args=[self.item_1.id])
        response = self.client.get(url)
        serializer_data = ItemSerializer(self.item_1).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

        response = self.unauthorized_client.get(url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
