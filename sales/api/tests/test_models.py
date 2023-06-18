from django.test import TestCase
from api.models import *
from django.contrib.auth import get_user_model


User = get_user_model()


class ItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Item.objects.create(name='Test Beer', price='20.00', qty=1000)

    def setUp(self) -> None:
        self.item = Item.objects.get(name='Test Beer')

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
        len_test_item_name = len(self.item.name)
        # self.assertEquals(max_length, 50)
        self.assertGreaterEqual(max_length, len_test_item_name)

    def test_price_max_digits(self):
        max_digits = self.item._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 10)


class OrderItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = User.objects.create_user(username='test', password='test')
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=100)
        cls.order = Order.objects.create(customer=cls.user, is_placed=False)
        cls.order_item = OrderItem.objects.create(order=cls.order, item=cls.item, qty=50)

    def test_order_label(self):
        field_label = self.order_item._meta.get_field('order').verbose_name
        self.assertEquals(field_label, 'order')

    def test_item_label(self):
        field_label = self.order_item._meta.get_field('item').verbose_name
        self.assertEquals(field_label, 'item')

    def test_qty_label(self):
        field_label = self.order_item._meta.get_field('qty').verbose_name
        self.assertEquals(field_label, 'qty')

    def test_object_name_is_item_name(self):
        expected_object_name = self.item.name
        self.assertEquals(expected_object_name, str(self.order_item))


class OrderModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test', password='test')
        cls.order = Order.objects.create(customer=cls.user, is_placed=False)

    def test_is_placed_field_help_text(self):
        self.assertEqual(self.order._meta.get_field('is_placed').help_text, 'The Order has been placed')
