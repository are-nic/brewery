from django.test import TestCase
from rest_framework.test import force_authenticate
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from api.views import RegisterUserView, ItemViewSet
from django.urls import reverse
from api.models import Item
from rest_framework import status

User = get_user_model()


class RegisterUserViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = APIRequestFactory()

    @classmethod
    def tearDownClass(cls) -> None:
        User.objects.get(username='test').delete()

    def test_get_register_user_view(self):
        view = RegisterUserView.as_view()
        url = reverse('register')
        user_data = {
            'username': 'test',
            'password': 'test',
        }
        request = self.factory.post(url, user_data, format='json')
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)


class ItemViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test', password='test')
        cls.token = cls.user.auth_token

        cls.factory = APIRequestFactory()
        cls.item = Item.objects.create(name='Test Beer', price='20.00', qty=1000)
        cls.item_2 = Item.objects.create(name='Test Sider', price='30.00', qty=500)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.item.delete()
        cls.item_2.delete()

    def test_get_list_items_view_set(self):
        view = ItemViewSet.as_view(actions={'get': 'list'})
        request = self.factory.get(reverse('items-list'))
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_item_detail_view_set(self):
        view = ItemViewSet.as_view(actions={'get': 'retrieve'})
        url = reverse('items-detail', args=[self.item.id])
        request = self.factory.get(url)
        force_authenticate(request, user=self.user, token=self.token)
        response = view(request, pk=self.item.id)
        self.assertEquals(response.status_code, status.HTTP_200_OK)