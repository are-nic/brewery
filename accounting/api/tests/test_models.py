from django.test import TestCase
from api.models import Item, OrderItem


class ItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=1000)

    @classmethod
    def tearDownClass(cls):
        cls.item.delete()
        print('Destroy test instances')

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


class OrderItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=1000)
        cls.order_item = OrderItem.objects.create(item=cls.item, qty=500)

    @classmethod
    def tearDownClass(cls):
        cls.order_item.delete()
        cls.item.delete()
        print('Destroy test instances')

    def test_item_label(self):
        field_label = self.order_item._meta.get_field('item').verbose_name
        self.assertEquals(field_label, 'item')

    def test_total_sum_label(self):
        field_label = self.order_item._meta.get_field('total_sum').verbose_name
        self.assertEquals(field_label, 'total sum')

    def test_qty_label(self):
        field_label = self.order_item._meta.get_field('qty').verbose_name
        self.assertEquals(field_label, 'qty')

    def test_object_name_is_item_name(self):
        expected_object_name = self.item.name
        self.assertEquals(expected_object_name, str(self.order_item))