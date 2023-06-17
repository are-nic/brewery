from unittest import TestCase
from api.serializers import ItemSerializer
from api.models import Item


class ItemSerializerTestCase(TestCase):
    def test_serializer(self):
        item_1 = Item.objects.create(name='Dark Beer', price='20.0', qty=100)
        item_2 = Item.objects.create(name='Sider', price='30.0', qty=1000)
        serializer_data = ItemSerializer([item_1, item_2], many=True).data
        expected_data = [
            {
                'id': item_1.id,
                'name': 'Dark Beer',
                'price': '20.00',
                'qty': 100
            },
            {
                'id': item_2.id,
                'name': 'Sider',
                'price': '30.00',
                'qty': 1000
            }
        ]
        self.assertEquals(serializer_data, expected_data)