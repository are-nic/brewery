from django.test import TestCase
from api.models import Item


class ItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Item.objects.create(name='Beer', price='20.00', qty=1000)

    def setUp(self) -> None:
        self.item = Item.objects.get(name='Beer')

    def test_name_label(self):
        field_label = self.item._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_price_label(self):
        field_label = self.item._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'price')

    def test_qty_label(self):
        field_label = self.item._meta.get_field('qty').verbose_name
        self.assertEquals(field_label, 'qty')

    def test_name_max_length(self):
        max_length = self.item._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_price_max_digits(self):
        max_digits = self.item._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 10)