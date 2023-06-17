from unittest import TestCase
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from api.views import ItemViewSet
from django.urls import reverse
from api.models import Item
from rest_framework import status

User = get_user_model()


class ViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_superuser(username='test', password='test')
        cls.factory = APIRequestFactory()
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=100)

    @classmethod
    def tearDownClass(cls):
        Item.objects.get(name='Test Golden Beer').delete()
        cls.user.delete()
        cls.item.delete()

    def test_get_view_set(self):
        view = ItemViewSet.as_view(actions={'get': 'list'})
        request = self.factory.get(reverse('items-list'))
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_post_view_set(self):
        view = ItemViewSet.as_view(actions={'post': 'create'})

        post_item_data = {
            "name": "Test Golden Beer",
            "price": "24.00",
            "qty": 200
        }

        request = self.factory.post(reverse('items-list'), data=post_item_data)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_get_item_detail_view_set(self):
        view = ItemViewSet.as_view(actions={'get': 'retrieve'})
        url = reverse('items-detail', args=[self.item.id])
        request = self.factory.get(url)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request, pk=self.item.id)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_put_item_view_set(self):
        view = ItemViewSet.as_view(actions={'put': 'update'})
        url = reverse('items-detail', args=[self.item.id])
        put_item_data = {
            "name": "Test Water",
            "price": "29.10",
            "qty": 10000
        }
        request = self.factory.put(url, data=put_item_data)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request, pk=self.item.id)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_patch_item_view_set(self):
        view = ItemViewSet.as_view(actions={'patch': 'partial_update'})
        url = reverse('items-detail', args=[self.item.id])
        put_item_data = {
            "price": "30.00"
        }
        request = self.factory.patch(url, data=put_item_data)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request, pk=self.item.id)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_item_view_set(self):
        item = Item.objects.create(name='Test Vodka', price='33.00', qty=100)
        view = ItemViewSet.as_view(actions={'delete': 'destroy'})
        url = reverse('items-detail', args=[item.id])
        request = self.factory.delete(url)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
        response = view(request, pk=item.id)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)