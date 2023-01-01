from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):

    link = reverse('main')

    def test_main_page(self):
        response = self.client.get(self.link)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')
