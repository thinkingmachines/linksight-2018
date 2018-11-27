from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UsersAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_create_user_tokens(self):
        response = self.client.post('/api/users/me/tokens')
        token = Token.objects.get(user=self.user)
        self.assertEqual(token.key, response.data['key'])
