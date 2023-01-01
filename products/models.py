from django.db import models

from users.models import User


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
    category = models.ForeignKey(
        to=ProductCategory, on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


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
