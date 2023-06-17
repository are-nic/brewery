from unittest import TestCase
from api.serializers import OrderItemSerializer
from api.models import Item, OrderItem


class ItemSerializerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=100)
        cls.order_item = OrderItem.objects.create(item=cls.item, qty=50)

    @classmethod
    def tearDownClass(cls):
        cls.item.delete()
        cls.order_item.delete()
        print('Destroy test instances')

    def test_serializer(self):
        serializer_data = OrderItemSerializer(self.order_item).data
        expected_data = {
            'id': self.order_item.id,
            'item': self.item.id,
            'total_sum': 1000.0,
            'qty': 50
        }

        self.assertEquals(serializer_data, expected_data)