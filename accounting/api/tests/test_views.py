from unittest import TestCase
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from api.views import OrderItemViewSet
from django.urls import reverse
from api.models import Item, OrderItem
from rest_framework import status

User = get_user_model()


class ViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test', password='test', is_staff=True)
        cls.token = cls.user.auth_token

        cls.factory = APIRequestFactory()
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=1000)
        cls.order_item_1 = OrderItem.objects.create(item=cls.item, qty=50)
        cls.order_item_2 = OrderItem.objects.create(item=cls.item, qty=500)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.item.delete()
        cls.order_item_1.delete()
        cls.order_item_2.delete()

    def test_get_order_items_view_set(self):
        view = OrderItemViewSet.as_view(actions={'get': 'list'})
        request = self.factory.get(reverse('order_items-list'))
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_order_item_detail_view_set(self):
        view = OrderItemViewSet.as_view(actions={'get': 'retrieve'})
        url = reverse('order_items-detail', args=[self.order_item_1.id])
        request = self.factory.get(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.order_item_1.id)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
