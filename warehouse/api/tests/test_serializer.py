from django.test import TestCase
from api.serializers import ItemSerializer
from api.models import Item


class ItemSerializerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.item_1 = Item.objects.create(name='Dark Beer', price='20.0', qty=100)
        cls.item_2 = Item.objects.create(name='Sider', price='30.0', qty=1000)

    def test_serializer(self):
        serializer_data = ItemSerializer([self.item_1, self.item_2], many=True).data
        expected_data = [
            {
                'id': self.item_1.id,
                'name': 'Dark Beer',
                'price': '20.00',
                'qty': 100
            },
            {
                'id': self.item_2.id,
                'name': 'Sider',
                'price': '30.00',
                'qty': 1000
            }
        ]
        self.assertEquals(serializer_data, expected_data)