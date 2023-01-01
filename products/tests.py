from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from products.models import Basket, Product
from users.models import User


class ProductsTestCase(TestCase):

    fixtures = ['products.json', 'categories.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.get(id=3)
        self.login_url = reverse('users:login')
        self.products_url = reverse('products:products')
        self.all_products = Product.objects.all()
        self.products_count_bfr_test = 5

    def test_display_all_goods(self):
        response = self.client.get(self.products_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(
            list(response.context_data['products']),
            list(self.all_products[:3]),
        )

    def test_add_and_delete_goods_from_basket(self):
        self.client.force_login(self.user)
        empty_basket = Basket.objects.filter(user=self.user)
        self.assertTrue(len(empty_basket) == 0)
        response = self.client.post(
            reverse('products:add_basket', args=[2])
        )
        for i in range(3):
            self.client.post(
                reverse('products:add_basket', args=[3])
            )
        for i in range(4):
            self.client.post(
                reverse('products:add_basket', args=[4])
            )
        non_empty_basket = Basket.objects.filter(user=self.user)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(non_empty_basket.total_quantity(), 8)
        self.client.post(
            reverse('products:remove_basket', args=[4])
        )
        basket_with_4_items = Basket.objects.filter(user=self.user)
        self.assertEqual(basket_with_4_items.total_quantity(), 4)

    def test_add_goods_if_no_auth(self):
        link = reverse('products:add_basket', args=[2])
        response = self.client.post(link)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
