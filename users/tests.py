from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from users.models import EmailVerification, User


class UsersTestCase(TestCase):

    fixtures = ['users.json']

    def setUp(self) -> None:

        self.client = Client()
        self.users = User.objects.all()
        self.users_count_before_test = User.objects.all().count()
        self.login_url = reverse('users:login')
        self.register_url = reverse('users:register')
        self.test_data_for_reg = {
            'first_name': 'Testname',
            'last_name': 'Testlastname',
            'username': 'Testusername',
            'email': 'estemail@mail.ru',
            'password1': 'SuperSecretPass1',
            'password2': 'SuperSecretPass1',
        }

    def test_register_user_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_user_post(self):
        response = self.client.post(
            self.register_url, data=self.test_data_for_reg
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.login_url)
        users_after_reg = User.objects.all().count()
        self.assertEqual(users_after_reg, self.users_count_before_test + 1)
        # Test which check to created EmailVerificationObj
        email_vrf = EmailVerification.objects.filter(
            user__username=self.test_data_for_reg['username']
        )
        self.assertTrue(email_vrf.exists())
