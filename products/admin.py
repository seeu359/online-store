from django.contrib import admin

from products.models import Basket, Product, ProductCategory


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'quantity', 'id')
    fields = (
        'name',
        'category',
        'description',
        ('price', 'quantity'),
        'stripe_product_price_id',
        'image',
    )
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('stripe_product_price_id',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity',)
    extra = 0


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
