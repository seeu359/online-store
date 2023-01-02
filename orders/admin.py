from django.contrib import admin

from orders.models import Order


class OrderAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'id')
    fields = (
        ('id', 'created_at'),
        ('first_name', 'last_name'),
        'email',
        'address',
        'status',
        'creator',
    )
    readonly_fields = ('id', 'created_at',)


admin.site.register(Order, OrderAdmin)
