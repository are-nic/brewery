from django.test import TestCase
from api.serializers import *
from api.models import *
from django.contrib.auth import get_user_model


User = get_user_model()


class ItemSerializerTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=100)

    @classmethod
    def tearDownClass(cls):
        cls.item.delete()

    def test_serializer(self):
        serializer_data = ItemSerializer(self.item).data
        expected_data = {
            'id': self.item.id,
            'name': 'Test Beer',
            'price': '20.00',
            'qty': 100
        }

        self.assertEquals(serializer_data, expected_data)


class OrderSerializerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test', password='test')
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=100)
        cls.order = Order.objects.create(customer=cls.user, is_placed=False)
        cls.order_item = OrderItem.objects.create(order=cls.order, item=cls.item, qty=50)

    def test_order_list_serializer(self):
        serializer_data = OrderListSerializer(self.order).data
        expected_data = {
            "id": self.order.id,
            "customer": self.user.username,
            "created_at": self.order.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "updated_at": self.order.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "is_placed": self.order.is_placed
        }
        self.assertEquals(serializer_data, expected_data)

    def test_order_detail_serializer(self):
        serializer_data = OrderDetailSerializer(self.order).data
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
                    "qty": 50,
                    "max_qty": None
                }
            ]
        }
        self.assertEquals(serializer_data, expected_data)

    def test_order_item_serializer(self):
        serializer_data = OrderItemSerializer(self.order_item).data
        expected_data = {
            "id": self.order_item.id,
            "item": self.item.id,
            "qty": 50,
            "max_qty": None
        }
        self.assertEquals(serializer_data, expected_data)


class UserRegisterSerializerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test', password='test')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_order_list_serializer(self):
        serializer_data = UserRegisterSerializer(self.user).data
        expected_data = {
            "username": self.user.username
        }
        self.assertEquals(serializer_data, expected_data)