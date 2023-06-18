from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

User = get_user_model()


class RegisterApiTestCase(APITestCase):

    def test_post_register_and_get_token(self):
        """ register a new user and get his token """
        url = reverse('register')
        new_user_data = {"username": "test", "password": "test"}
        response = self.client.post(url, data=new_user_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, {"response": "You've been registered"})

        self.client = APIClient()
        url = reverse('token')
        request_data = {"username": "test", "password": "test"}
        response = self.client.post(url, request_data, format='json')
        token = response.data.get('token')
        user = User.objects.get(username='test')
        expected_token = user.auth_token.key
        self.assertEquals(token, expected_token)