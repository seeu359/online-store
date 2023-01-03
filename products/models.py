from django.db import models

import stripe
from django.conf import settings

from users.models import User


stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):

    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):

    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    stripe_product_price_id = models.CharField(
        max_length=128, null=True, blank=True,
    )
    category = models.ForeignKey(
        to=ProductCategory, on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None,
             ):

        if not self.stripe_product_price_id:
            product_price = self.create_stripe_product_and_price()
            self.stripe_product_price_id = product_price['id']

        super().save(force_insert=False,
                     force_update=False,
                     using=None,
                     update_fields=None,
                     )

    def create_stripe_product_and_price(self):

        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='rub',
        )

        return stripe_product_price


class BasketRelatedManager(models.QuerySet):

    def total_price(self):

        return sum(good.sum_price() for good in self)

    def total_quantity(self):

        return sum(good.quantity for good in self)


class Basket(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketRelatedManager.as_manager()

    def __str__(self):

        return f'Корзина пользователя {self.user.get_full_name()}'

    def sum_price(self):

        return self.product.price * self.quantity
