from django.test import TestCase
from api.serializers import OrderItemSerializer
from api.models import Item, OrderItem


class ItemSerializerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=100)
        cls.order_item = OrderItem.objects.create(item=cls.item, qty=50)

    def test_serializer(self):
        serializer_data = OrderItemSerializer(self.order_item).data
        expected_data = {
            'id': self.order_item.id,
            'item': self.item.id,
            'total_sum': 1000.0,
            'qty': 50
        }

        self.assertEquals(serializer_data, expected_data)