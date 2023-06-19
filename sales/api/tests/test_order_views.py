from django.test import TestCase
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from api.views import *
from django.urls import reverse
from api.models import *
from rest_framework import status


User = get_user_model()


class OrderViewSetTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user', password='test_pass')
        cls.user_2 = User.objects.create_user(username='unknown', password='unknown')
        cls.super_user = User.objects.create_superuser(username='super', password='super')
        cls.token = cls.user.auth_token
        cls.token_2 = cls.user_2.auth_token
        cls.super_token = cls.super_user.auth_token

        cls.factory = APIRequestFactory()

        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=1000)

        cls.order = Order.objects.create(customer=cls.user, is_placed=False)
        cls.order_item = OrderItem.objects.create(order=cls.order, item=cls.item, qty=500)

        cls.order_placed = Order.objects.create(customer=cls.user, is_placed=True)
        cls.order_item_2 = OrderItem.objects.create(order=cls.order_placed, item=cls.item, qty=50)

    def test_get_list_orders_view_set(self):
        view = OrderViewSet.as_view(actions={'get': 'list'})
        request = self.factory.get(reverse('orders-list'))
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        expected_data = [
            {
                "id": self.order.id,
                "customer": self.user.username,
                "created_at": self.order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "updated_at": self.order.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "is_placed": self.order.is_placed
            },
            {
                "id": self.order_placed.id,
                "customer": self.user.username,
                "created_at": self.order_placed.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "updated_at": self.order_placed.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "is_placed": self.order_placed.is_placed
            },
        ]
        self.assertEquals(response.data, expected_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        force_authenticate(request, user=self.user_2, token=self.token_2)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, [])

        force_authenticate(request, user=self.super_user, token=self.super_token)
        response = view(request)
        self.assertGreaterEqual(len(response.data), 0)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_order_detail_view_set(self):
        view = OrderViewSet.as_view(actions={'get': 'retrieve'})
        url = reverse('orders-detail', args=[self.order.id])
        request = self.factory.get(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.order.id)

        expected_data = {
            "id": self.order.id,
            "customer": self.user.username,
            "created_at": self.order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "updated_at": self.order.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "is_placed": self.order.is_placed,
            "items": [
                {
                    "id": self.order_item.id,
                    "item": self.item.id,
                    "qty": self.order_item.qty,
                    "max_qty": None
                }
            ]
        }
        self.assertEquals(response.data, expected_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_not_enough_data_create_method(self):
        view = OrderViewSet.as_view(actions={'post': 'create'})
        new_order_data = {
            'is_placed': False
        }
        request = self.factory.post(reverse('orders-list'), data=new_order_data, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'error': 'Not enough data to create Order'})

    def test_order_create_create_method(self):
        view = OrderViewSet.as_view(actions={'post': 'create'})
        new_order_data = {
            'is_placed': False,
            "items": [
                {
                    "item": self.item.id,
                    "qty": 50
                }
            ]
        }
        request = self.factory.post(reverse('orders-list'), data=new_order_data, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.last()
        self.assertEquals(response.data, {'Order complete - order_id': order.id})
        order.delete()

    def test_not_enough_item_quantity_create_method(self):
        view = OrderViewSet.as_view(actions={'post': 'create'})
        new_order_data = {
            'is_placed': False,
            "items": [
                {
                    "item": self.item.id,
                    "qty": 5000
                }
            ]
        }
        request = self.factory.post(reverse('orders-list'), data=new_order_data, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'error': f"Not enough quantity available for item {self.item.name}"})

    def test_item_does_not_exist_create_method(self):
        view = OrderViewSet.as_view(actions={'post': 'create'})
        new_order_data = {
            'is_placed': False,
            "items": [
                {
                    "item": self.item.id + 1,
                    "qty": 5000
                }
            ]
        }
        request = self.factory.post(reverse('orders-list'), data=new_order_data, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'error': f"Item with id {self.item.id + 1} does not exist"})

    def test_order_was_placed_update_method(self):
        view = OrderViewSet.as_view(actions={'put': 'update'})
        url = reverse('orders-detail', args=[self.order_placed.id])
        put_item_data = {
            "is_placed": False,
            "items": [
                {
                    "item": self.item.id,
                    "qty": 40
                }
            ]
        }
        request = self.factory.put(url, data=put_item_data, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.order_placed.id)
        self.assertEquals(response.data, {'Error': "This Order already was placed. Create another Order"})

    def test_item_does_not_exist_update_method(self):
        view = OrderViewSet.as_view(actions={'put': 'update'})
        url = reverse('orders-detail', args=[self.order.id])
        put_item_data = {
            "is_placed": False,
            "items": [
                {
                    "item": self.item.id + 1,
                    "qty": 40
                }
            ]
        }
        request = self.factory.put(url, data=put_item_data, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.order.id)
        self.assertEquals(response.data, {'error': f"Item with id {self.item.id + 1} does not exist"})

    def test_not_enough_item_quantity_update_method(self):
        view = OrderViewSet.as_view(actions={'put': 'update'})
        url = reverse('orders-detail', args=[self.order.id])
        put_item_data = {
            'is_placed': False,
            "items": [
                {
                    "item": self.item.id,
                    "qty": 5000
                }
            ]
        }
        request = self.factory.put(url, data=put_item_data, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.order.id)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'error': f"Not enough quantity available for item {self.item.name}"})

    def test_order_updated_update_method(self):
        view = OrderViewSet.as_view(actions={'put': 'update'})
        url = reverse('orders-detail', args=[self.order.id])
        put_item_data = {
            'is_placed': True,
            "items": [
                {
                    "item": self.item.id,
                    "max_qty": True
                }
            ]
        }
        request = self.factory.put(url, data=put_item_data, format='json')
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.order.id)
        self.assertEquals(response.status_code, status.HTTP_200_OK)