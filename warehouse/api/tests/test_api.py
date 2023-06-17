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
        User.objects.create_superuser(username='test', password='test')

    def setUp(self):
        """
        Create super_user, get his token and add it to headers

        Вызывается перед каждой тестовой функцией для настройки объектов, которые могут изменяться во время тестов
        (каждая функция тестирования будет получать "свежую" версию данных объектов).
        """
        self.client = APIClient()
        self.user = User.objects.get(username='test')
        url_token_auth = reverse('token')
        request_data = {"username": "test", "password": "test"}
        response = self.client.post(url_token_auth, request_data, format='json')
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.item_1 = Item.objects.create(name='Dark Beer', price='20.00', qty=100)
        self.item_2 = Item.objects.create(name='Sider', price='30.00', qty=1000)
        self.item_3 = Item.objects.create(name='Vodka', price='10.00', qty=2000)

    def test_post_item(self):
        """ post an item """
        item_data = {
              "name": "Beer",
              "price": "22.00",
              "qty": 2300
        }
        url = reverse('items-list')
        response = self.client.post(url, item_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_get_items(self):
        """ create some items and get list of them"""
        url = reverse('items-list')
        response = self.client.get(url)
        serializer_data = ItemSerializer([self.item_1, self.item_2, self.item_3], many=True).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

    def test_get_detail_put_patch_delete_item(self):
        """ Get item's details, put, patch and delete item """
        item_id = self.item_1.id

        url = reverse('items-detail', args=[item_id])

        response = self.client.get(url)
        serializer_data = ItemSerializer(self.item_1).data
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer_data)

        put_item_data = {
            "name": "Beer",
            "price": "20.10",
            "qty": 1000
        }
        response = self.client.put(url, put_item_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        patch_item_data = {
            "name": "Wine",
            "price": "25.00",
            "qty": 500
        }
        response = self.client.patch(url, patch_item_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

